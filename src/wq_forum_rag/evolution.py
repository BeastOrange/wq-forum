from __future__ import annotations

from pathlib import Path
from typing import Any

from wq_forum_rag.knowledge import DRAFT, PUBLISHED, KnowledgePage, KnowledgeStore
from wq_forum_rag.search import ForumSearcher
from wq_forum_rag.storage import ForumStore
from wq_forum_rag.wiki import WikiService

AUTO_PUBLISH_CONFIDENCE = 0.85


class EvolutionService:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def build_evolution_context(self, query: str, top_k: int = 5) -> dict[str, Any]:
        knowledge = self.search_knowledge(query, top_k=min(top_k, 5), include_drafts=False)
        forum = self.search_forum(query, top_k=top_k)
        posts = [self.get_post(item["topic_id"]) for item in forum]
        return {
            "query": query,
            "instructions": (
                "Use published_knowledge first, then forum_evidence. "
                "Call propose_knowledge_page with source_topic_ids that support each key claim."
            ),
            "published_knowledge": knowledge,
            "forum_evidence": [post for post in posts if post],
        }

    def propose_knowledge_page(
        self,
        *,
        slug: str,
        title: str,
        summary: str,
        body: str,
        source_topic_ids: list[str],
        confidence: float,
        links: list[dict[str, Any]] | None = None,
        auto_publish: bool = True,
    ) -> dict[str, Any]:
        page = KnowledgePage(
            slug=slug,
            title=title,
            summary=summary,
            body=body,
            status=DRAFT,
            confidence=confidence,
        )
        unique_sources = sorted({str(topic_id) for topic_id in source_topic_ids if str(topic_id).strip()})
        with KnowledgeStore(self.db_path) as store:
            if not store.topic_ids_exist(unique_sources):
                raise ValueError("source_topic_ids must reference existing forum topics")
            issues = self._lint_page_payload(page, unique_sources, links or [])
            can_auto_publish = (
                auto_publish
                and page.confidence >= AUTO_PUBLISH_CONFIDENCE
                and not any(item["severity"] == "block" for item in issues)
            )
            if can_auto_publish:
                page.status = PUBLISHED
            stored = store.upsert_page(
                page,
                source_topic_ids=unique_sources,
                links=links or [],
                event_type="proposed",
                event_note="auto-published" if page.status == PUBLISHED else "drafted",
            )
            return {
                "page": store.get_page(stored.slug),
                "issues": issues,
                "auto_published": stored.status == PUBLISHED,
            }

    def publish_knowledge_page(self, slug: str) -> dict[str, Any]:
        issues = self.lint_knowledge(slug=slug)["issues"]
        blockers = [item for item in issues if item["severity"] == "block"]
        if blockers:
            return {"published": False, "slug": slug, "issues": blockers}
        with KnowledgeStore(self.db_path) as store:
            return {"published": True, "page": store.set_status(slug, PUBLISHED, "manual publish")}

    def get_knowledge_page(self, slug: str) -> dict[str, Any] | None:
        with KnowledgeStore(self.db_path) as store:
            return store.get_page(slug)

    def link_knowledge_pages(
        self,
        source_slug: str,
        target_slug: str,
        relation_type: str,
        *,
        weight: float = 1.0,
        confidence: float = 0.8,
    ) -> dict[str, Any]:
        with KnowledgeStore(self.db_path) as store:
            return store.link_pages(
                source_slug,
                target_slug,
                relation_type,
                weight=weight,
                confidence=confidence,
            )

    def search_knowledge(
        self,
        query: str,
        top_k: int = 5,
        *,
        include_drafts: bool = False,
    ) -> list[dict[str, Any]]:
        with KnowledgeStore(self.db_path) as store:
            pages = store.list_pages(include_drafts=include_drafts)
            link_counts = self._link_counts(store)
        if not pages or top_k <= 0:
            return []
        chunks = [
            {
                "topic_id": page["slug"],
                "chunk_id": page["slug"],
                "community": "knowledge",
                "title": page["title"],
                "content": f"{page['summary']}\n{page['body']}",
            }
            for page in pages
        ]
        hits = ForumSearcher(chunks, dense_weight=0.45, lexical_weight=0.55).search(
            query,
            top_k=max(top_k * 3, top_k),
        )
        pages_by_slug = {page["slug"]: page for page in pages}
        ranked: list[dict[str, Any]] = []
        for hit in hits:
            page = pages_by_slug[hit.topic_id]
            boost = min(link_counts.get(hit.topic_id, 0) * 0.04, 0.24)
            ranked.append(
                {
                    "slug": page["slug"],
                    "title": page["title"],
                    "summary": page["summary"],
                    "status": page["status"],
                    "confidence": page["confidence"],
                    "score": hit.score + boost,
                    "backlink_boost": boost,
                    "snippet": hit.snippet,
                }
            )
        ranked.sort(key=lambda item: (item["score"], item["confidence"], item["slug"]), reverse=True)
        return ranked[:top_k]

    def search_forum(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        rows = self._chunk_rows()
        if not rows:
            return []
        topic_meta = {row["topic_id"]: row for row in rows}
        hits = ForumSearcher(rows).search(query=query, top_k=max(top_k * 3, top_k))
        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        for hit in hits:
            if hit.topic_id in seen:
                continue
            seen.add(hit.topic_id)
            meta = topic_meta[hit.topic_id]
            results.append(
                {
                    "topic_id": hit.topic_id,
                    "community_id": meta["community_id"],
                    "community_title": hit.community,
                    "title": hit.title,
                    "author": meta["author"],
                    "datetime": meta["created_at"],
                    "url": meta["url"],
                    "vote_num": meta["vote_num"],
                    "comment_num": meta["comment_count"],
                    "snippet": hit.snippet,
                    "score": hit.score,
                }
            )
            if len(results) >= top_k:
                break
        return results

    def get_post(self, topic_id: str) -> dict[str, Any] | None:
        with ForumStore(self.db_path) as store:
            topic = store.get_topic(topic_id)
        if topic is None:
            return None
        payload = topic.to_dict()
        payload["topic_id"] = payload.get("id", topic_id)
        return payload

    def lint_knowledge(self, slug: str | None = None) -> dict[str, Any]:
        with KnowledgeStore(self.db_path) as store:
            pages = [store.get_page(slug)] if slug else [
                store.get_page(page["slug"]) for page in store.list_pages(include_drafts=True)
            ]
        issues: list[dict[str, Any]] = []
        for page in [item for item in pages if item]:
            page_issues = self._lint_page_record(page)
            issues.extend(page_issues)
        return {
            "slug": slug,
            "issues": issues,
            "blocking_count": sum(1 for item in issues if item["severity"] == "block"),
            "warning_count": sum(1 for item in issues if item["severity"] == "warn"),
        }

    def graph_query(self, slug: str, *, depth: int = 1, relation_type: str | None = None) -> dict[str, Any]:
        return WikiService(self.db_path).graph_query(slug, depth=depth, relation_type=relation_type)

    def export_wiki(
        self,
        output_dir: str | Path = ".cache/wiki",
        *,
        include_drafts: bool = False,
    ) -> dict[str, Any]:
        return WikiService(self.db_path).export_wiki(output_dir, include_drafts=include_drafts)

    def _chunk_rows(self) -> list[dict[str, Any]]:
        with ForumStore(self.db_path) as store:
            rows = store.conn.execute(
                """
                SELECT
                    c.chunk_id,
                    c.topic_id,
                    c.community_id,
                    c.content,
                    t.title,
                    t.community_title,
                    t.author,
                    t.created_at,
                    t.url,
                    t.vote_num,
                    t.comment_count
                FROM chunks AS c
                JOIN topics AS t ON t.topic_id = c.topic_id
                WHERE c.chunk_level = 1
                ORDER BY c.topic_id, c.chunk_level, c.chunk_index
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def _lint_page_payload(
        self,
        page: KnowledgePage,
        source_topic_ids: list[str],
        links: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if not source_topic_ids:
            issues.append(self._issue(page.slug, "block", "missing_sources"))
        if page.confidence < AUTO_PUBLISH_CONFIDENCE:
            issues.append(self._issue(page.slug, "warn", "low_confidence"))
        if any(link.get("relation_type") == "conflicts_with" for link in links):
            issues.append(self._issue(page.slug, "block", "conflict_link_present"))
        if len(page.summary) < 20 or len(page.body) < 40:
            issues.append(self._issue(page.slug, "warn", "thin_content"))
        return issues

    def _lint_page_record(self, page: dict[str, Any]) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if not page["sources"]:
            issues.append(self._issue(page["slug"], "block", "missing_sources"))
        if float(page["confidence"]) < AUTO_PUBLISH_CONFIDENCE:
            issues.append(self._issue(page["slug"], "warn", "low_confidence"))
        links = page["links"] + page["backlinks"]
        if any(item["relation_type"] == "conflicts_with" for item in links):
            issues.append(self._issue(page["slug"], "block", "conflict_link_present"))
        if not links:
            issues.append(self._issue(page["slug"], "warn", "orphan_page"))
        return issues

    def _link_counts(self, store: KnowledgeStore) -> dict[str, int]:
        rows = store.conn.execute(
            """
            SELECT target_slug AS slug, COUNT(*) AS count
            FROM knowledge_links
            GROUP BY target_slug
            UNION ALL
            SELECT source_slug AS slug, COUNT(*) AS count
            FROM knowledge_links
            GROUP BY source_slug
            """
        ).fetchall()
        counts: dict[str, int] = {}
        for row in rows:
            counts[str(row["slug"])] = counts.get(str(row["slug"]), 0) + int(row["count"])
        return counts

    @staticmethod
    def _issue(slug: str, severity: str, code: str) -> dict[str, str]:
        return {"slug": slug, "severity": severity, "code": code}

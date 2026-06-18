# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

from pathlib import Path
from typing import Any

from wq_forum_rag.indexer import ForumIndexService
from wq_forum_rag.knowledge import DRAFT, PUBLISHED, KnowledgePage, KnowledgeStore
from wq_forum_rag.search_index import search_forum_records, search_knowledge_records
from wq_forum_rag.storage import ForumStore
from wq_forum_rag.wiki import WikiService

AUTO_PUBLISH_CONFIDENCE = 0.85


class EvolutionService:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def build_evolution_context(self, query: str, top_k: int = 5) -> dict[str, Any]:
        self._ensure_forum_fresh()
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
        self._ensure_forum_fresh()
        with ForumStore(self.db_path) as store:
            return search_knowledge_records(
                store.conn,
                query,
                top_k=top_k,
                include_drafts=include_drafts,
            )

    def search_forum(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        self._ensure_forum_fresh()
        with ForumStore(self.db_path) as store:
            return search_forum_records(store.conn, query, top_k=top_k)

    def get_post(self, topic_id: str) -> dict[str, Any] | None:
        self._ensure_forum_fresh()
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

    def _ensure_forum_fresh(self) -> None:
        ForumIndexService(self.db_path).auto_refresh_if_needed()

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

    @staticmethod
    def _issue(slug: str, severity: str, code: str) -> dict[str, str]:
        return {"slug": slug, "severity": severity, "code": code}

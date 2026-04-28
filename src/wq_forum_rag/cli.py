from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from wq_forum_rag.evolution_cli import register_evolution_commands

DEFAULT_DB_PATH = Path(".cache/forum.sqlite3")
app = typer.Typer(no_args_is_help=True, help="Offline lightweight RAG for WQ forum exports")
console = Console()


def _load_module(name: str) -> Any:
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise RuntimeError(f"Missing required module: {name}") from exc


class ForumIndexService:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.parser = _load_module("wq_forum_rag.parser")
        self.search_mod = _load_module("wq_forum_rag.search")
        self.storage = _load_module("wq_forum_rag.storage")

    def index_from_json(self, json_path: str | Path, rebuild: bool = False) -> dict[str, Any]:
        source = Path(json_path)
        stat = source.stat()
        fingerprint = {
            "source_path": str(source.resolve()),
            "source_mtime_ns": str(stat.st_mtime_ns),
            "source_size": str(stat.st_size),
        }
        with self.storage.ForumStore(self.db_path) as store:
            known = dict(store.conn.execute("SELECT key, value FROM schema_meta").fetchall())
            if not rebuild and all(known.get(key) == value for key, value in fingerprint.items()):
                total = store.conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
                return {"status": "unchanged", "db": str(self.db_path), "json": str(source), "indexed_topics": total}
            if rebuild:
                store.conn.execute("DELETE FROM chunks")
                store.conn.execute("DELETE FROM topics")
            stats = store.upsert_topics(self.parser.iter_topics(source))
            with store.conn:
                store.conn.executemany(
                    """
                    INSERT INTO schema_meta(key, value) VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """,
                    fingerprint.items(),
                )
            total = store.conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
        return {"status": "rebuilt" if rebuild else "indexed", "db": str(self.db_path), "json": str(source), "indexed_topics": total, **stats}

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        with self.storage.ForumStore(self.db_path) as store:
            rows = [
                dict(row)
                for row in store.conn.execute(
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
            ]
        topic_meta = {row["topic_id"]: row for row in rows}
        hits = self.search_mod.ForumSearcher(rows).search(query=query, top_k=max(top_k * 3, top_k))
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
        with self.storage.ForumStore(self.db_path) as store:
            topic = store.get_topic(topic_id)
        if topic is None:
            return None
        payload = topic.to_dict()
        payload.setdefault("topic_id", payload.get("id", topic_id))
        return payload

    def find_by_exact(
        self,
        value: str,
        *,
        community: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        normalized = value.strip()
        if not normalized:
            return []
        lowered = normalized.lower()
        like_value = f"%{lowered}%"
        with self.storage.ForumStore(self.db_path) as store:
            rows = store.conn.execute(
                """
                SELECT
                    t.topic_id,
                    t.community_id,
                    t.community_title,
                    t.title,
                    t.author,
                    t.created_at,
                    t.url,
                    t.vote_num,
                    t.comment_count,
                    MAX(CASE
                        WHEN t.topic_id = ? THEN 100
                        WHEN lower(t.url) = ? THEN 95
                        WHEN lower(t.title) = ? THEN 90
                        WHEN lower(t.title) LIKE ? THEN 75
                        WHEN lower(t.body_text) LIKE ? THEN 60
                        WHEN lower(t.comments_json) LIKE ? THEN 50
                        WHEN lower(c.content) LIKE ? THEN 40
                        ELSE 0
                    END) AS exact_rank,
                    MIN(CASE
                        WHEN lower(c.content) LIKE ? THEN c.content
                        ELSE NULL
                    END) AS matched_content
                FROM topics AS t
                LEFT JOIN chunks AS c ON c.topic_id = t.topic_id AND c.chunk_level = 1
                WHERE
                    (? IS NULL OR t.community_id = ? OR lower(t.community_title) = ?)
                    AND (
                        t.topic_id = ?
                        OR lower(t.url) = ?
                        OR lower(t.title) = ?
                        OR lower(t.title) LIKE ?
                        OR lower(t.body_text) LIKE ?
                        OR lower(t.comments_json) LIKE ?
                        OR lower(c.content) LIKE ?
                    )
                GROUP BY t.topic_id
                ORDER BY exact_rank DESC, t.vote_num DESC, t.comment_count DESC, t.created_at DESC
                LIMIT ?
                """,
                (
                    normalized,
                    lowered,
                    lowered,
                    like_value,
                    like_value,
                    like_value,
                    like_value,
                    like_value,
                    community,
                    community,
                    community.lower() if community else None,
                    normalized,
                    lowered,
                    lowered,
                    like_value,
                    like_value,
                    like_value,
                    like_value,
                    top_k,
                ),
            ).fetchall()
        return [
            {
                "topic_id": str(row["topic_id"]),
                "community_id": row["community_id"],
                "community_title": row["community_title"],
                "title": row["title"],
                "author": row["author"],
                "datetime": row["created_at"],
                "url": row["url"],
                "vote_num": row["vote_num"],
                "comment_num": row["comment_count"],
                "snippet": self.search_mod._build_snippet(  # noqa: SLF001
                    normalized,
                    {"content": row["matched_content"] or row["title"], "title": row["title"]},
                ),
                "rank": row["exact_rank"],
            }
            for row in rows
        ]

    def related_posts(self, topic_id: str, top_k: int = 5) -> list[dict[str, Any]]:
        base = self.get_post(topic_id)
        if not base:
            return []
        ranked = [item for item in self.search(base["title"], top_k=top_k + 3) if item["topic_id"] != topic_id]
        same_community = [item for item in ranked if item["community_id"] == base["community_id"]]
        return (same_community + [item for item in ranked if item["community_id"] != base["community_id"]])[:top_k]


def _render_search(results: list[dict[str, Any]]) -> None:
    table = Table(title=f"Top {len(results)}")
    for name in ("topic_id", "community_title", "title", "author", "score"):
        table.add_column(name)
    for item in results:
        table.add_row(item["topic_id"], item["community_title"], item["title"], item["author"], f"{item['score']:.3f}")
    console.print(table)


@app.command("index")
def index_command(
    json_path: Path = typer.Option(..., "--json", exists=True, dir_okay=False, readable=True),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", dir_okay=False),
    rebuild: bool = typer.Option(False, "--rebuild", help="Force full rebuild"),
) -> None:
    console.print_json(data=ForumIndexService(db_path).index_from_json(json_path=json_path, rebuild=rebuild))


@app.command("search")
def search_command(
    query: str = typer.Argument(..., help="Full-text query"),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False, readable=True),
    top_k: int = typer.Option(5, "--top-k", min=1, max=20),
) -> None:
    _render_search(ForumIndexService(db_path).search(query=query, top_k=top_k))


@app.command("show")
def show_command(
    topic_id: str = typer.Argument(..., help="Forum topic id"),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False, readable=True),
) -> None:
    post = ForumIndexService(db_path).get_post(topic_id)
    if post is None:
        raise typer.Exit(code=1)
    console.print_json(data=post)


def main() -> None:
    app()


register_evolution_commands(app)

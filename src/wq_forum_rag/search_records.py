# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

import sqlite3
from typing import Any

from wq_forum_rag.embeddings import EmbeddingBackend, build_embedding_backend
from wq_forum_rag.search import ForumSearcher
from wq_forum_rag.search_cache import CachedEmbeddingBackend


def search_forum_records(
    conn: sqlite3.Connection,
    query: str,
    *,
    top_k: int = 5,
    embedding_backend: EmbeddingBackend | None = None,
) -> list[dict[str, Any]]:
    rows = _forum_candidate_rows(conn, query, top_k=max(top_k * 20, 80)) or [
        dict(row) for row in _forum_detail_rows(conn)
    ]
    if not rows or top_k <= 0:
        return []

    backend = _backend(conn, embedding_backend)
    hits = ForumSearcher(rows, embedding_backend=backend).search(query=query, top_k=max(top_k * 3, top_k))
    meta = {row["topic_id"]: row for row in rows}
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for hit in hits:
        if hit.topic_id in seen:
            continue
        seen.add(hit.topic_id)
        results.append(_hit_payload(hit, meta[hit.topic_id]))
        if len(results) >= top_k:
            break
    return results


def search_knowledge_records(
    conn: sqlite3.Connection,
    query: str,
    *,
    top_k: int = 5,
    include_drafts: bool = False,
    embedding_backend: EmbeddingBackend | None = None,
) -> list[dict[str, Any]]:
    pages = _knowledge_candidate_rows(
        conn,
        query,
        top_k=max(top_k * 20, 80),
        include_drafts=include_drafts,
    ) or _knowledge_detail_rows(conn, include_drafts=include_drafts)
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
    hits = ForumSearcher(
        chunks,
        embedding_backend=_backend(conn, embedding_backend),
        dense_weight=0.45,
        lexical_weight=0.55,
    ).search(query=query, top_k=max(top_k * 3, top_k))
    return _knowledge_results(hits, pages, _knowledge_link_counts(conn), top_k)


def _backend(conn: sqlite3.Connection, embedding_backend: EmbeddingBackend | None):
    db_path = _db_path(conn)
    if db_path:
        return CachedEmbeddingBackend(db_path, backend=embedding_backend)
    return embedding_backend or build_embedding_backend()


def _forum_detail_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT c.chunk_id, c.topic_id, c.community_id, c.content, t.title,
               t.community_title, t.author, t.created_at, t.url, t.vote_num, t.comment_count
        FROM chunks AS c
        JOIN topics AS t ON t.topic_id = c.topic_id
        WHERE c.chunk_level = 1
        ORDER BY c.topic_id, c.chunk_index
        """
    ).fetchall()


def _forum_candidate_rows(conn: sqlite3.Connection, query: str, *, top_k: int) -> list[dict[str, Any]]:
    from wq_forum_rag.search_index import _fts_query, _table_exists

    match_query = _fts_query(query)
    if not match_query or not _table_exists(conn, "document_fts"):
        return []
    try:
        rows = conn.execute(
            """
            SELECT c.chunk_id, c.topic_id, c.community_id, c.content, t.title,
                   t.community_title, t.author, t.created_at, t.url, t.vote_num, t.comment_count
            FROM document_fts
            JOIN chunks AS c ON c.chunk_id = document_fts.record_id
            JOIN topics AS t ON t.topic_id = c.topic_id
            WHERE kind = 'forum_chunk' AND document_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (match_query, top_k),
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return [dict(row) for row in rows]


def _knowledge_detail_rows(conn: sqlite3.Connection, *, include_drafts: bool) -> list[dict[str, Any]]:
    from wq_forum_rag.search_index import _table_exists

    if not _table_exists(conn, "knowledge_pages"):
        return []
    where = "" if include_drafts else "WHERE status = 'published'"
    rows = conn.execute(
        f"""
        SELECT slug, title, summary, body, status, confidence
        FROM knowledge_pages
        {where}
        ORDER BY status DESC, confidence DESC, updated_at DESC, slug
        """
    ).fetchall()
    return [dict(row) for row in rows]


def _knowledge_candidate_rows(conn: sqlite3.Connection, query: str, *, top_k: int, include_drafts: bool):
    from wq_forum_rag.search_index import _fts_query, _table_exists

    match_query = _fts_query(query)
    if not match_query or not _table_exists(conn, "document_fts") or not _table_exists(conn, "knowledge_pages"):
        return []
    rows = conn.execute(
        """
        SELECT knowledge_pages.slug, knowledge_pages.title, knowledge_pages.summary,
               knowledge_pages.body, knowledge_pages.status, knowledge_pages.confidence
        FROM document_fts
        JOIN knowledge_pages ON knowledge_pages.slug = document_fts.record_id
        WHERE kind = 'knowledge_page' AND document_fts MATCH ?
          AND (? OR knowledge_pages.status = 'published')
        ORDER BY rank
        LIMIT ?
        """,
        (match_query, int(include_drafts), top_k),
    ).fetchall()
    return [dict(row) for row in rows]


def _knowledge_results(hits: Any, pages: list[dict[str, Any]], link_counts: dict[str, int], top_k: int):
    pages_by_slug = {page["slug"]: page for page in pages}
    results = []
    for hit in hits:
        page = pages_by_slug[hit.topic_id]
        boost = min(link_counts.get(hit.topic_id, 0) * 0.04, 0.24)
        results.append({**{k: page[k] for k in ("slug", "title", "summary", "status", "confidence")}, "score": hit.score + boost, "backlink_boost": boost, "snippet": hit.snippet})
    results.sort(key=lambda item: (item["score"], item["confidence"], item["slug"]), reverse=True)
    return results[:top_k]


def _knowledge_link_counts(conn: sqlite3.Connection) -> dict[str, int]:
    from wq_forum_rag.search_index import _table_exists

    if not _table_exists(conn, "knowledge_links"):
        return {}
    rows = conn.execute("SELECT target_slug, COUNT(*) AS link_count FROM knowledge_links GROUP BY target_slug").fetchall()
    return {str(row["target_slug"]): int(row["link_count"]) for row in rows}


def _db_path(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("PRAGMA database_list").fetchone()
    return None if row is None or not row[2] else str(row[2])


def _hit_payload(hit: Any, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "topic_id": hit.topic_id,
        "community_id": row["community_id"],
        "community_title": hit.community,
        "title": hit.title,
        "author": row["author"],
        "datetime": row["created_at"],
        "url": row["url"],
        "vote_num": row["vote_num"],
        "comment_num": row["comment_count"],
        "snippet": hit.snippet,
        "score": hit.score,
    }

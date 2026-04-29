# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .cli import DEFAULT_DB_PATH, ForumIndexService
from .evolution import EvolutionService
from .manifest import SourceManifestService
from .search_index import (
    rebuild_search_index as rebuild_search_index_impl,
    search_knowledge_records,
)
from .storage import ForumStore

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:  # pragma: no cover
    class FastMCP:  # type: ignore[override]
        def __init__(self, name: str, **_: Any) -> None:
            self.name = name
            self.tools: dict[str, Any] = {}

        def tool(self, **_: Any):
            def decorator(func: Any) -> Any:
                self.tools[func.__name__] = func
                return func

            return decorator

        def run(self, transport: str = "stdio") -> None:
            raise RuntimeError(f"mcp is not installed; cannot run transport={transport}")


def _resolve_db_path(db: str | None) -> Path:
    return Path(db or os.environ.get("WQ_FORUM_RAG_DB") or DEFAULT_DB_PATH)


def search_forum(query: str, db: str | None = None, top_k: int = 5) -> dict[str, Any]:
    results = ForumIndexService(_resolve_db_path(db)).search(query=query, top_k=top_k)
    return {"query": query, "db": str(_resolve_db_path(db)), "results": results}


def get_post(topic_id: str, db: str | None = None) -> dict[str, Any]:
    post = ForumIndexService(_resolve_db_path(db)).get_post(topic_id)
    return {"topic_id": topic_id, "db": str(_resolve_db_path(db)), "post": post}


def find_by_exact(
    value: str,
    db: str | None = None,
    community: str | None = None,
    top_k: int = 5,
) -> dict[str, Any]:
    results = ForumIndexService(_resolve_db_path(db)).find_by_exact(
        value,
        community=community,
        top_k=top_k,
    )
    return {"value": value, "db": str(_resolve_db_path(db)), "results": results}


def related_posts(topic_id: str, db: str | None = None, top_k: int = 5) -> dict[str, Any]:
    posts = ForumIndexService(_resolve_db_path(db)).related_posts(topic_id=topic_id, top_k=top_k)
    return {"topic_id": topic_id, "db": str(_resolve_db_path(db)), "results": posts}


def source_status(source: str, db: str | None = None) -> dict[str, Any]:
    return SourceManifestService(_resolve_db_path(db)).source_status(source)


def source_ingest_plan(
    source: str,
    db: str | None = None,
    commit: bool = False,
) -> dict[str, Any]:
    return SourceManifestService(_resolve_db_path(db)).source_ingest_plan(source, commit=commit)


def build_evolution_context(query: str, db: str | None = None, top_k: int = 5) -> dict[str, Any]:
    context = EvolutionService(_resolve_db_path(db)).build_evolution_context(
        query=query,
        top_k=top_k,
    )
    return {"query": query, "db": str(_resolve_db_path(db)), **context}


def propose_knowledge_page(
    slug: str,
    title: str,
    summary: str,
    body: str,
    source_topic_ids: list[str],
    confidence: float,
    db: str | None = None,
    links: list[dict[str, Any]] | None = None,
    auto_publish: bool = True,
) -> dict[str, Any]:
    result = EvolutionService(_resolve_db_path(db)).propose_knowledge_page(
        slug=slug,
        title=title,
        summary=summary,
        body=body,
        source_topic_ids=source_topic_ids,
        confidence=confidence,
        links=links,
        auto_publish=auto_publish,
    )
    return {"db": str(_resolve_db_path(db)), **result}


def search_knowledge(
    query: str,
    db: str | None = None,
    top_k: int = 5,
    include_drafts: bool = False,
) -> dict[str, Any]:
    with ForumStore(_resolve_db_path(db)) as store:
        results = search_knowledge_records(
            store.conn,
            query=query,
            top_k=top_k,
            include_drafts=include_drafts,
        )
    return {"query": query, "db": str(_resolve_db_path(db)), "results": results}


def get_knowledge_page(slug: str, db: str | None = None) -> dict[str, Any]:
    page = EvolutionService(_resolve_db_path(db)).get_knowledge_page(slug)
    return {"slug": slug, "db": str(_resolve_db_path(db)), "page": page}


def link_knowledge_pages(
    source_slug: str,
    target_slug: str,
    relation_type: str,
    db: str | None = None,
    weight: float = 1.0,
    confidence: float = 0.8,
) -> dict[str, Any]:
    link = EvolutionService(_resolve_db_path(db)).link_knowledge_pages(
        source_slug,
        target_slug,
        relation_type,
        weight=weight,
        confidence=confidence,
    )
    return {"db": str(_resolve_db_path(db)), "link": link}


def lint_knowledge(db: str | None = None, slug: str | None = None) -> dict[str, Any]:
    result = EvolutionService(_resolve_db_path(db)).lint_knowledge(slug=slug)
    return {"db": str(_resolve_db_path(db)), **result}


def publish_knowledge_page(slug: str, db: str | None = None) -> dict[str, Any]:
    result = EvolutionService(_resolve_db_path(db)).publish_knowledge_page(slug)
    return {"db": str(_resolve_db_path(db)), **result}


def graph_query(
    slug: str,
    db: str | None = None,
    depth: int = 1,
    relation_type: str | None = None,
) -> dict[str, Any]:
    result = EvolutionService(_resolve_db_path(db)).graph_query(
        slug,
        depth=depth,
        relation_type=relation_type,
    )
    return {"db": str(_resolve_db_path(db)), **result}


def export_knowledge_wiki(
    db: str | None = None,
    output_dir: str = ".cache/wiki",
    include_drafts: bool = False,
) -> dict[str, Any]:
    result = EvolutionService(_resolve_db_path(db)).export_wiki(
        output_dir,
        include_drafts=include_drafts,
    )
    return {"db": str(_resolve_db_path(db)), **result}


def rebuild_search_index(db: str | None = None) -> dict[str, Any]:
    result = rebuild_search_index_impl(_resolve_db_path(db))
    return {"db": str(_resolve_db_path(db)), **result}


def build_mcp_server(default_db: str | Path | None = None) -> FastMCP:
    if default_db:
        os.environ.setdefault("WQ_FORUM_RAG_DB", str(default_db))
    server = FastMCP("wq-forum-rag", json_response=True)
    server.tool()(search_forum)
    server.tool()(get_post)
    server.tool()(find_by_exact)
    server.tool()(related_posts)
    server.tool()(source_status)
    server.tool()(source_ingest_plan)
    server.tool()(build_evolution_context)
    server.tool()(propose_knowledge_page)
    server.tool()(search_knowledge)
    server.tool()(get_knowledge_page)
    server.tool()(link_knowledge_pages)
    server.tool()(lint_knowledge)
    server.tool()(publish_knowledge_page)
    server.tool()(graph_query)
    server.tool()(export_knowledge_wiki)
    server.tool()(rebuild_search_index)
    return server


mcp = build_mcp_server()


def main() -> None:
    mcp.run(transport="stdio")

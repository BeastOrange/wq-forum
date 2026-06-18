# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from wq_forum_rag.documents import ingest_documents as ingest_documents_impl, DocumentStore
from wq_forum_rag.evolution_cli import register_evolution_commands
from wq_forum_rag.indexer import ForumIndexService
from wq_forum_rag.manifest import SourceManifestService
from wq_forum_rag.source_cli import register_source_commands
from wq_forum_rag.search_index import rebuild_search_index
from wq_forum_rag.search_records import search_doc_records

DEFAULT_DB_PATH = Path(".cache/forum.sqlite3")
app = typer.Typer(no_args_is_help=True, help="Offline lightweight RAG for WQ forum exports")
console = Console()

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
    prune: bool = typer.Option(
        True,
        "--prune/--no-prune",
        help="Delete topics present in DB but absent from new JSON (skipped on --rebuild)",
    ),
) -> None:
    console.print_json(
        data=ForumIndexService(db_path).index_from_json(
            json_path=json_path, rebuild=rebuild, prune=prune
        )
    )


@app.command("refresh")
def refresh_command(
    json_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", dir_okay=False),
    rebuild: bool = typer.Option(False, "--rebuild", help="Force full rebuild"),
    prune: bool = typer.Option(
        True,
        "--prune/--no-prune",
        help="Delete topics present in DB but absent from new JSON (skipped on --rebuild)",
    ),
) -> None:
    """Index forum JSON and commit source manifest in one step."""
    index_result = ForumIndexService(db_path).index_from_json(
        json_path=json_path, rebuild=rebuild, prune=prune
    )
    manifest_result = SourceManifestService(db_path).source_ingest_plan(json_path, commit=True)
    console.print_json(data={"index": index_result, "manifest": manifest_result})


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


@app.command("search-reindex")
def search_reindex_command(
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
) -> None:
    console.print_json(data=rebuild_search_index(db_path))


@app.command("ingest-docs")
def ingest_docs_command(
    directory: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", dir_okay=False),
    rebuild: bool = typer.Option(False, "--rebuild", help="Force full rebuild"),
    prune: bool = typer.Option(
        True,
        "--prune/--no-prune",
        help="Delete documents present in DB but absent from directory (skipped on --rebuild)",
    ),
) -> None:
    """Ingest a directory of markdown documents into the database."""
    ingest_result = ingest_documents_impl(directory, db_path, rebuild=rebuild, prune=prune)
    search_index = rebuild_search_index(db_path)
    console.print_json(data={**ingest_result, "search_index": search_index})


@app.command("search-docs")
def search_docs_command(
    query: str = typer.Argument(..., help="Full-text query"),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False, readable=True),
    top_k: int = typer.Option(5, "--top-k", min=1, max=20),
) -> None:
    import sqlite3 as _sqlite3

    with _sqlite3.connect(db_path) as conn:
        conn.row_factory = _sqlite3.Row
        results = search_doc_records(conn, query=query, top_k=top_k)
    table = Table(title=f"Top {len(results)}")
    for name in ("slug", "title", "score"):
        table.add_column(name)
    for item in results:
        table.add_row(item["slug"], item["title"], f"{item['score']:.3f}")
    console.print(table)


@app.command("show-doc")
def show_doc_command(
    slug: str = typer.Argument(..., help="Document slug"),
    db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False, readable=True),
) -> None:
    with DocumentStore(db_path) as store:
        document = store.get_document(slug)
    if document is None:
        raise typer.Exit(code=1)
    console.print_json(data=document)


def main() -> None:
    app()


register_evolution_commands(app)
register_source_commands(app)

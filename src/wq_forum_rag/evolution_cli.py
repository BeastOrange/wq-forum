# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from wq_forum_rag.evolution import EvolutionService

DEFAULT_DB_PATH = Path(".cache/forum.sqlite3")
console = Console()


def register_evolution_commands(app: typer.Typer) -> None:
    @app.command("evolve-context")
    def context_command(
        query: str = typer.Argument(..., help="Question to build an evolution context for"),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
        top_k: int = typer.Option(5, "--top-k", min=1, max=20),
    ) -> None:
        console.print_json(
            data=EvolutionService(db_path).build_evolution_context(query=query, top_k=top_k)
        )

    @app.command("knowledge-search")
    def knowledge_search_command(
        query: str = typer.Argument(..., help="Search published knowledge pages"),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
        top_k: int = typer.Option(5, "--top-k", min=1, max=20),
        include_drafts: bool = typer.Option(False, "--include-drafts"),
        json_output: bool = typer.Option(False, "--json"),
    ) -> None:
        results = EvolutionService(db_path).search_knowledge(
            query=query,
            top_k=top_k,
            include_drafts=include_drafts,
        )
        if json_output:
            console.print_json(data={"query": query, "results": results})
            return
        table = Table(title=f"Knowledge Top {len(results)}")
        for name in ("slug", "title", "status", "confidence", "score"):
            table.add_column(name)
        for item in results:
            table.add_row(
                item["slug"],
                item["title"],
                item["status"],
                f"{item['confidence']:.2f}",
                f"{item['score']:.3f}",
            )
        console.print(table)

    @app.command("knowledge-show")
    def knowledge_show_command(
        slug: str = typer.Argument(..., help="Knowledge page slug"),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
    ) -> None:
        page = EvolutionService(db_path).get_knowledge_page(slug)
        if page is None:
            raise typer.Exit(code=1)
        console.print_json(data=page)

    @app.command("knowledge-lint")
    def knowledge_lint_command(
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
        slug: str | None = typer.Option(None, "--slug"),
    ) -> None:
        console.print_json(data=EvolutionService(db_path).lint_knowledge(slug=slug))

    @app.command("knowledge-graph")
    def knowledge_graph_command(
        slug: str = typer.Argument(..., help="Knowledge page slug"),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
        depth: int = typer.Option(1, "--depth", min=0, max=5),
        relation_type: str | None = typer.Option(None, "--relation"),
    ) -> None:
        console.print_json(
            data=EvolutionService(db_path).graph_query(
                slug,
                depth=depth,
                relation_type=relation_type,
            )
        )

    @app.command("knowledge-export")
    def knowledge_export_command(
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", exists=True, dir_okay=False),
        output_dir: Path = typer.Option(Path(".cache/wiki"), "--out", file_okay=False),
        include_drafts: bool = typer.Option(False, "--include-drafts"),
    ) -> None:
        console.print_json(
            data=EvolutionService(db_path).export_wiki(
                output_dir,
                include_drafts=include_drafts,
            )
        )

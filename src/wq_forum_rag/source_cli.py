from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from wq_forum_rag.manifest import SourceManifestService

DEFAULT_DB_PATH = Path(".cache/forum.sqlite3")
console = Console()


def register_source_commands(app: typer.Typer) -> None:
    @app.command("source-status")
    def source_status_command(
        source: Path = typer.Argument(..., exists=True, readable=True),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", dir_okay=False),
    ) -> None:
        console.print_json(data=SourceManifestService(db_path).source_status(source))

    @app.command("source-ingest-plan")
    def source_ingest_plan_command(
        source: Path = typer.Argument(..., exists=True, readable=True),
        db_path: Path = typer.Option(DEFAULT_DB_PATH, "--db", dir_okay=False),
        commit: bool = typer.Option(False, "--commit"),
    ) -> None:
        console.print_json(
            data=SourceManifestService(db_path).source_ingest_plan(source, commit=commit)
        )

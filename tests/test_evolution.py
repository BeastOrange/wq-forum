from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from wq_forum_rag.cli import app
from wq_forum_rag.mcp_server import (
    build_evolution_context,
    export_knowledge_wiki,
    get_knowledge_page,
    graph_query,
    lint_knowledge,
    propose_knowledge_page,
    search_knowledge,
)
from wq_forum_rag.evolution import EvolutionService


def _write_fixture(json_path: Path) -> None:
    payload = {
        "byCommunity": {
            "c1": {
                "title": "Alpha Lab",
                "topics": {
                    "t1": {
                        "id": "t1",
                        "author": "alice",
                        "commentNum": 0,
                        "datetime": "2026-04-28T13:00:00Z",
                        "postContent": "<p>Alpha decay should be tested with neutralization settings.</p>",
                        "title": "Alpha decay neutralization",
                        "url": "https://example.com/t1",
                        "voteNum": 10,
                    },
                    "t2": {
                        "id": "t2",
                        "author": "bob",
                        "commentNum": 0,
                        "datetime": "2026-04-28T13:10:00Z",
                        "postContent": "<p>Subindustry neutralization can reduce sector exposure.</p>",
                        "title": "Subindustry neutralization",
                        "url": "https://example.com/t2",
                        "voteNum": 8,
                    },
                },
            }
        }
    }
    json_path.write_text(json.dumps(payload), encoding="utf-8")


def _index_fixture(tmp_path: Path) -> Path:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    result = CliRunner().invoke(
        app,
        ["index", "--json", str(json_path), "--db", str(db_path), "--rebuild"],
    )
    assert result.exit_code == 0
    return db_path


def test_evolution_context_and_auto_publish_flow(tmp_path: Path) -> None:
    db_path = _index_fixture(tmp_path)

    context = build_evolution_context("neutralization decay", db=str(db_path), top_k=2)
    assert context["forum_evidence"]
    assert context["published_knowledge"] == []

    proposed = propose_knowledge_page(
        slug="alpha/neutralization-decay",
        title="Alpha decay and neutralization",
        summary="Alpha decay tests should be interpreted together with neutralization settings.",
        body=(
            "When a forum question combines alpha decay and neutralization, preserve the "
            "original decay setup and compare sector or subindustry neutralization evidence."
        ),
        source_topic_ids=["t1", "t2"],
        confidence=0.92,
        db=str(db_path),
    )

    assert proposed["auto_published"] is True
    assert proposed["page"]["status"] == "published"
    assert {item["topic_id"] for item in proposed["page"]["sources"]} == {"t1", "t2"}

    results = search_knowledge("sector neutralization decay", db=str(db_path), top_k=1)
    assert results["results"][0]["slug"] == "alpha/neutralization-decay"

    page = get_knowledge_page("alpha/neutralization-decay", db=str(db_path))
    assert page["page"]["title"] == "Alpha decay and neutralization"
    assert lint_knowledge(db=str(db_path), slug="alpha/neutralization-decay")["blocking_count"] == 0

    lint_result = CliRunner().invoke(
        app,
        ["knowledge-lint", "--db", str(db_path), "--slug", "alpha/neutralization-decay"],
    )
    assert lint_result.exit_code == 0
    assert '"blocking_count": 0' in lint_result.stdout

    search_result = CliRunner().invoke(
        app,
        ["knowledge-search", "decay", "--db", str(db_path), "--top-k", "1", "--json"],
    )
    assert search_result.exit_code == 0
    assert "alpha/neutralization-decay" in search_result.stdout


def test_low_confidence_or_conflict_stays_draft(tmp_path: Path) -> None:
    db_path = _index_fixture(tmp_path)

    low_confidence = propose_knowledge_page(
        slug="alpha/weak-note",
        title="Weak note",
        summary="This is a tentative neutralization note with limited confidence.",
        body="The evidence is still thin, so the page should stay in draft status.",
        source_topic_ids=["t1"],
        confidence=0.5,
        db=str(db_path),
    )
    assert low_confidence["auto_published"] is False
    assert low_confidence["page"]["status"] == "draft"

    conflict = propose_knowledge_page(
        slug="alpha/conflict-note",
        title="Conflict note",
        summary="This note intentionally carries a conflict relation for lint coverage.",
        body="A conflict relation should block automatic publishing until reviewed.",
        source_topic_ids=["t2"],
        confidence=0.95,
        links=[{"target_slug": "alpha/weak-note", "relation_type": "conflicts_with"}],
        db=str(db_path),
    )
    assert conflict["auto_published"] is False
    assert conflict["page"]["status"] == "draft"
    assert any(item["code"] == "conflict_link_present" for item in conflict["issues"])


def test_cli_evolve_context_and_show_commands(tmp_path: Path) -> None:
    db_path = _index_fixture(tmp_path)
    service = EvolutionService(db_path)
    service.propose_knowledge_page(
        slug="alpha/neutralization-guide",
        title="Neutralization guide",
        summary="Neutralization settings should be evaluated with alpha decay evidence.",
        body="Use original forum evidence when deciding whether subindustry neutralization fits.",
        source_topic_ids=["t1"],
        confidence=0.9,
    )

    runner = CliRunner()
    context = runner.invoke(
        app,
        ["evolve-context", "neutralization", "--db", str(db_path), "--top-k", "1"],
    )
    assert context.exit_code == 0
    assert "forum_evidence" in context.stdout

    show = runner.invoke(
        app,
        ["knowledge-show", "alpha/neutralization-guide", "--db", str(db_path)],
    )
    assert show.exit_code == 0
    assert "Neutralization guide" in show.stdout


def test_graph_query_and_wiki_export(tmp_path: Path) -> None:
    db_path = _index_fixture(tmp_path)
    service = EvolutionService(db_path)
    service.propose_knowledge_page(
        slug="alpha/neutralization-guide",
        title="Neutralization guide",
        summary="Neutralization settings should be evaluated with alpha decay evidence.",
        body="Use original forum evidence when deciding whether subindustry neutralization fits.",
        source_topic_ids=["t1"],
        confidence=0.9,
    )
    service.propose_knowledge_page(
        slug="alpha/decay-checklist",
        title="Decay checklist",
        summary="Decay checks should preserve original alpha context before comparison.",
        body="Compare decay behavior with cited neutralization evidence before publishing conclusions.",
        source_topic_ids=["t2"],
        confidence=0.91,
        links=[
            {
                "target_slug": "alpha/neutralization-guide",
                "relation_type": "refines",
                "weight": 1.2,
            }
        ],
    )

    graph = graph_query("alpha/decay-checklist", db=str(db_path), depth=1)
    assert {node["slug"] for node in graph["nodes"]} == {
        "alpha/decay-checklist",
        "alpha/neutralization-guide",
    }
    assert graph["edges"][0]["relation_type"] == "refines"

    output_dir = tmp_path / "wiki"
    exported = export_knowledge_wiki(db=str(db_path), output_dir=str(output_dir))
    assert exported["page_count"] == 2
    assert (output_dir / "index.md").exists()
    assert (output_dir / "log.md").exists()
    assert (output_dir / "hot.md").exists()

    page_text = (output_dir / "alpha" / "decay-checklist.md").read_text(encoding="utf-8")
    assert "status: published" in page_text
    assert "confidence: 0.910" in page_text
    assert "forum topic `t2`" in page_text
    assert "[[alpha/neutralization-guide]]" in page_text

    runner = CliRunner()
    cli_graph = runner.invoke(
        app,
        ["knowledge-graph", "alpha/decay-checklist", "--db", str(db_path), "--depth", "1"],
    )
    assert cli_graph.exit_code == 0
    assert "alpha/neutralization-guide" in cli_graph.stdout

    cli_export = runner.invoke(
        app,
        ["knowledge-export", "--db", str(db_path), "--out", str(tmp_path / "wiki-cli")],
    )
    assert cli_export.exit_code == 0
    assert "index.md" in cli_export.stdout

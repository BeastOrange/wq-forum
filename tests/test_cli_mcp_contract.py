# -*- coding: utf-8 -*-
# Author: konrad
# WQ_ID: OB53521
# Encoding: utf-8

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from typer.testing import CliRunner

from wq_forum_rag.cli import app
from wq_forum_rag.knowledge import KnowledgeStore
from wq_forum_rag.mcp_server import (
    find_by_exact,
    get_post,
    rebuild_search_index,
    related_posts,
    search_forum,
)


def _write_fixture(json_path: Path) -> None:
    payload = {
        "byCommunity": {
            "c1": {
                "id": "c1",
                "title": "Alpha Lab",
                "followers": 12,
                "posts": 2,
                "url": "https://example.com/community/c1",
                "topics": {
                    "t1": {
                        "id": "t1",
                        "author": "alice",
                        "commentNum": 3,
                        "datetime": "2026-04-28T13:00:00Z",
                        "postContent": "<p>Alpha decay and neutralization notes.</p>",
                        "title": "Alpha decay",
                        "url": "https://example.com/t1",
                        "voteNum": 10,
                    },
                    "t2": {
                        "id": "t2",
                        "author": "bob",
                        "commentNum": 1,
                        "comments": {
                            "c2": {
                                "id": "c2",
                                "author": "carol",
                                "commentContent": "<p>Use subindustry neutralization for this setup.</p>",
                                "commentTimeDatetime": "2026-04-28T13:20:00Z",
                                "voteNum": 1,
                            }
                        },
                        "datetime": "2026-04-28T13:10:00Z",
                        "postContent": "<p>Portfolio neutralization checklist.</p>",
                        "title": "Neutralization checklist",
                        "url": "https://example.com/t2",
                        "voteNum": 8,
                    },
                },
            }
        }
    }
    json_path.write_text(json.dumps(payload), encoding="utf-8")


def _write_fixture_only_t1(json_path: Path) -> None:
    payload = {
        "byCommunity": {
            "c1": {
                "id": "c1",
                "title": "Alpha Lab",
                "followers": 12,
                "posts": 1,
                "url": "https://example.com/community/c1",
                "topics": {
                    "t1": {
                        "id": "t1",
                        "author": "alice",
                        "commentNum": 3,
                        "datetime": "2026-04-28T13:00:00Z",
                        "postContent": "<p>Alpha decay and neutralization notes.</p>",
                        "title": "Alpha decay",
                        "url": "https://example.com/t1",
                        "voteNum": 10,
                    },
                },
            }
        }
    }
    json_path.write_text(json.dumps(payload), encoding="utf-8")


def test_cli_contract_end_to_end(tmp_path: Path) -> None:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    runner = CliRunner()

    index_result = runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path), "--rebuild"])
    assert index_result.exit_code == 0
    assert '"indexed_topics": 2' in index_result.stdout

    unchanged_result = runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path)])
    assert unchanged_result.exit_code == 0
    assert '"status": "unchanged"' in unchanged_result.stdout

    search_result = runner.invoke(app, ["search", "neutralization", "--db", str(db_path), "--top-k", "2"])
    assert search_result.exit_code == 0
    assert "Neutralization checklist" in search_result.stdout

    reindex_result = runner.invoke(app, ["search-reindex", "--db", str(db_path)])
    assert reindex_result.exit_code == 0
    assert '"fts_available": true' in reindex_result.stdout

    show_result = runner.invoke(app, ["show", "t1", "--db", str(db_path)])
    assert show_result.exit_code == 0
    assert '"topic_id": "t1"' in show_result.stdout


def test_mcp_tool_contract_without_client(tmp_path: Path) -> None:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    runner = CliRunner()
    runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path), "--rebuild"])

    search_payload = search_forum("alpha", db=str(db_path), top_k=3)
    assert search_payload["query"] == "alpha"
    assert search_payload["results"][0]["topic_id"] == "t1"

    post_payload = get_post("t1", db=str(db_path))
    assert post_payload["post"]["title"] == "Alpha decay"

    exact_payload = find_by_exact("subindustry neutralization", db=str(db_path))
    assert exact_payload["results"][0]["topic_id"] == "t2"

    community_payload = find_by_exact(
        "neutralization",
        db=str(db_path),
        community="Alpha Lab",
        top_k=2,
    )
    assert {item["topic_id"] for item in community_payload["results"]} <= {"t1", "t2"}

    related_payload = related_posts("t1", db=str(db_path), top_k=2)
    assert related_payload["topic_id"] == "t1"
    assert len(related_payload["results"]) <= 2

    reindex_payload = rebuild_search_index(db=str(db_path))
    assert reindex_payload["fts_available"] is True


def test_refresh_command_prunes_orphans_and_commits_manifest(tmp_path: Path) -> None:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    runner = CliRunner()

    initial = runner.invoke(app, ["refresh", str(json_path), "--db", str(db_path), "--rebuild"])
    assert initial.exit_code == 0
    initial_payload = json.loads(initial.stdout)
    assert initial_payload["index"]["indexed_topics"] == 2
    assert initial_payload["manifest"]["committed"] is True

    _write_fixture_only_t1(json_path)
    refresh_result = runner.invoke(app, ["refresh", str(json_path), "--db", str(db_path)])
    assert refresh_result.exit_code == 0
    refresh_payload = json.loads(refresh_result.stdout)
    assert refresh_payload["index"]["indexed_topics"] == 1
    assert refresh_payload["index"]["pruned"] == 1
    assert refresh_payload["index"]["protected_orphans"] == []

    conn = sqlite3.connect(db_path)
    try:
        topic_ids = {row[0] for row in conn.execute("SELECT topic_id FROM topics").fetchall()}
        chunk_topic_ids = {row[0] for row in conn.execute("SELECT DISTINCT topic_id FROM chunks").fetchall()}
    finally:
        conn.close()
    assert topic_ids == {"t1"}
    assert chunk_topic_ids == {"t1"}


def test_index_no_prune_keeps_orphans(tmp_path: Path) -> None:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    runner = CliRunner()
    runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path), "--rebuild"])

    _write_fixture_only_t1(json_path)
    result = runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path), "--no-prune"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["pruned"] == 0

    conn = sqlite3.connect(db_path)
    try:
        topic_ids = {row[0] for row in conn.execute("SELECT topic_id FROM topics").fetchall()}
    finally:
        conn.close()
    assert topic_ids == {"t1", "t2"}


def test_index_prune_protects_topics_referenced_by_knowledge_pages(tmp_path: Path) -> None:
    json_path = tmp_path / "forum.json"
    db_path = tmp_path / "forum.sqlite3"
    _write_fixture(json_path)
    runner = CliRunner()
    runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path), "--rebuild"])

    with KnowledgeStore(db_path) as kstore:
        with kstore.conn:
            kstore.conn.execute(
                """
                INSERT INTO knowledge_pages(slug, title, summary, body, status, confidence,
                    content_hash, created_at, updated_at)
                VALUES ('alpha-decay', 'Alpha Decay', 'summary', 'body', 'published', 0.9,
                    'hash', '2026-04-28T13:00:00Z', '2026-04-28T13:00:00Z')
                """
            )
            kstore.conn.execute(
                """
                INSERT INTO knowledge_sources(slug, topic_id, evidence_note)
                VALUES ('alpha-decay', 't2', 'cited')
                """
            )

    _write_fixture_only_t1(json_path)
    result = runner.invoke(app, ["index", "--json", str(json_path), "--db", str(db_path)])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["pruned"] == 0
    assert payload["protected_orphans"] == ["t2"]

    conn = sqlite3.connect(db_path)
    try:
        topic_ids = {row[0] for row in conn.execute("SELECT topic_id FROM topics").fetchall()}
    finally:
        conn.close()
    assert topic_ids == {"t1", "t2"}

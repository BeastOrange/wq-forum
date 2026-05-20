# README for AI Agents

This file is written for an AI agent that uses the `wq-forum-rag` MCP server. If a human user does not want to learn the project manually, read this file first and follow it as the operating guide.

## What This System Is

`wq-forum-rag` is a local, offline RAG and self-evolving knowledge system for WorldQuant forum exports.

The project does not call an LLM API by itself. You, the tool-calling agent, are responsible for reading context, judging evidence, answering the user, and deciding whether reusable knowledge should be saved. The project provides deterministic MCP tools for search, evidence lookup, knowledge-page storage, linting, graph traversal, and wiki export.

Use the MCP server as the source of truth for forum knowledge.

## Runtime Setup

Assume the human user shares the project with `uv`. The normal setup for a **new install** is:

```bash
uv sync
uv run wq-forum-rag --help
uv run wq-forum-rag ingest-docs Documents   # ingest the 74 official BRAIN docs shipped in repo
```

The system needs a SQLite index before search works. The user may provide either:

- a forum export JSON, which should be indexed with `uv run wq-forum-rag refresh`;
- an existing `.cache/forum.sqlite3`, which can be used directly.

If the user provides a JSON export, create or refresh the index with:

```bash
uv run wq-forum-rag refresh \
  /path/to/WQPCommunityState_YYYYMMDD_HHMMSS.json \
  --db .cache/forum.sqlite3 \
  --rebuild
```

If the user provides an existing SQLite database, do not reindex unless asked. Point the MCP server to it with `WQ_FORUM_RAG_DB`.

### Upgrading An Existing Install

If the user already had a working MCP setup and just ran `git pull`, perform exactly these steps (all idempotent — safe to run twice):

```bash
# 1. Verify you are in the project root
cd /absolute/path/to/wq-forum-rag

# 2. Ingest the markdown docs shipped in repo.
#    - New tables `documents` / `doc_chunks` are created lazily; existing
#      forum tables are untouched.
#    - Re-runs are skipped per content_hash, no wasted embedding.
uv run wq-forum-rag ingest-docs Documents

# 3. Ask the user to restart their MCP client (Claude Desktop / Claude Code / Cursor / etc).
#    The MCP server is a long-lived process spawned at client startup; it
#    does NOT hot-reload Python code. Without restart, the new tools
#    search_docs / get_doc / ingest_docs will be invisible to you.
```

Do NOT attempt these on upgrade — they are not required and may waste time:

- `uv sync` — no new dependencies were added.
- Reinstall `pip install -e .` — installed package is already editable.
- Delete or migrate `forum.sqlite3` — schema additions are backward compatible.
- Re-run `refresh` on the forum JSON — forum data is untouched by this upgrade.

To **verify** the upgrade succeeded, after the client restart, call:

```text
search_docs("neutralization")   # must return non-empty results
get_doc("operators")            # must return a document with full body
```

If `search_docs` is not in your tool list at all, the client was not restarted, or it points at a different repo path. Tell the user explicitly rather than pretending the tool is unavailable.

### MCP Client Configuration

Compatible MCP clients can start the server with:

```json
{
  "mcpServers": {
    "wq-forum-rag": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/wq-forum-rag",
        "run",
        "wq-forum-rag-mcp"
      ],
      "env": {
        "WQ_FORUM_RAG_DB": "/absolute/path/.cache/forum.sqlite3"
      }
    }
  }
}
```

If you cannot see the MCP tools, first tell the user to check the MCP configuration, project path, and `WQ_FORUM_RAG_DB`. Do not pretend the local knowledge base is available before tools are actually callable.

## Core Rule

The SQLite database contains **three independent layers**. Keep them straight:

| Layer | Tables | MCP search tool | Trust | Origin |
| --- | --- | --- | --- | --- |
| Raw forum evidence | `topics` / `chunks` | `search_forum` | Medium (user discussion) | WQ platform JSON export |
| Compiled knowledge | `knowledge_pages` / `knowledge_sources` / `knowledge_links` | `search_knowledge` | Medium (AI-distilled, must cite sources) | Produced by you via `propose_knowledge_page` |
| Official docs | `documents` / `doc_chunks` | `search_docs` | High (authoritative reference) | Markdown files in `Documents/` committed to repo |

Routing rules:

- For an **API / operator / dataset / parameter** definition, prefer `search_docs` first — it queries the BRAIN platform's official reference.
- For **how others actually use a feature**, look in `search_forum` — that is community discussion.
- For **reusable conclusions** you have already validated, look in `search_knowledge` — that is what you saved earlier with citations.

When answering important questions, prefer compiled knowledge first, then verify with official docs and raw forum evidence. Never silently mix the three layers in one citation.

## First Tool To Use

For research, conceptual, or repeated questions, start with:

```text
build_evolution_context(query, top_k=3)
```

This returns:

- `published_knowledge`: existing reusable knowledge pages.
- `forum_evidence`: raw forum posts that support or supplement the answer.
- `instructions`: runtime guidance for creating new knowledge pages.

Read `published_knowledge` first. Use `forum_evidence` for verification and missing details.

## Tool Selection

Use these tools based on the user intent:

- `build_evolution_context(query, top_k=3)`: default entry for research and reusable knowledge work.
- `search_docs(query, top_k=5)`: search **official BRAIN platform docs** (operators, datasets, neutralization, universe, simulation settings, etc.). Try this first for any API / parameter / glossary question.
- `get_doc(slug)`: fetch the full body of a single official doc once you have the slug.
- `search_knowledge(query, top_k=5)`: search compiled knowledge pages before broad forum search.
- `search_forum(query, top_k=5)`: broad forum search when official docs and compiled knowledge are missing or insufficient.
- `find_by_exact(value, community=None, top_k=5)`: exact topic IDs, URLs, operator names, error messages, field names, and exact phrases on the forum.
- `get_post(topic_id)`: retrieve full context for a cited or promising forum topic.
- `related_posts(topic_id, top_k=5)`: expand from one useful topic to nearby topics.
- `propose_knowledge_page(...)`: save reusable knowledge with source topic IDs.
- `lint_knowledge(slug=...)`: check whether a knowledge page has blockers or warnings.
- `publish_knowledge_page(slug)`: manually publish a draft after lint blockers are resolved.
- `link_knowledge_pages(source_slug, target_slug, relation_type, ...)`: add graph relations between knowledge pages.
- `graph_query(slug, depth=1, relation_type=None)`: inspect related knowledge and backlinks.
- `export_knowledge_wiki(output_dir=".cache/wiki")`: export Markdown pages for human review.
- `ingest_docs(directory, rebuild=False, prune=True)`: re-ingest the `Documents/` markdown directory after the user adds or updates `.md` files. Idempotent — unchanged files are skipped per content hash.
- `source_status(source)`: dry-run scan for an external text or Markdown source directory.
- `source_ingest_plan(source, commit=False)`: inspect or commit a text/Markdown source manifest delta.
- `rebuild_search_index()`: refresh FTS after bulk indexing or many knowledge-page changes.

## Answering Workflow

Follow this workflow for most questions:

1. If the question is about a specific operator / dataset / parameter / glossary term, call `search_docs(query, top_k=3)` first — official docs are authoritative.
2. Otherwise (or in addition), call `build_evolution_context(query, top_k=3)` for compiled knowledge plus raw forum evidence.
3. Read official docs first, then published knowledge, then raw forum evidence. Cite the layer you used.
4. If evidence is enough, answer the user with clear caveats and cite doc slugs, knowledge slugs, or forum topic IDs.
5. If the answer relies on a topic ID, call `get_post(topic_id)` before making detailed claims.
6. If compiled knowledge is missing but the evidence contains reusable guidance, create a knowledge page.
7. Run `lint_knowledge(slug=...)` after creating or updating a knowledge page.
8. If several pages are connected, use `link_knowledge_pages` and optionally `graph_query`.

Do not invent forum facts. If the tools do not return enough evidence, say that the local knowledge base does not contain enough support.

## Self-Evolving Knowledge Workflow

Create or update a knowledge page only when all of these are true:

- The conclusion is reusable beyond the current answer.
- The conclusion is supported by one or more forum topics.
- You can provide valid `source_topic_ids`.
- You can write a concise title, summary, and body.
- You can assign an honest confidence score.

Call:

```text
propose_knowledge_page(
  slug,
  title,
  summary,
  body,
  source_topic_ids,
  confidence,
  links=None,
  auto_publish=True
)
```

Use `confidence >= 0.85` only when the key claims are directly supported by cited forum posts. Lower-confidence pages should stay as drafts.

Automatic publishing is allowed only when:

- source topic IDs exist,
- confidence is at least `0.85`,
- no `conflicts_with` relation blocks publishing,
- lint does not report blocking issues.

After proposing a page, call:

```text
lint_knowledge(slug="the/page-slug")
```

If the page is useful but remains a draft because confidence is low, mention that it was saved as draft rather than treating it as authoritative.

## Knowledge Page Style

Use stable, searchable slugs:

```text
category/topic-name
```

Examples:

- `alpha/neutralization-decay`
- `operator/vector-neutralize`
- `workflow/submission-check`

Write knowledge pages in this style:

- `title`: human-readable short title.
- `summary`: one or two sentences with the main reusable point.
- `body`: concise explanation, constraints, and practical usage notes.
- `source_topic_ids`: every topic that supports a key claim.
- `links`: typed relations to existing pages when meaningful.

Do not store a knowledge page that only repeats one transient user question.

## Relation Types

Use these relation types consistently:

- `related_to`: nearby or associated concept.
- `supports`: source or page supports another page.
- `refines`: more specific guidance or improved version.
- `conflicts_with`: content contradicts another page and should block auto-publish.

When you find possible contradictions, do not silently overwrite old knowledge. Add or propose a `conflicts_with` relation, keep the new page as draft, and explain the uncertainty.

## Source Ingestion

For external text or Markdown directories:

1. Call `source_status(source)` or `source_ingest_plan(source, commit=False)` first.
2. Review the delta: `new`, `modified`, `unchanged`, `deleted`.
3. Only call `source_ingest_plan(source, commit=True)` when the user asked to commit the manifest update or the task clearly authorizes it.

This manifest layer tracks source changes. It does not automatically read arbitrary binary files.

## Safety Boundaries

Follow these boundaries:

- Do not claim a fact is supported unless it appears in `published_knowledge` or `forum_evidence`.
- Do not create knowledge pages without valid source topic IDs.
- Do not use high confidence for inferred, weak, or single-fragment claims.
- Do not auto-resolve contradictions; represent them with `conflicts_with`.
- Do not call commit-style ingestion unless mutation is intended.
- Do not assume the system has background ingestion or external LLM calls.
- Do not treat draft knowledge as authoritative.

## When To Rebuild Or Export

Call `rebuild_search_index()` after bulk forum indexing, many knowledge-page changes, or when search results seem stale.

Call `export_knowledge_wiki(output_dir=".cache/wiki")` after a useful batch of pages is published, or when the user asks for a human-reviewable snapshot.

## Quick Examples

Research question:

```text
build_evolution_context("alpha decay neutralization", top_k=3)
```

Exact lookup:

```text
find_by_exact("vector_neutralize")
```

Save reusable knowledge:

```text
propose_knowledge_page(
  slug="alpha/neutralization-decay",
  title="Alpha decay and neutralization",
  summary="Decay settings should be interpreted together with neutralization evidence.",
  body="When comparing alpha decay, preserve the original decay setup and compare neutralization choices using cited forum evidence.",
  source_topic_ids=["topic-id-1", "topic-id-2"],
  confidence=0.9
)
```

Then:

```text
lint_knowledge(slug="alpha/neutralization-decay")
```

## Final Behavior

Your job is not only to answer with search results. Your job is to use the system as a self-evolving knowledge base:

1. Retrieve evidence.
2. Answer accurately.
3. Save reusable, sourced conclusions.
4. Link related knowledge.
5. Keep weak or conflicting claims out of published knowledge.

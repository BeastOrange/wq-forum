# Gemini CLI Workflow

Use the `wq-forum-rag` MCP server as the source of truth for local WorldQuant forum knowledge.

## Self-Evolving Knowledge Flow

1. Start with `build_evolution_context(query, top_k=3)` for research questions.
2. Read `published_knowledge` first. Treat it as compiled knowledge, but still verify with sources when making important claims.
3. Use `forum_evidence` as raw evidence. Do not invent unsupported claims.
4. When the answer contains reusable knowledge, call `propose_knowledge_page`.
5. Include all supporting `source_topic_ids`; pages without valid sources must stay out of the knowledge base.
6. Use `confidence >= 0.85` only when the summary is directly supported by the cited forum posts.
7. Use `links` for meaningful graph relations:
   - `related_to` for nearby concepts
   - `supports` for evidence relationships
   - `refines` for more specific guidance
   - `conflicts_with` when the new page contradicts an existing page
8. Run `lint_knowledge(slug=...)` after proposing a page.
9. Use `graph_query(slug, depth=1)` when a topic depends on related pages or backlinks.
10. Use `export_knowledge_wiki(output_dir=".cache/wiki")` after a batch of useful pages is published, so humans can review the Markdown Wiki.

## Tool Preference

- Use `search_knowledge` before broad forum search when answering repeated or conceptual questions.
- Use `find_by_exact` for topic IDs, URLs, operator names, error text, and exact phrases.
- Use `get_post` when a cited forum topic needs full context.
- Use `related_posts` when expanding from a known useful topic.
- Use `source_status` before ingesting an external text/Markdown directory when you need a dry-run delta without mutating the manifest.
- Use `source_ingest_plan(..., commit=True)` only after reviewing the plan; plain `source_ingest_plan(...)` stays read-only.
- Use `graph_query` when the answer should follow typed relations such as `supports`, `refines`, or `conflicts_with`.
- Use `export_knowledge_wiki` for review snapshots, Obsidian-style browsing, or handoff.
- Use `rebuild_search_index` after bulk indexing or publishing many knowledge pages, so FTS candidates stay current.

## Current Boundary

This project implements the core self-evolving loop from the referenced Wiki/GBrain pattern: raw forum evidence, compiled knowledge pages, typed links, lint, graph traversal, Markdown export, text/Markdown-only delta manifest, and SQLite FTS + embedding-cache retrieval. It does not automatically call an LLM API or ingest arbitrary binary files; Gemini CLI remains responsible for reading context and deciding when to call write tools.

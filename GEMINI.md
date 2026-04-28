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

## Tool Preference

- Use `search_knowledge` before broad forum search when answering repeated or conceptual questions.
- Use `find_by_exact` for topic IDs, URLs, operator names, error text, and exact phrases.
- Use `get_post` when a cited forum topic needs full context.
- Use `related_posts` when expanding from a known useful topic.

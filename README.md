# wq-forum-rag

`wq-forum-rag` 用于把 `WQPCommunityState_20260428_133740.json` 这类论坛导出文件做成本地离线、轻量、可增量更新的检索层，并同时暴露 CLI 和 MCP 工具。

当前版本刻意保持轻依赖：

- 解析：`beautifulsoup4`
- CLI：`typer` + `rich`
- MCP：`mcp`
- 可选本地向量能力：`fastembed`（extra `local-embeddings`）

## 安装

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

如需后续接本地 embedding：

```bash
pip install -e ".[local-embeddings]"
```

## 离线索引

首次建立索引：

```bash
wq-forum-rag index \
  --json WQPCommunityState_20260428_133740.json \
  --db .cache/forum.sqlite3 \
  --rebuild
```

默认实现会从 JSON 中抽取：

- community id / title
- topic id / title / url
- author / datetime
- vote / comment 等轻量元数据
- HTML 清洗后的正文文本

索引落到 SQLite，检索阶段复用仓库内现有 `search.py` 做本地 hybrid search（lexical + dense fallback），不依赖外部服务。

## 增量索引

再次执行：

```bash
wq-forum-rag index \
  --json WQPCommunityState_20260428_133740.json \
  --db .cache/forum.sqlite3
```

如果源 JSON 的路径、mtime、size 都未变化，命令会直接跳过重建并返回 `unchanged`。当你替换导出文件或希望强制刷新时，加 `--rebuild`。

## 查询

全文检索：

```bash
wq-forum-rag search "alpha decay neutralization" --db .cache/forum.sqlite3 --top-k 5
```

查看单帖：

```bash
wq-forum-rag show 12913566170391 --db .cache/forum.sqlite3
```

## MCP 用法

服务端默认从 `WQ_FORUM_RAG_DB` 读取索引路径，也允许每次调用工具时显式传 `db`。

```bash
export WQ_FORUM_RAG_DB=/absolute/path/.cache/forum.sqlite3
wq-forum-rag-mcp
```

Claude Desktop / 兼容 MCP 客户端配置示例：

```json
{
  "mcpServers": {
    "wq-forum-rag": {
      "command": "wq-forum-rag-mcp",
      "env": {
        "WQ_FORUM_RAG_DB": "/absolute/path/.cache/forum.sqlite3"
      }
    }
  }
}
```

已暴露工具：

- `search_forum(query, db=None, top_k=5)`
- `get_post(topic_id, db=None)`
- `find_by_exact(value, db=None, community=None, top_k=5)`
- `related_posts(topic_id, db=None, top_k=5)`
- `build_evolution_context(query, db=None, top_k=5)`
- `propose_knowledge_page(slug, title, summary, body, source_topic_ids, confidence, db=None, links=None, auto_publish=True)`
- `search_knowledge(query, db=None, top_k=5, include_drafts=False)`
- `get_knowledge_page(slug, db=None)`
- `link_knowledge_pages(source_slug, target_slug, relation_type, db=None, weight=1.0, confidence=0.8)`
- `lint_knowledge(db=None, slug=None)`
- `publish_knowledge_page(slug, db=None)`

## 自进化知识层

当前版本在原始论坛 RAG 之上新增了一层可沉淀的知识库，目标是让 Gemini CLI、Codex 或其他 MCP 客户端把高价值查询结果整理成可复用知识，而不是每次都重新从论坛 chunk 临场拼答案。

推荐流程：

1. 调用 `build_evolution_context("你的问题")`，系统会返回已发布知识页和完整论坛证据。
2. 由 Gemini CLI 阅读上下文并总结稳定结论。
3. 调用 `propose_knowledge_page(...)` 写入知识页草稿，必须提供支撑结论的 `source_topic_ids`。
4. 系统会按低风险规则自动发布：`confidence >= 0.85`、来源 topic 存在、没有 `conflicts_with` 阻塞项。
5. 后续查询优先使用 `search_knowledge(...)` 命中已沉淀知识，再回落到论坛检索。

知识层仍然写入同一个 SQLite 文件，新增表包括：

- `knowledge_pages`：概念、规则、经验等沉淀页面
- `knowledge_sources`：知识页到论坛原帖的来源绑定
- `knowledge_links`：知识页之间的 typed edges / backlink
- `knowledge_events`：append-only 演化日志

这套设计刻意不内置外部 LLM API。LLM 的阅读、总结和判断由 MCP 客户端完成；本项目只负责确定性存储、来源校验、低风险自动发布、图谱连边和 lint。

对应 CLI 也提供了本地检查入口：

```bash
wq-forum-rag evolve-context "alpha decay neutralization" --db .cache/forum.sqlite3 --top-k 3
wq-forum-rag knowledge-search "neutralization" --db .cache/forum.sqlite3 --json
wq-forum-rag knowledge-show alpha/neutralization-decay --db .cache/forum.sqlite3
wq-forum-rag knowledge-lint --db .cache/forum.sqlite3
```

## 精度 / 性能策略

当前策略优先“本地可跑 + 低维护成本”：

1. 默认检索复用现有 `ForumSearcher`，即 lexical 候选召回 + deterministic dense rerank fallback；不开外部模型也能离线跑。
2. 数据持久化仍是 SQLite，适合本地单文件分发、增量更新和精确查找。
3. `find_by_exact` 走 `topic_id / url / title / 正文 / 评论 / chunk` 精确词命中，避免把字段名、报错、operator 等导航型问题交给语义检索。
4. `related_posts` 复用标题检索做近邻召回，优先返回同社区相关主题。
5. 自进化知识层采用“知识页优先 + 论坛证据回退”的渐进式披露；知识页搜索会叠加轻量 backlink boost。

如果后续要提高语义召回，可以保留当前 SQLite 作为元数据与精确查找层，再用 `.[local-embeddings]` 接入 `fastembed` 替换默认 dense backend，做更强的混合召回或 rerank。这样不会破坏现有 CLI/MCP contract。

## 与后续 parser/storage/search 集成

当前骨架已经直接复用项目内 `parser` / `storage` / `search`。后续即使替换 embedding backend 或调优 chunk/search 策略，也不需要改 CLI/MCP 对外接口。

# wq-forum-rag

`wq-forum-rag` 用于把 `WQPCommunityState_20260428_133740.json` 这类论坛导出文件做成本地离线、轻量、可增量更新的检索层，并同时暴露 CLI 和 MCP 工具。

如果你希望直接让 AI Agent 使用本项目，而不是自己阅读全部细节，请把 [`README_AGENT.md`](README_AGENT.md) 作为 Agent 的首要操作手册。

当前版本刻意保持轻依赖：

- 解析：`beautifulsoup4`
- CLI：`typer` + `rich`
- MCP：`mcp`
- 可选本地向量能力：`fastembed`（extra `local-embeddings`）

## 分享给别人时需要什么

仓库内有 **3 类数据**，分发方式不同：

| 数据 | 体积 | 来源 | 是否在 repo 里 | 别人怎么拿到 |
| --- | --- | --- | --- | --- |
| 代码 / 测试 / `pyproject.toml` | 小 | 本仓库 | ✅ git | `git clone` |
| **`Documents/` 官方文档(74 篇 .md)** | 468KB | 自己整理 | ✅ git | `git clone` 后跑 `ingest-docs` |
| 论坛 SQLite (`.cache/forum.sqlite3`, ~438MB) | 大 | WQ 平台导出的 JSON 解析而来 | ❌ `.gitignore` | 由用户自己用自己的 WQ 帐号导 JSON 再 `refresh` |

因此最小交付物 = **本仓库源码 + 用户自己的论坛 JSON**。`Documents/` 部分对所有 clone 用户都是开箱即用，不需要外部依赖。

如果你愿意把已经构建好的 SQLite 私下分享(注意 WQ ToS 风险)，对方可以跳过"离线索引"步骤，只需要把 MCP 配置里的 `WQ_FORUM_RAG_DB` 指到该文件。

## 快速开始(全新安装)

```bash
git clone <repo-url>
cd wq-forum-rag
uv sync
uv run wq-forum-rag --help
```

项目要求 Python `>=3.11`。如果本机没有合适版本，可以先执行：

```bash
uv python install 3.11
uv sync
```

如需后续接本地 embedding：

```bash
uv sync --extra local-embeddings
```

**入库官方文档**(必跑，否则 `search_docs` 返回空)：

```bash
uv run wq-forum-rag ingest-docs Documents
```

如果你还有自己的论坛 JSON，再入论坛：

```bash
uv run wq-forum-rag refresh /path/to/WQPCommunityState_YYYYMMDD_HHMMSS.json
```

至此 SQLite 内同时包含官方文档与论坛帖，MCP 工具全部可用。

## 升级已有安装(老用户拉新代码)

老用户的 MCP 已经配过，**升级只需要 3 步**(都是幂等的，多跑无害)：

```bash
# 1. 拉新代码
cd /path/to/wq-forum-rag
git pull

# 2. 把官方文档增量入库
#    - 新表 documents / doc_chunks 由 CREATE TABLE IF NOT EXISTS 懒创建
#    - 已有 forum 数据完全不动
#    - 同名文档按 content_hash 跳过，未改动的不会重复 embed
uv run wq-forum-rag ingest-docs Documents

# 3. 重启 MCP 客户端(Claude Desktop / Claude Code / Cursor 等)
#    - MCP server 是常驻进程，启动时加载代码，不会热重载
#    - 重启后新工具 search_docs / get_doc / ingest_docs 才会出现在工具列表里
```

**不需要做的事**：

- ❌ `uv sync` —— 没新增依赖
- ❌ `pip install -e .` —— 已经是 editable 安装，源码改动自动生效
- ❌ 删 / 迁移 `forum.sqlite3` —— 老表完全兼容，新表 additive
- ❌ 重跑 `refresh` —— 论坛部分零影响

**校验升级成功的方法**：

```bash
# 应看到 indexed_documents=74, doc_chunks>=228
uv run wq-forum-rag ingest-docs Documents

# 重启 MCP 客户端后，在客户端里调一次：
#   search_docs("neutralization")  → 应返回非空命中
#   get_doc("operators")           → 应返回完整 markdown body
```

如果新工具仍然不可见，99% 是 MCP 客户端没重启，少数情况检查 `command` / `args` 路径有没有指错 repo。

## 离线索引

首次建立索引：

```bash
uv run wq-forum-rag index \
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
uv run wq-forum-rag index \
  --json WQPCommunityState_20260428_133740.json \
  --db .cache/forum.sqlite3
```

如果源 JSON 的路径、mtime、size 都未变化，命令会直接跳过重建并返回 `unchanged`。当你替换导出文件或希望强制刷新时，加 `--rebuild`。

## 查询

全文检索：

```bash
uv run wq-forum-rag search "alpha decay neutralization" --db .cache/forum.sqlite3 --top-k 5
```

查看单帖：

```bash
uv run wq-forum-rag show 12913566170391 --db .cache/forum.sqlite3
```

## 官方文档库 (Documents/)

`Documents/` 目录是从 BRAIN 平台整理的 74 篇官方文档(Operators / Neutralization / 各种 Dataset 用法等)，作为论坛之外的高信任度知识源，已直接 commit 进仓库，对所有 clone 用户开箱即用。

入库 / 增量更新：

```bash
uv run wq-forum-rag ingest-docs Documents
# 选项：
#   --rebuild       强制全清重建
#   --no-prune      保留 DB 中已不存在于目录的文档(默认 prune)
```

搜索与查看：

```bash
uv run wq-forum-rag search-docs "subindustry neutralization" --top-k 5
uv run wq-forum-rag show-doc operators
```

设计上文档与论坛**完全隔离**：

- 文档走 `documents` / `doc_chunks` 表，FTS kind = `doc_chunk`
- 论坛走 `topics` / `chunks` 表，FTS kind = `forum_chunk`
- MCP 端 `search_docs` 只命中文档，`search_forum` 只命中论坛
- 两者共享同一个 SQLite 文件、同一个 embedding cache，互不污染

## MCP 用法

服务端默认从 `WQ_FORUM_RAG_DB` 读取索引路径，也允许每次调用工具时显式传 `db`。

```bash
export WQ_FORUM_RAG_DB=/absolute/path/.cache/forum.sqlite3
uv run wq-forum-rag-mcp
```

Claude Desktop / 兼容 MCP 客户端配置示例：

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

已暴露工具(共 19 个)：

论坛检索：

- `search_forum(query, db=None, top_k=5)`
- `get_post(topic_id, db=None)`
- `find_by_exact(value, db=None, community=None, top_k=5)`
- `related_posts(topic_id, db=None, top_k=5)`

官方文档检索：

- `search_docs(query, db=None, top_k=5)`
- `get_doc(slug, db=None)`
- `ingest_docs(directory, db=None, rebuild=False, prune=True)`

来源管理：

- `source_status(source, db=None)`
- `source_ingest_plan(source, db=None, commit=False)`

知识层(self-evolving)：

- `build_evolution_context(query, db=None, top_k=5)`
- `propose_knowledge_page(slug, title, summary, body, source_topic_ids, confidence, db=None, links=None, auto_publish=True)`
- `search_knowledge(query, db=None, top_k=5, include_drafts=False)`
- `get_knowledge_page(slug, db=None)`
- `link_knowledge_pages(source_slug, target_slug, relation_type, db=None, weight=1.0, confidence=0.8)`
- `lint_knowledge(db=None, slug=None)`
- `publish_knowledge_page(slug, db=None)`
- `graph_query(slug, db=None, depth=1, relation_type=None)`
- `export_knowledge_wiki(db=None, output_dir=".cache/wiki", include_drafts=False)`

维护：

- `rebuild_search_index(db=None)`

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

当前已实现的 PDF 对齐能力：

- Raw layer：论坛 JSON 解析、SQLite 原帖与 chunk 索引。
- Wiki layer：可沉淀的知识页、来源绑定、Markdown Wiki 导出。
- Schema / operation layer：MCP 工具约束 Gemini CLI 的 ingest、query、lint、publish 流程。
- Progressive disclosure：优先返回已发布知识页，再返回完整论坛证据。
- Typed graph：`knowledge_links` 记录 typed edges，支持 backlink boost 和 `graph_query` 多跳遍历。
- Hot / log / index：`export_knowledge_wiki` 生成 `index.md`、`log.md`、`hot.md` 和页面 Markdown。
- Delta manifest：`source_status` / `source_ingest_plan` 可扫描外部文本/Markdown 目录，记录 `sha256`、`mtime_ns`、`size`、`relative_path`，并区分 `new/modified/unchanged/deleted`；默认 dry-run，只有显式 `commit=True` 才会更新 manifest 表。
- SQLite 混合检索增强：`search-reindex` / `rebuild_search_index` 重建 FTS5 索引，搜索时先用 FTS 候选召回，再复用原 hybrid rerank；embedding 结果按 backend 和内容 hash 持久化缓存。

尚未实现或后续可继续增强：

- PDF/截图/音频/视频等多模态摄入。
- 定时任务或后台 always-on ingestion。
- LLM 自动矛盾识别；当前只支持客户端提交 `conflicts_with` 后由系统阻止自动发布。
- 外部向量数据库或 seekdb 类服务化基础设施；当前已实现 SQLite 本地增强版。

对应 CLI 也提供了本地检查入口：

```bash
uv run wq-forum-rag evolve-context "alpha decay neutralization" --db .cache/forum.sqlite3 --top-k 3
uv run wq-forum-rag knowledge-search "neutralization" --db .cache/forum.sqlite3 --json
uv run wq-forum-rag knowledge-show alpha/neutralization-decay --db .cache/forum.sqlite3
uv run wq-forum-rag knowledge-lint --db .cache/forum.sqlite3
uv run wq-forum-rag knowledge-graph alpha/neutralization-decay --db .cache/forum.sqlite3 --depth 2
uv run wq-forum-rag knowledge-export --db .cache/forum.sqlite3 --out .cache/wiki
uv run wq-forum-rag search-reindex --db .cache/forum.sqlite3
uv run wq-forum-rag source-status ./notes --db .cache/forum.sqlite3
uv run wq-forum-rag source-ingest-plan ./notes --db .cache/forum.sqlite3 --commit
```

## 精度 / 性能策略

当前策略优先“本地可跑 + 低维护成本”：

1. 默认检索使用 SQLite FTS5 做关键词候选召回，再复用现有 `ForumSearcher` 做 lexical + dense rerank；不开外部模型也能离线跑。
2. 数据持久化仍是 SQLite，适合本地单文件分发、增量更新和精确查找。
3. `find_by_exact` 走 `topic_id / url / title / 正文 / 评论 / chunk` 精确词命中，避免把字段名、报错、operator 等导航型问题交给语义检索。
4. `related_posts` 复用标题检索做近邻召回，优先返回同社区相关主题。
5. 自进化知识层采用“知识页优先 + 论坛证据回退”的渐进式披露；知识页搜索会叠加轻量 backlink boost。
6. `embedding_cache` 会缓存文档向量，重复搜索不需要反复 embed 同一内容。

如果后续要提高语义召回，可以保留当前 SQLite 作为元数据与精确查找层，再用 `.[local-embeddings]` 接入 `fastembed` 替换默认 dense backend，做更强的混合召回或 rerank。这样不会破坏现有 CLI/MCP contract。

## 与后续 parser/storage/search 集成

当前骨架已经直接复用项目内 `parser` / `storage` / `search`。后续即使替换 embedding backend 或调优 chunk/search 策略，也不需要改 CLI/MCP 对外接口。

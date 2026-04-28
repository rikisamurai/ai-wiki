# Repository Guidelines

## 项目定位

这是一个以 Obsidian 为核心的中文知识库，参考 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 范式构建。仓库重点是文档的可读性、可链接性和可持续整理，不是应用构建或发布。

## 核心理念

**三层架构**（严格隔离，不串味）：
- `sources/`：原料层，LLM **只读不改**。包含 clippings（剪藏）、posts（用户原创/译文）、inbox（草稿）、asset（图片）。
- `wiki/`：精华层，LLM **拥有可改**。从 sources 抽取的概念页面，按 agent-engineering / claude-code / skills / retrieval / frontend / business / obsidian 分类（部分一级下有二级子目录，详见目录树）。
- `AGENT.md`（CLAUDE.md 是其符号链接）：schema 层，定义工作流和约定。

**LLM 角色**：sources 只读、wiki 只写、log/index 自动维护。

**目标**：让维护成本接近零——用户专注产生原料和提问，LLM 负责沉淀和编织。

## 三种核心操作

通过 slash commands 触发，每个命令的完整定义见 `.claude/commands/`：

- **`/ingest <source-path>`**：把 sources/ 下一份原料抽取成 wiki/ 多个互链页面。
- **`/query <问题>`**：基于 wiki/ 回答问题；找不到才降级查 sources/；高价值答案 ingest 回 wiki/。
- **`/lint`**：扫 wiki/ 检测孤儿、矛盾、过时、断链、缺交叉引用。**只报告，不自动修**。
- **`/migrate-next`**：从根目录 `migration-backlog.md` 取下一条做 ingest（存量迁移驱动器）。**当前无活跃 backlog**，2026-04 首批 41 条已 drain，归档于 [[wiki/_orphans/migration-2026-04|wiki/_orphans/migration-2026-04.md]]。需新批次时重建根目录 `migration-backlog.md` 即可。

## 顶层目录

```
ai-wiki/
├── AGENT.md                      # schema（本文件）；CLAUDE.md → AGENT.md 符号链接
├── index.md                      # 内容目录（手写主框架 + Bases 嵌入）
├── log.md                        # append-only 时间线
├── migration-backlog.md          # 存量 ingest 进度（按需创建；2026-04 首批已归档至 wiki/_orphans/）
├── index.base / log.base         # Bases 动态视图
├── sources/                      # 只读原料
│   ├── clippings/                # 网页剪藏
│   ├── posts/{aigc,frontend,obsidian}/  # 用户原创/译文
│   ├── inbox/                    # 草稿
│   └── asset/                    # 图片
├── wiki/                         # 可改精华
│   ├── agent-engineering/        # philosophy / context / workflow / code-review
│   ├── claude-code/              # Claude Code & 同类 CLI 工具系
│   ├── skills/                   # Agent Skills 生态（跨工具资产）
│   ├── retrieval/                # rag / browser
│   ├── frontend/                 # web-platform / network / react-patterns / react-native / ui-libraries
│   ├── business/                 # 商业模式
│   ├── obsidian/                 # Obsidian 语法/工具/方法论
│   └── _orphans/                 # lint 检测出的孤儿暂存
├── .claude/commands/             # 4 个 slash commands
└── docs/superpowers/             # specs 与 plans
```

**source 路径与 wiki 路径不要求一一对应**：sources/ 按"内容来源"组织，wiki/ 按"概念域"组织。一个 source 可能产出跨多个 wiki 子域的页面。

## wiki 页面规范

每个 `wiki/**/*.md` 必须满足：

```yaml
---
title: 页面标题
tags: [tag1, tag2]              # kebab-case，最多 3 个
date: YYYY-MM-DD
sources:                         # 抽取自哪些 source
  - "[[sources/clippings/xxx]]"
last-ingested: YYYY-MM-DD
status: draft | stable | stale
---
```

正文规范：
- 单页面专注一个概念（atomic）
- 首段是 TL;DR（1-3 句）
- 至少 2 个 wikilink 出链到其他 wiki 页面
- 用 Obsidian callouts（`> [!note] / > [!example] / > [!compare]`）组织内容

**status 三态流转**（`/lint` 自动切换，无需人工 review）：
- `draft`：ingest 出生默认值，所有新页一律 draft
- `stable`：被 ≥3 个 wiki 页 wikilink 引用 → `/lint` 自动从 draft 升 stable
- `stale`：`last-ingested` 早于 180 天 → `/lint` 自动改成 stale；如要"续期"重跑 `/ingest <对应 source>` 即可重置
- 字段值非法（不在三态内）→ `/lint` 仅报告，由用户决定怎么改

## index.md / log.md 维护

- **每次 ingest 完成后**必须更新 `index.md`（在对应 `## <domain>` 分类下追加 wikilink）
- **每次操作完成后**必须 append 一行到 `log.md`，格式严格遵循：

  ```
  ## [YYYY-MM-DD HH:MM] <op> | <subject>
  - 正文一段说明（新建了什么、source 是哪个）
  ```

  `<op>` 取值：`ingest` / `lint` / `query` / `migrate-next`

- index.md 嵌入 `index.base` 的动态视图（最近更新、按 status 过滤）

## 文档编写规范

- 笔记内容尽量使用**中文**撰写，但英文专有名词不要使用中文（比如写"Agent"，不写"代理"）
- 使用 Obsidian Flavored Markdown（wikilinks、callouts、frontmatter 等）
- 内部链接使用 `[[wikilink]]`，外部链接使用标准 Markdown 语法
- 新建 wiki 页面必须包含 §wiki 页面规范 中的 frontmatter
- tag 必须 kebab-case，一篇文章最多 3 个 tags
- 善用 Obsidian callouts 组织内容
- **克制使用 header**（`##`、`###`）：短内容（少于 3-5 段实质内容、或只有 1-2 个 bullet 就讲完）不要单独开 header，改用 `**粗体引导句**：` 或直接成段。只有真正多分支且各分支较长的内容才上 header。Callout（`> [!note]` 等）自带视觉边界，外层不要再套 header。

## 提交规范

提交信息沿用现有风格，优先使用 `docs:` / `feat:` / `chore:` 开头，主题简短明确，例如 `docs: 新增 browser-use 对比文章`。涉及目录结构调整、链接修复、图片移动时在 commit 说明里写清楚。

每次 ingest / migrate-next 都应单独 commit，方便回滚。

## 与用户沟通

- 使用中文交流

---
title: 把 ai-wiki 重构为 Karpathy LLM Wiki 范式
date: 2026-04-22
status: approved
references:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# 设计：把 ai-wiki 重构为 Karpathy LLM Wiki 范式

## 背景

当前 ai-wiki 是一个以 Obsidian 为核心的中文知识库（AI Coding / AIGC / FrontEnd / Obsidian 工具四个域），存量约 50+ 篇内容混合存放在 emoji 主题目录、`Clippings/`、`00_inbox/` 中，没有「素材」与「精华」的架构性分离，也没有 Ingest / Lint 工作流。

目标是按 Karpathy 在 [llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 中提出的三层模型重构：raw sources（只读原料）/ wiki（LLM 拥有的精华页面）/ schema（CLAUDE.md），并落地三种核心操作 Ingest / Query / Lint。

## 核心决定（来自澄清环节）

| 维度 | 决定 |
|---|---|
| 迁移姿态 | 覆盖式重构 |
| Wiki 范围 | 一个统一 wiki |
| 原创内容定位 | 原创/译文 = raw source（LLM 不改写） |
| 操作触发方式 | Slash command 手动触发 |
| 存量迁移范围 | 骨架 + 全量 ingest |
| 实现风格 | 方案 B：Obsidian 原生增强（Bases + backlog 追踪） |

## 1. 顶层目录结构

```
ai-wiki/
├── CLAUDE.md              # schema 层（保留并扩展）
├── AGENTS.md              # 软链到 CLAUDE.md（保留）
├── index.md               # 内容目录（手写主框架 + Bases 嵌入）
├── log.md                 # append-only 时间线
├── sources/               # 所有「原料」，LLM 只读
│   ├── clippings/         # 网页剪藏（原 Clippings/）
│   ├── posts/             # 用户原创/译文长文
│   │   ├── aigc/          # 原 🚀AIGC/
│   │   ├── frontend/      # 原 🌇FrontEnd/
│   │   └── obsidian/      # 原 😈Magic/
│   ├── inbox/             # 草稿、待整理素材（原 00_inbox/）
│   └── asset/             # 各 source 配套图片
├── wiki/                  # LLM 生成 / 拥有的页面
│   ├── ai-coding/
│   ├── aigc/
│   ├── frontend/
│   ├── obsidian/
│   └── _orphans/          # lint 检测出无入链的页面暂存
├── migration-backlog.md   # 存量 ingest 进度追踪
├── index.base             # Bases：动态切片 wiki 页面
├── log.base               # Bases：按操作类型/日期过滤 log
└── .claude/
    └── commands/
        ├── ingest.md
        ├── lint.md
        ├── query.md
        └── migrate-next.md
```

**取舍说明**：
- 牺牲 emoji 目录视觉识别度，换取架构清晰
- `wiki/` 内分 4 个一级子域：太平铺 wikilink 不好认路、太深违反 Karpathy「扁平 + 依赖 index」精神，4 个子域是折中
- `wiki/_orphans/` 隔离离群页面，避免污染主域
- **source 路径与 wiki 路径不要求一一对应**：sources/ 按「内容来源」组织（aigc 是历史命名），wiki/ 按「概念域」组织（拆出 ai-coding 是因为 Claude Code / Codex / Cursor 类话题已成独立体系）。一个 source 可能 ingest 出跨多个 wiki 子域的页面，反之亦然。

## 2. Schema (CLAUDE.md) 改造

保留现有「项目定位 / 文档编写规范 / 提交规范 / 与用户沟通」四章，删除已过时的「目录结构」段，新增以下四章。

### 2.1 §核心理念

- 三层架构：raw sources / wiki / schema 严格隔离
- LLM 角色：sources 只读，wiki 只写
- 一句话目标：「让维护成本接近零」

### 2.2 §三种操作

每个操作 50-100 字描述 + 链接到对应 slash command 文件。

- **Ingest**：把 `sources/` 里一份原料抽取成 `wiki/` 多个互链页面
- **Query**：基于 `wiki/` 回答问题；高价值答案 ingest 回 wiki/
- **Lint**：扫 `wiki/` 检测孤儿、矛盾、过时、断链、缺交叉引用

### 2.3 §wiki 页面规范

- 单页面专注一个概念（atomic）
- 必须含 frontmatter，沿用现有规范，新增字段：

```yaml
---
title: 页面标题
tags: [tag1, tag2]              # 沿用 kebab-case，最多 3 个
date: YYYY-MM-DD
sources:                         # 新增：抽取自哪些 source
  - "[[sources/clippings/xxx]]"
last-ingested: YYYY-MM-DD        # 新增：最后一次 ingest 时间
status: draft | stable | stale   # 新增：lint 维护
---
```

- 至少 2 个 wikilink 出链
- 首段是 TL;DR
- 用 callouts 区分定义 / 示例 / 对比

### 2.4 §index.md / log.md 维护规则

- 每次 ingest 完成后必须更新 `index.md`（在对应分类追加 wikilink）
- 每次操作必须 append 一行到 `log.md`，格式：

  ```
  ## [YYYY-MM-DD HH:MM] <op> | <subject>
  - 正文一段说明
  ```

- index.md 里嵌入 Bases 视图（动态聚合最近更新、按 tag、按 status）

## 3. Slash Commands

放在 `.claude/commands/`，每个一个 `.md` 文件，遵循 Claude Code 命令标准。

### 3.1 `/ingest <source-path>`

把一份原料抽取成 wiki/ 页面。

**输入**：sources/ 下的某个文件路径或 wikilink

**流程**：
1. 读 source；识别 5-15 个值得独立成页的「概念 / 工具 / 事件」
2. 对每个概念：先检查 `wiki/` 是否已有同名 / 近义页面 → 有则追加补充，无则新建
3. 每个新页面建立 ≥2 个 wikilink 到现有 wiki 页
4. 在每个被影响页面的 frontmatter `sources:` 里加上这条 source
5. 更新 `index.md` 对应分类
6. append 到 `log.md`：`## [...] ingest | <source-title>` + 列出新建/更新的页面

**退出条件**：所有新页面都有出链；source 在某个 wiki 页 frontmatter 里被引用

### 3.2 `/lint`

健康检查，**只报告，不自动修**。

扫 `wiki/` 全部页面，输出报告：
- 孤儿（无入链 + 不在 index.md）→ 候选移到 `wiki/_orphans/`
- 缺出链（< 2 个 wikilink）
- `last-ingested` 超过 90 天的页面
- 标题 / 概念在多页面重复 → 候选合并
- index.md 里指向不存在文件的链接

修复由用户确认后再次 prompt 触发，不自动改。

### 3.3 `/query <问题>`

基于 wiki/ 答问。

**流程**：
1. 优先在 `wiki/` 里找答案
2. 找不到再降级查 `sources/`
3. 答完追问：「这个答案值得 ingest 回 wiki 吗？」→ 是的话生成新页面草稿
4. append 到 `log.md`：`## [...] query | <问题摘要>`

### 3.4 `/migrate-next`

存量迁移驱动器。

**流程**：
1. 读 `migration-backlog.md`，取下一条未完成 source（标记 `- [ ]`）
2. **复用 §3.1 的 ingest 流程**走完 6 步（slash command 不互相调用，命令文件里把 ingest 流程内联引用即可）
3. 完成后在 backlog 里勾掉，显示进度（X/Y 已完成）
4. 一次只处理一条，避免 context 爆炸
5. log.md 的 op 字段写 `migrate-next`（不是 `ingest`），便于事后区分主动 ingest 与存量迁移

## 4. index.md / log.md / Bases

### 4.1 index.md（约 100 行，手写为主）

```markdown
---
title: ai-wiki Index
date: 2026-04-22
---
# ai-wiki

> [!note] 三层架构
> sources/（原料，只读） · wiki/（精华，可改） · CLAUDE.md（schema）

## AI Coding
- [[wiki/ai-coding/agentic-coding-的边界]]
- [[wiki/ai-coding/prefix-cache-机制]]

## AIGC
- [[wiki/aigc/browser-use]]

## FrontEnd
- [[wiki/frontend/...]]

## Obsidian
- [[wiki/obsidian/...]]

---
## 动态视图

最近 7 天更新的 wiki：
![[index.base#recent-wiki]]

待 ingest 的 sources：
![[index.base#pending-sources]]
```

### 4.2 log.md（append-only）

格式严格遵循 Karpathy gist：`## [YYYY-MM-DD HH:MM] <op> | <subject>`，便于 grep。

```markdown
---
title: ai-wiki Activity Log
---
# Log

## [2026-04-22 14:30] ingest | Agentic Coding 的边界
- 新建 wiki/ai-coding/agentic-coding-的边界.md
- 更新 wiki/ai-coding/index 链接
- source: sources/inbox/Agentic Coding 的边界.md

## [2026-04-22 15:00] lint | weekly check
- 3 个孤儿移入 wiki/_orphans/
- 1 处断链已标注

## [2026-04-22 16:10] migrate-next | 1/47
- 处理：sources/clippings/Large Language Models explained briefly.md
- 生成 wiki 页面：5 个
```

### 4.3 Bases

两个文件 `index.base`、`log.base`：

- `index.base`：按 wiki/ 子域分 view，按 status / last-ingested 过滤
- `log.base`：按操作类型（ingest / lint / query / migrate）过滤、按日期排序

**Bases 是叠加而不是替代**：static index.md 仍然是真相源，Bases 只是动态切片。

## 5. 存量迁移流程

### Phase 0：骨架就位（一次性，约 30 分钟）

- 建空目录：`sources/{clippings,posts/{aigc,frontend,obsidian},inbox,asset}`、`wiki/{ai-coding,aigc,frontend,obsidian,_orphans}`、`.claude/commands/`
- 写 4 个 slash command 文件
- 改写 CLAUDE.md（按 §2）
- 创建空 `index.md`、`log.md`、`migration-backlog.md`
- 写 2 个 Bases 文件

### Phase 1：物理迁移（一次性，无 ingest）

- `Clippings/*` → `sources/clippings/`
- `00_inbox/*.md` → `sources/inbox/`
- `🚀AIGC/**` → `sources/posts/aigc/`
- `🌇FrontEnd/**` → `sources/posts/frontend/`
- `😈Magic/**` → `sources/posts/obsidian/`
- 各级 `asset/` 图片随原文移动；wikilink 由 Obsidian 自动更新（需开启 Auto-update internal links）
- **不删原 emoji 目录**直到验证 wikilink 全通——这一步以一次 commit 收尾
- 把所有 source 文件路径列入 `migration-backlog.md`，每条 `- [ ] sources/...`

### Phase 2：增量 ingest（持续，按节奏跑）

**优先级顺序**：
1. `sources/inbox/`（最新草稿，最贴近当前思考）
2. `sources/posts/aigc/`（最关心的领域）
3. `sources/clippings/`（外部信源）
4. `sources/posts/{frontend,obsidian}/`

**节奏建议**：每天跑 `/migrate-next` 1-3 次，每次 1 篇；每周跑 1 次 `/lint`。

**进度可见**：`migration-backlog.md` 顶部显示 `进度：X/Y`。

### Phase 3：清理与稳定（迁移完成后）

- 删除空的旧 emoji 目录
- 跑完整 `/lint`，处理孤儿、断链、过时
- 把 `migration-backlog.md` 归档到 `wiki/_orphans/migration-2026-04.md` 留念

### 风险控制

- Phase 0 + 1 在一个 PR 里完成、可回滚
- Phase 2 每次 ingest 都是 atomic commit（一个 source 一个 commit）
- 如果某 source 太长导致 ingest 失败，标记为 `- [SKIP]` 并记录原因，不阻塞流水线

## 6. 成功标准

设计落地后，以下都成立：

1. `sources/` 下所有内容 LLM 不会自动修改（只在用户主动要求时才动）
2. `wiki/` 下每个页面都有 frontmatter（含 sources / last-ingested）、≥2 个 wikilink 出链、TL;DR 首段
3. `index.md` 能让陌生人在 1 分钟内找到任意主题的入口
4. `log.md` grep `## \[2026-04` 能拉出当月所有操作
5. `/ingest` `/lint` `/query` `/migrate-next` 4 个命令在 Claude Code 中可用
6. `migration-backlog.md` 进度从 0% 推进到 100%（迁移完成的标志）

## 7. 非目标（YAGNI）

- 不引入 hooks 全自动化
- 不引入向量检索 / qmd / 嵌入
- 不做多 wiki / 多 schema
- 不引入 Marp 或其他 gist 里提到但与当前用户无关的工具
- 不重写用户原创内容的措辞（status: stable 之后 LLM 不动）

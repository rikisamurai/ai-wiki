# LLM Wiki 重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 ai-wiki 从「emoji 主题目录混合存储」重构为 Karpathy LLM Wiki 三层架构（sources / wiki / schema），落地 4 个 slash commands 和存量迁移 backlog。

**Architecture:** Phase 0 建骨架（目录、commands、schema、空 index/log/backlog/bases）；Phase 1 用 `git mv` 把所有现存内容迁入 `sources/`，并填充 backlog；Phase 2（不在本计划内）由用户使用 `/migrate-next` 持续把 sources 抽取成 wiki。

**Tech Stack:** Markdown + Obsidian Flavored Markdown + Obsidian Bases + Claude Code slash commands + git

**Spec reference:** `docs/superpowers/specs/2026-04-22-llm-wiki-design.md`

**Scope of this plan:** Pre-flight + Phase 0 + Phase 1 + 一次端到端 smoke test。Phase 2/3 是用户长期运营行为，不在本计划。

---

## Pre-flight: 处理未提交改动

当前 working tree 有大量未提交改动（00_inbox 新文件、Clippings 已删除、AIGC 有 modify、FrontEnd 有新文件）。这些必须先成为基线，否则 git mv 会让它们混入"重构"提交里，回滚困难。

### Task P.1: 检视并分类未提交改动

**Files:**
- Inspect: working tree

- [ ] **Step 1: 列出当前未提交改动**

Run: `git status --short`
Expected: 多行 `M /??/D` 改动，混合 .obsidian、内容文件、新草稿。

- [ ] **Step 2: 用户确认这些改动的归属**

跟用户确认两件事：
1. 这些未提交内容（特别是 00_inbox 里的几个新草稿）是否要保留进重构后的 sources/inbox/？（默认是）
2. .obsidian/ 下的插件配置改动是否要进重构提交？（默认是，分开 commit）

如果用户没有特殊偏好，按上述默认走。

- [ ] **Step 3: 单独 commit Obsidian 配置类改动**

```bash
git add .obsidian/community-plugins.json .obsidian/plugins/manual-sorting/data.json .obsidian/plugins/obsidian-image-toolkit/
git commit -m "chore: 同步 Obsidian 插件配置"
```

Expected: 1 个 commit 落地，与重构无关的配置噪声排除。

- [ ] **Step 4: 单独 commit 内容类改动（草稿、新文章、删除项）**

```bash
git add 00_inbox/ "🌇FrontEnd/React/React Native/react-native tips.md" "🚀AIGC/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/"
git rm "Clippings/Large Language Models explained briefly.md" 2>/dev/null || true
git status --short
git commit -m "docs: 重构前内容基线（待整理草稿与新文章入库）"
```

Expected: working tree 干净（`git status` 无输出）。

- [ ] **Step 5: 验证 working tree 干净**

Run: `git status`
Expected: `nothing to commit, working tree clean`

---

## Phase 0：骨架就位

### Task 0.1: 创建空目录骨架

**Files:**
- Create dirs: `sources/{clippings,posts/{aigc,frontend,obsidian},inbox,asset}`、`wiki/{ai-coding,aigc,frontend,obsidian,_orphans}`、`.claude/commands/`

- [ ] **Step 1: 一次性创建所有目录**

```bash
cd /Users/shanyulong/riki/wiki/ai-wiki
mkdir -p sources/clippings sources/posts/aigc sources/posts/frontend sources/posts/obsidian sources/inbox sources/asset
mkdir -p wiki/ai-coding wiki/aigc wiki/frontend wiki/obsidian wiki/_orphans
mkdir -p .claude/commands
```

- [ ] **Step 2: 在每个空目录放 .gitkeep（git 不追踪空目录）**

```bash
touch sources/clippings/.gitkeep sources/posts/aigc/.gitkeep sources/posts/frontend/.gitkeep sources/posts/obsidian/.gitkeep sources/inbox/.gitkeep sources/asset/.gitkeep
touch wiki/ai-coding/.gitkeep wiki/aigc/.gitkeep wiki/frontend/.gitkeep wiki/obsidian/.gitkeep wiki/_orphans/.gitkeep
```

- [ ] **Step 3: 验证目录结构**

Run: `find sources wiki .claude/commands -type d`
Expected: 列出 11 个目录，与 spec §1 一致。

- [ ] **Step 4: Commit**

```bash
git add sources/ wiki/ .claude/commands/
git commit -m "feat(wiki): 建立 Karpathy 三层架构空骨架"
```

---

### Task 0.2: 写 `/ingest` slash command

**Files:**
- Create: `.claude/commands/ingest.md`

- [ ] **Step 1: 写 ingest.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/.claude/commands/ingest.md` with content:

```markdown
---
description: 把 sources/ 下一份原料抽取成 wiki/ 多个互链页面
argument-hint: <source-path>
---

# /ingest

输入：`$ARGUMENTS`（sources/ 下的某个文件路径或 wikilink）

## 你必须严格遵守的步骤

1. **读 source**：用 Read 工具读取 `$ARGUMENTS` 指向的文件全文。如果 source 是 wikilink 形式（`[[xxx]]`），先在 `sources/` 下定位实际路径。

2. **识别概念**：识别其中 5-15 个值得独立成页的概念、工具、事件、人物。每个概念应满足：
   - 能被一句话定义
   - 大概率会在未来其他 source 中再次出现
   - 不是 source 的一次性论点

3. **检查重复**：对每个概念，先用 Grep 在 `wiki/` 全域搜近义页面（含别名、英文/中文对照）。
   - 已有 → 走"追加补充"分支
   - 没有 → 走"新建"分支

4. **写页面**（每页都满足）：
   - 路径：`wiki/<domain>/<kebab-case-标题>.md`，domain 在 ai-coding / aigc / frontend / obsidian 里选
   - frontmatter 含：title / tags（≤3 kebab-case）/ date / sources（wikilink 列表）/ last-ingested / status: draft
   - 首段是 TL;DR（1-3 句，不带 "TL;DR:" 前缀）
   - 至少 2 个 wikilink 出链到其他 wiki 页面
   - 用 Obsidian callouts 区分定义 / 示例 / 对比

5. **回填 frontmatter**：在每个被影响的 wiki 页面的 `sources:` 列表里加上这条 source（wikilink 形式）。

6. **更新 index.md**：在对应 `## <domain>` 标题下追加 wikilink 行（按字母序插入，不重复）。

7. **append 到 log.md**：

   ```
   ## [YYYY-MM-DD HH:MM] ingest | <source 标题>
   - 新建：[[wiki/.../page-a]]、[[wiki/.../page-b]]
   - 更新：[[wiki/.../page-c]]
   - source: $ARGUMENTS
   ```

## 退出条件

完成时必须满足：
- 所有新建/更新的 wiki 页面都有 ≥2 个 wikilink 出链
- 这条 source 至少在 1 个 wiki 页面的 frontmatter `sources:` 里出现
- index.md 和 log.md 都已更新
- **不修改 source 本身**

## 禁止

- 不修改 `sources/` 下任何文件
- 不写超过 15 个概念页（控制单次 ingest 规模）
- 不在 wiki 页面里放原 source 的大段引用（精华提炼，不是搬运）
```

- [ ] **Step 2: 验证文件存在**

Run: `cat .claude/commands/ingest.md | head -3`
Expected: 看到 frontmatter 开头。

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/ingest.md
git commit -m "feat(commands): /ingest slash command"
```

---

### Task 0.3: 写 `/lint` slash command

**Files:**
- Create: `.claude/commands/lint.md`

- [ ] **Step 1: 写 lint.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/.claude/commands/lint.md` with content:

```markdown
---
description: 扫 wiki/ 输出健康报告，不自动修
---

# /lint

扫 `wiki/` 全部 markdown 文件，**只报告，不自动改**。

## 你必须输出的检查项

### 1. 孤儿页面
- 定义：在 `wiki/` 下存在，但没有任何其他 wiki 页面 wikilink 到它，且不在 `index.md` 里
- 报告：列出文件路径，建议候选动作（移到 `wiki/_orphans/` 或在 index.md 补链）

### 2. 出链不足
- 定义：wiki 页面正文中 wikilink 数 < 2
- 报告：列出文件路径 + 当前 wikilink 数

### 3. 过时页面
- 定义：frontmatter `last-ingested` 早于 90 天前（用 `date -v-90d +%Y-%m-%d` 拿基准）
- 报告：列出文件路径 + last-ingested 日期

### 4. 概念重复
- 定义：标题或 H1 在多个文件高度相似（启发式：包含相同 ≥4 字关键词）
- 报告：列出候选合并组

### 5. 断链
- 定义：`index.md` 或 wiki 页面里的 wikilink 指向不存在的文件
- 报告：源文件 + 断链目标

### 6. status 异常
- frontmatter 缺 status，或 status 不在 {draft, stable, stale} 内

## 输出格式

把上面 6 类各自一节，用 markdown 输出到对话。每节末尾给"建议下一步"（一条 prompt 用户复制就能继续）。

## 退出条件

- 全部 6 类检查跑完
- 报告里至少包含每类的"零项"或"具体清单"
- append 到 log.md：`## [...] lint | weekly check` + 简要数字汇总

## 禁止

- 不自动修任何文件（除了 log.md）
- 不删任何 wiki 页面（即便是孤儿，移动也要等用户确认）
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/lint.md
git commit -m "feat(commands): /lint slash command"
```

---

### Task 0.4: 写 `/query` slash command

**Files:**
- Create: `.claude/commands/query.md`

- [ ] **Step 1: 写 query.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/.claude/commands/query.md` with content:

```markdown
---
description: 基于 wiki/ 答问，找不到才降级查 sources/
argument-hint: <问题>
---

# /query

问题：`$ARGUMENTS`

## 你必须遵守的步骤

1. **优先在 wiki/ 找答案**
   - 用 Grep 在 `wiki/` 全域搜关键词
   - 命中后阅读相关页面，组合答案
   - 答案中引用的 wiki 页面用 wikilink 列出来

2. **找不到时降级查 sources/**
   - 同样的 Grep，但在 `sources/` 下
   - 答案要明确标注"以下来自未 ingest 的 source，wiki 里还没沉淀"

3. **追问 ingest 价值**
   - 答完后，问用户：「这个答案值得 ingest 回 wiki 吗？」
   - 如果 yes：生成 1-3 个新 wiki 页面草稿（按 /ingest 的页面规范），写入 `wiki/` 对应 domain
   - 如果 no：跳过

4. **append 到 log.md**

   ```
   ## [YYYY-MM-DD HH:MM] query | <问题摘要>
   - 来源：wiki | sources | both
   - 是否 ingest：yes/no
   ```

## 禁止

- 不基于"训练数据"答题（必须有 wiki/ 或 sources/ 的 grep 命中作为依据）
- 不修改 sources/
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/query.md
git commit -m "feat(commands): /query slash command"
```

---

### Task 0.5: 写 `/migrate-next` slash command

**Files:**
- Create: `.claude/commands/migrate-next.md`

- [ ] **Step 1: 写 migrate-next.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/.claude/commands/migrate-next.md` with content:

```markdown
---
description: 从 migration-backlog.md 取下一条 source 做 ingest
---

# /migrate-next

存量迁移驱动器。一次只处理 backlog 里的 1 条 source。

## 你必须遵守的步骤

1. **读 backlog**：Read `migration-backlog.md`。
2. **取下一条**：找到第一个 `- [ ]` 开头的 source 路径。如果全部勾完了，输出 "Migration complete 🎉" 并退出。
3. **遵循 §3.1 ingest 流程**：把那条 source 当作 `/ingest` 的输入，跑完 6 步流程（见 `.claude/commands/ingest.md`）。
4. **勾掉 backlog**：把这一条的 `- [ ]` 改成 `- [x]`，并在末尾追加 `← YYYY-MM-DD`。
5. **更新进度**：把 backlog 文件顶部的 `进度：X/Y` 数字加 1。
6. **append 到 log.md**：op 字段写 `migrate-next`（不是 `ingest`，便于事后区分主动 ingest 与存量迁移）：

   ```
   ## [YYYY-MM-DD HH:MM] migrate-next | <X>/<Y> · <source 标题>
   - 新建：[[wiki/...]]、[[wiki/...]]
   - source: <path>
   ```

## 失败处理

- 如果 source 太长导致 ingest 失败 → 把 backlog 那条的 `- [ ]` 改成 `- [SKIP]` 并在末尾加 ← YYYY-MM-DD: <原因>，**不阻塞流水线**，输出说明后退出。

## 禁止

- 一次只处理 1 条，不连续跑（context 爆炸）
- 不跳过 backlog 顺序（按从上到下 FIFO）
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/migrate-next.md
git commit -m "feat(commands): /migrate-next slash command"
```

---

### Task 0.6: 改写 CLAUDE.md（实际是 AGENTS.md，CLAUDE.md 是 symlink）

**Files:**
- Modify: `AGENTS.md` (CLAUDE.md is symlink to it)

- [ ] **Step 1: 读现有 AGENTS.md**

Run: `cat AGENTS.md`
Expected: 看到现有 4 章（项目定位 / 目录结构 / 文档编写规范 / 提交规范 / 与用户沟通）。记下哪些章节要保留、哪些要替换。

- [ ] **Step 2: 完整重写 AGENTS.md**

用 Write 工具完全覆盖 `AGENTS.md`：

```markdown
# Repository Guidelines

## 项目定位

这是一个以 Obsidian 为核心的中文知识库，参考 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 范式构建。仓库重点是文档的可读性、可链接性和可持续整理，不是应用构建或发布。

## 核心理念

**三层架构**（严格隔离，不串味）：
- `sources/`：原料层，LLM **只读不改**。包含 clippings（剪藏）、posts（用户原创/译文）、inbox（草稿）、asset（图片）。
- `wiki/`：精华层，LLM **拥有可改**。从 sources 抽取的概念页面，按 ai-coding / aigc / frontend / obsidian 分类。
- `AGENTS.md`（即 CLAUDE.md）：schema 层，定义工作流和约定。

**LLM 角色**：sources 只读、wiki 只写、log/index 自动维护。

**目标**：让维护成本接近零——用户专注产生原料和提问，LLM 负责沉淀和编织。

## 三种核心操作

通过 slash commands 触发，每个命令的完整定义见 `.claude/commands/`：

- **`/ingest <source-path>`**：把 sources/ 下一份原料抽取成 wiki/ 多个互链页面。
- **`/query <问题>`**：基于 wiki/ 回答问题；找不到才降级查 sources/；高价值答案 ingest 回 wiki/。
- **`/lint`**：扫 wiki/ 检测孤儿、矛盾、过时、断链、缺交叉引用。**只报告，不自动修**。
- **`/migrate-next`**：从 `migration-backlog.md` 取下一条做 ingest（存量迁移驱动器）。

## 顶层目录

```
ai-wiki/
├── AGENTS.md / CLAUDE.md         # schema（本文件）
├── index.md                      # 内容目录（手写主框架 + Bases 嵌入）
├── log.md                        # append-only 时间线
├── migration-backlog.md          # 存量 ingest 进度
├── index.base / log.base         # Bases 动态视图
├── sources/                      # 只读原料
│   ├── clippings/                # 网页剪藏
│   ├── posts/{aigc,frontend,obsidian}/  # 用户原创/译文
│   ├── inbox/                    # 草稿
│   └── asset/                    # 图片
├── wiki/                         # 可改精华
│   ├── ai-coding/ aigc/ frontend/ obsidian/
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

## 提交规范

提交信息沿用现有风格，优先使用 `docs:` / `feat:` / `chore:` 开头，主题简短明确，例如 `docs: 新增 browser-use 对比文章`。涉及目录结构调整、链接修复、图片移动时在 commit 说明里写清楚。

每次 ingest / migrate-next 都应单独 commit，方便回滚。

## 与用户沟通

- 使用中文交流
```

- [ ] **Step 3: 验证 symlink 仍指向 AGENTS.md**

Run: `ls -la CLAUDE.md`
Expected: `CLAUDE.md -> AGENTS.md`（symlink 没断）

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "docs(schema): 改写 CLAUDE.md 为 LLM Wiki 三层架构 schema"
```

---

### Task 0.7: 创建初始 index.md

**Files:**
- Create: `index.md`

- [ ] **Step 1: 写 index.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/index.md` with content:

```markdown
---
title: ai-wiki Index
date: 2026-04-22
---

# ai-wiki

> [!note] 三层架构
> `sources/`（原料，只读） · `wiki/`（精华，可改） · `AGENTS.md`（schema）
>
> 用 `/ingest` `/query` `/lint` `/migrate-next` 操作。详见 [[AGENTS]]。

## AI Coding

_等待第一次 ingest_

## AIGC

_等待第一次 ingest_

## FrontEnd

_等待第一次 ingest_

## Obsidian

_等待第一次 ingest_

---

## 动态视图

最近 7 天更新的 wiki 页面：
![[index.base#recent-wiki]]

待 ingest 的 sources：
![[index.base#pending-sources]]
```

- [ ] **Step 2: Commit**

```bash
git add index.md
git commit -m "docs: 新增 index.md 主框架"
```

---

### Task 0.8: 创建初始 log.md

**Files:**
- Create: `log.md`

- [ ] **Step 1: 写 log.md**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/log.md` with content：

```markdown
---
title: ai-wiki Activity Log
---

# Log

> append-only 时间线，记录所有 ingest / query / lint / migrate-next 操作。
> 格式：`## [YYYY-MM-DD HH:MM] <op> | <subject>`，便于 `grep '## \[2026-'`。

## [2026-04-22 16:30] init | ai-wiki 重构落地
- 建立 sources/ wiki/ .claude/commands/ 骨架
- 写入 4 个 slash commands
- 改写 AGENTS.md 为 LLM Wiki schema
- 创建 index.md / log.md / migration-backlog.md / *.base
```

- [ ] **Step 2: Commit**

```bash
git add log.md
git commit -m "docs: 新增 log.md 时间线"
```

---

### Task 0.9: 创建 Bases 文件

**Files:**
- Create: `index.base`, `log.base`

- [ ] **Step 1: 写 index.base**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/index.base`:

```yaml
filters:
  and:
    - file.folder.startsWith("wiki")
    - file.ext == "md"
properties:
  title:
    displayName: 标题
  status:
    displayName: 状态
  last-ingested:
    displayName: 最近 ingest
  tags:
    displayName: tags
views:
  - type: table
    name: recent-wiki
    order:
      - file.name
      - status
      - last-ingested
      - tags
    sort:
      - property: last-ingested
        direction: DESC
    limit: 30
  - type: table
    name: by-domain
    groupBy: file.folder
    order:
      - file.name
      - status
      - last-ingested
  - type: table
    name: pending-sources
    filters:
      and:
        - file.folder.startsWith("sources")
        - file.ext == "md"
    order:
      - file.name
      - file.folder
      - file.mtime
    sort:
      - property: file.mtime
        direction: DESC
    limit: 30
```

- [ ] **Step 2: 写 log.base**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/log.base`:

```yaml
filters:
  and:
    - file.name == "log.md"
properties:
  file.name:
    displayName: 文件
views:
  - type: table
    name: ops-by-date
    order:
      - file.name
```

> 说明：log.md 是 append-only 单文件，Bases 不擅长按 H2 拆分。这个 base 主要作为占位；真实查询用 `grep '## \[2026-04' log.md` 或 Obsidian 内置全局搜索。

- [ ] **Step 3: Commit**

```bash
git add index.base log.base
git commit -m "docs: 新增 Bases 动态视图（index/log）"
```

---

### Task 0.10: 创建空 migration-backlog.md（Phase 1 会填充）

**Files:**
- Create: `migration-backlog.md`

- [ ] **Step 1: 写占位 backlog**

Write file `/Users/shanyulong/riki/wiki/ai-wiki/migration-backlog.md`:

```markdown
---
title: Migration Backlog
date: 2026-04-22
---

# 存量 Source Ingest Backlog

进度：0/0 _（Phase 1 物理迁移完成后填充）_

> 用 `/migrate-next` 自动取下一条。完成的条目会被勾掉并附日期。
> 失败的标记为 `- [SKIP]` 并附原因，不阻塞流水线。

## inbox（最高优先级）

_等待 Phase 1 填充_

## posts/aigc

_等待 Phase 1 填充_

## clippings

_等待 Phase 1 填充_

## posts/frontend

_等待 Phase 1 填充_

## posts/obsidian

_等待 Phase 1 填充_
```

- [ ] **Step 2: Commit**

```bash
git add migration-backlog.md
git commit -m "docs: 新增 migration-backlog 占位"
```

---

### Task 0.11: Phase 0 整体验证

- [ ] **Step 1: 列出本阶段产出**

```bash
ls -la AGENTS.md index.md log.md migration-backlog.md index.base log.base
ls -la .claude/commands/
find sources wiki -type d
```

Expected:
- 6 个顶层文件存在
- 4 个 .md 命令文件存在
- 11 个目录存在（sources/ 6 个 + wiki/ 5 个 + .claude/commands/ 1 个，已减去重复）

- [ ] **Step 2: 检查 commit 历史**

Run: `git log --oneline -15`
Expected: 至少 9 个 Phase 0 commits（骨架 + 4 commands + AGENTS + index + log + bases + backlog）。

---

## Phase 1：物理迁移

### Task 1.1: 启用 Obsidian 链接自动更新

**Files:**
- Inspect: `.obsidian/app.json`

- [ ] **Step 1: 检查当前设置**

Run: `cat .obsidian/app.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('alwaysUpdateLinks:', d.get('alwaysUpdateLinks', 'NOT SET'))"`
Expected: 输出 `alwaysUpdateLinks: True` 或 `NOT SET`。如果是 False 或 NOT SET，进入 Step 2。

- [ ] **Step 2: 设置 alwaysUpdateLinks=true**

如果上一步显示需要修改：
```bash
python3 -c "
import json
with open('.obsidian/app.json') as f:
    d = json.load(f)
d['alwaysUpdateLinks'] = True
with open('.obsidian/app.json', 'w') as f:
    json.dump(d, f, indent=2)
"
```

- [ ] **Step 3: 提示用户**

告诉用户：「请打开 Obsidian，确认 设置 → 文件与链接 → 自动更新内部链接 = 开。git mv 不会触发 Obsidian 重写 wikilink，所以正式迁移前需要在 Obsidian 内做一次 rename 触发更新——这一步在 Task 1.7 处理。」

- [ ] **Step 4: 如果 app.json 改动了，commit**

```bash
git diff --quiet .obsidian/app.json || (git add .obsidian/app.json && git commit -m "chore(obsidian): 启用 alwaysUpdateLinks")
```

---

### Task 1.2: 迁移 Clippings/

**Files:**
- Move: `Clippings/*` → `sources/clippings/`

- [ ] **Step 1: 检查 Clippings 是否存在**

Run: `ls Clippings/ 2>/dev/null && git ls-files Clippings/`

注意：根据 pre-flight 的 git status，Clippings/Large Language Models explained briefly.md 可能已被 git rm（因为前面 commit 的内容基线把删除也提交了）。如果目录不存在或为空，跳到 Step 4。

- [ ] **Step 2: 用 git mv 迁移**

```bash
if [ -d Clippings ]; then
  for f in Clippings/*; do
    [ -e "$f" ] || continue
    git mv "$f" "sources/clippings/$(basename "$f")"
  done
  rmdir Clippings 2>/dev/null || true
fi
```

- [ ] **Step 3: 验证**

Run: `ls sources/clippings/ && git status --short`
Expected: 看到 clipping 文件在新位置，git status 显示 R 重命名。

- [ ] **Step 4: Commit（即使没有迁移也安全跳过）**

```bash
git diff --cached --quiet || git commit -m "refactor(wiki): 迁移 Clippings/ → sources/clippings/"
```

---

### Task 1.3: 迁移 00_inbox/

**Files:**
- Move: `00_inbox/*` → `sources/inbox/`

- [ ] **Step 1: 列出 inbox 内容**

Run: `ls 00_inbox/`
Expected: 6-7 个 .md 文件 + 1 个 asset/ 子目录。

- [ ] **Step 2: 用 git mv 整体迁移**

```bash
git mv 00_inbox/* sources/inbox/
rmdir 00_inbox 2>/dev/null || true
```

注意：包含中文/特殊字符文件名时 shell 通配符通常没问题。如果某文件失败，单独 git mv "文件名"。

- [ ] **Step 3: 验证 asset 子目录跟着移动了**

Run: `ls sources/inbox/asset/ 2>/dev/null | head`
Expected: 看到几张 Pasted image 图片。如果 asset 没跟着走，单独 `git mv 00_inbox/asset sources/inbox/asset`。

- [ ] **Step 4: Commit**

```bash
git status --short | head
git commit -m "refactor(wiki): 迁移 00_inbox/ → sources/inbox/"
```

---

### Task 1.4: 迁移 🚀AIGC/

**Files:**
- Move: `🚀AIGC/*` → `sources/posts/aigc/`

- [ ] **Step 1: 列出 AIGC 子目录**

Run: `ls "🚀AIGC/"`
Expected: 看到 `ai-coding`、`browser-use`、`rag` 三个子目录。

- [ ] **Step 2: 用 git mv 迁移子目录**

```bash
for d in "🚀AIGC"/*; do
  [ -e "$d" ] || continue
  name=$(basename "$d")
  git mv "$d" "sources/posts/aigc/$name"
done
rmdir "🚀AIGC" 2>/dev/null || true
```

- [ ] **Step 3: 验证**

Run: `find sources/posts/aigc -maxdepth 2 -type d`
Expected: ai-coding / browser-use / rag 都在新位置。

- [ ] **Step 4: Commit**

```bash
git commit -m "refactor(wiki): 迁移 🚀AIGC/ → sources/posts/aigc/"
```

---

### Task 1.5: 迁移 🌇FrontEnd/

**Files:**
- Move: `🌇FrontEnd/*` → `sources/posts/frontend/`

- [ ] **Step 1: 列出**

Run: `ls "🌇FrontEnd/"`

- [ ] **Step 2: 用 git mv 迁移**

```bash
for d in "🌇FrontEnd"/*; do
  [ -e "$d" ] || continue
  name=$(basename "$d")
  git mv "$d" "sources/posts/frontend/$name"
done
rmdir "🌇FrontEnd" 2>/dev/null || true
```

- [ ] **Step 3: 验证 + Commit**

```bash
find sources/posts/frontend -maxdepth 2 | head
git commit -m "refactor(wiki): 迁移 🌇FrontEnd/ → sources/posts/frontend/"
```

---

### Task 1.6: 迁移 😈Magic/

**Files:**
- Move: `😈Magic/*` → `sources/posts/obsidian/`

- [ ] **Step 1: 列出**

Run: `ls "😈Magic/"`

- [ ] **Step 2: 用 git mv 迁移**

```bash
for d in "😈Magic"/*; do
  [ -e "$d" ] || continue
  name=$(basename "$d")
  git mv "$d" "sources/posts/obsidian/$name"
done
rmdir "😈Magic" 2>/dev/null || true
```

- [ ] **Step 3: 验证 + Commit**

```bash
find sources/posts/obsidian -maxdepth 2 | head
git commit -m "refactor(wiki): 迁移 😈Magic/ → sources/posts/obsidian/"
```

---

### Task 1.7: Obsidian 内"假 rename"触发 wikilink 更新

**Files:**
- Inspect / fix: 任何 .md 文件里的 wikilink

- [ ] **Step 1: 全量扫描旧路径 wikilink**

Run（找出仍指向旧目录的 wikilink）：
```bash
grep -rn -E '\[\[(00_inbox|Clippings|🚀AIGC|🌇FrontEnd|😈Magic)' sources/ --include="*.md" 2>/dev/null | head -50
```
Expected: 如果有命中，需要修复。如果空，直接跳到 Step 4。

- [ ] **Step 2: 让用户在 Obsidian 内手动修复**

如果 Step 1 有命中，告诉用户：「Obsidian 没看到外部 git mv，wikilink 没自动更新。请在 Obsidian 里：
1. 打开命令面板 → "Reload app without saving"
2. 任意文件右键 → Rename → 加个空格再去掉（触发链接刷新）
或者，直接手动批量替换：用下面的 sed 命令批量修。」

- [ ] **Step 3: （可选）批量 sed 替换旧路径前缀**

仅当 Step 1 有命中且用户授权批量修改时：
```bash
# 在所有 .md 里替换旧路径前缀（dry-run 先看）
grep -rl -E '\[\[(00_inbox|Clippings|🚀AIGC|🌇FrontEnd|😈Magic)' sources/ --include="*.md" 2>/dev/null | while read f; do
  sed -i.bak \
    -e 's|\[\[00_inbox/|[[sources/inbox/|g' \
    -e 's|\[\[Clippings/|[[sources/clippings/|g' \
    -e 's|\[\[🚀AIGC/|[[sources/posts/aigc/|g' \
    -e 's|\[\[🌇FrontEnd/|[[sources/posts/frontend/|g' \
    -e 's|\[\[😈Magic/|[[sources/posts/obsidian/|g' \
    "$f"
  rm "$f.bak"
done
```

- [ ] **Step 4: 重新扫描确认无残留**

Run: `grep -rn -E '\[\[(00_inbox|Clippings|🚀AIGC|🌇FrontEnd|😈Magic)' sources/ --include="*.md" 2>/dev/null | wc -l`
Expected: `0`

- [ ] **Step 5: Commit（如果有改动）**

```bash
git diff --quiet || (git add -u && git commit -m "fix(wiki): 修复迁移后的 wikilink 指向")
```

---

### Task 1.8: 填充 migration-backlog.md

**Files:**
- Modify: `migration-backlog.md`

- [ ] **Step 1: 列出所有 source .md 文件并分类**

```bash
echo "=== inbox ==="; find sources/inbox -maxdepth 5 -name "*.md" | sort
echo "=== posts/aigc ==="; find sources/posts/aigc -maxdepth 5 -name "*.md" | sort
echo "=== clippings ==="; find sources/clippings -maxdepth 5 -name "*.md" | sort
echo "=== posts/frontend ==="; find sources/posts/frontend -maxdepth 5 -name "*.md" | sort
echo "=== posts/obsidian ==="; find sources/posts/obsidian -maxdepth 5 -name "*.md" | sort
echo "=== TOTAL ==="; find sources -name "*.md" | wc -l
```

记下总数 N（约 40-50）。

- [ ] **Step 2: 用 Write 工具重写 migration-backlog.md**

把 5 个章节的占位 `_等待 Phase 1 填充_` 替换为实际清单。每条用 `- [ ] ` 前缀，路径用反引号包裹。

模板：
```markdown
---
title: Migration Backlog
date: 2026-04-22
---

# 存量 Source Ingest Backlog

进度：0/N _（用 `/migrate-next` 推进，每完成一条进度 +1）_

> 用 `/migrate-next` 自动取下一条。完成的条目会被勾掉并附日期。
> 失败的标记为 `- [SKIP]` 并附原因，不阻塞流水线。

## inbox（最高优先级）

- [ ] `sources/inbox/Agentic Coding 的边界.md`
- [ ] `sources/inbox/为什么你的"AI 优先"战略可能大错特错？.md`
- ...（按 Step 1 输出填充全部）

## posts/aigc

- [ ] `sources/posts/aigc/ai-coding/...md`
- ...

## clippings

- [ ] `sources/clippings/Large Language Models explained briefly.md`
- ...

## posts/frontend

- [ ] `sources/posts/frontend/...`
- ...

## posts/obsidian

- [ ] `sources/posts/obsidian/...`
- ...
```

把分母 N 替换为 Step 1 拿到的 TOTAL。

- [ ] **Step 3: 验证**

Run: `grep -c '^- \[ \]' migration-backlog.md`
Expected: 输出等于 Step 1 的 TOTAL。

- [ ] **Step 4: Commit**

```bash
git add migration-backlog.md
git commit -m "docs: 填充 migration-backlog（N 条 sources 待 ingest）"
```

---

### Task 1.9: Phase 1 整体验证

- [ ] **Step 1: 旧目录已清空**

Run: `ls -d 00_inbox Clippings "🚀AIGC" "🌇FrontEnd" "😈Magic" 2>/dev/null`
Expected: 全部"No such file or directory"。

- [ ] **Step 2: 新目录有内容**

```bash
echo "clippings: $(find sources/clippings -name '*.md' | wc -l)"
echo "inbox: $(find sources/inbox -name '*.md' | wc -l)"
echo "posts/aigc: $(find sources/posts/aigc -name '*.md' | wc -l)"
echo "posts/frontend: $(find sources/posts/frontend -name '*.md' | wc -l)"
echo "posts/obsidian: $(find sources/posts/obsidian -name '*.md' | wc -l)"
echo "TOTAL: $(find sources -name '*.md' | wc -l)"
```
Expected: TOTAL ≈ 42 (与 pre-flight 计数对得上，可能 ±1-2 因为基线 commit)。

- [ ] **Step 3: 旧路径 wikilink 全清**

Run: `grep -rn -E '\[\[(00_inbox|Clippings|🚀AIGC|🌇FrontEnd|😈Magic)' . --include="*.md" 2>/dev/null | grep -v docs/superpowers | grep -v "\.git/" | wc -l`
Expected: `0`

- [ ] **Step 4: backlog 计数与实际匹配**

```bash
backlog=$(grep -c '^- \[ \]' migration-backlog.md)
actual=$(find sources -name "*.md" | wc -l)
echo "backlog: $backlog"
echo "actual: $actual"
[ "$backlog" -eq "$actual" ] && echo "✅ 匹配" || echo "❌ 不匹配，需要修复"
```

如果不匹配，修复 backlog 后重 commit。

---

## Smoke Test：跑一次完整 /migrate-next 验证管线

### Task S.1: 端到端冒烟

- [ ] **Step 1: 调用 /migrate-next 处理 backlog 第一条**

在 Claude Code 里输入：`/migrate-next`

- [ ] **Step 2: 验证产物**

```bash
# 应该至少有 1-3 个新 wiki 页面
find wiki -name "*.md" -newer migration-backlog.md | head

# index.md 对应分类应该多了 wikilink
git diff index.md | head

# log.md 末尾应该有一条 [migrate-next | 1/N]
tail -10 log.md

# backlog 第一条应该被勾上
head -20 migration-backlog.md
```

Expected：
- ≥1 个 wiki 页面（含 frontmatter、≥2 wikilink、TL;DR 首段）
- index.md 对应分类多了链接
- log.md 末尾有 `## [...] migrate-next | 1/N`
- backlog 第一条变成 `- [x]` 并附日期

- [ ] **Step 3: 验证 source 没被改**

```bash
git status sources/  # 应该是空的，或者只有 frontmatter sources 字段被回填的（这不应该发生在 source 上，应该在 wiki 上）
```
Expected: `sources/` 下没有 modify。

- [ ] **Step 4: 如果通过，commit smoke test 产物**

```bash
git add wiki/ index.md log.md migration-backlog.md
git commit -m "feat(wiki): smoke test - 首次 migrate-next 管线打通"
```

如果 smoke test 失败：根据失败点回到对应 task 修 ingest.md / migrate-next.md 的 prompt。失败本身就是一个有价值的反馈点。

---

## 完成检查清单（Definition of Done）

- [ ] Pre-flight：working tree 在重构开始前是干净的
- [ ] Phase 0：6 个顶层文件 + 4 个 commands + 11 个目录全部就位
- [ ] AGENTS.md / CLAUDE.md 已是新 schema
- [ ] Phase 1：5 个旧目录全部清空，所有 .md 已迁入 sources/
- [ ] Phase 1：migration-backlog.md 条目数 = sources 实际 .md 数
- [ ] Phase 1：旧路径 wikilink 残留为 0
- [ ] Smoke test：跑过一次 /migrate-next，wiki/ 有产物，index.md/log.md 有更新，sources/ 没动
- [ ] git log 干净有序，每个 task 至少 1 个 commit

完成后，Phase 2 开始：用户日常用 `/migrate-next`、`/lint`、`/query` 自助运营。Phase 3（清理与稳定）等 backlog 跑到 0/N 时再启动。

---

## 失败回滚预案

- Phase 0 出问题：`git reset --hard <Phase 0 起点 commit>`
- Phase 1 单 task 失败：那个 task 是单独 commit，`git revert <commit>` 即可
- Smoke test 暴露 prompt 设计问题：改 `.claude/commands/*.md` 然后再 smoke 一次。Smoke commit 用 `git revert` 撤销，不影响骨架。

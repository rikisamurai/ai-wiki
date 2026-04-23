---
title: ai-wiki README
date: 2026-04-23
---

# ai-wiki

> 一个让维护成本接近零的中文知识库 —— 你产生原料和提问，LLM 负责沉淀和编织。

参考 Karpathy [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 范式，以 Obsidian 为壳，以 Claude Code slash command 为编辑器。

```
sources/  ──/ingest──▶  wiki/   ◀──/query──  你
 (原料)                  (精华)
   ▲                       │
   └── 你只写这里           └── LLM 写 + 自动维护 index.md / log.md
```

## 它跟普通 Obsidian vault 有什么不同

> [!note] 三个角色固定
> 人产原料和提问，LLM 沉淀和编织，slash command 是唯一交互入口。

- **原料和精华严格隔离**：`sources/` 是你的输入区（剪藏、推文、随手草稿），LLM 只读不改；`wiki/` 是经过抽取重组的 atomic 概念页，LLM 才能写。这条边界让"原始上下文"和"沉淀知识"互不污染。
- **元信息自动维护**：[[index]] 是目录、[[log]] 是时间线、`status: draft / stable / stale` 三态自动流转，你不用手动 review。
- **source 路径与 wiki 路径不一一对应**：`sources/` 按"来源"组织，`wiki/` 按"概念域"组织，一个 source 可能产出跨多个 wiki 子域的页面。

## 我现在该干嘛？（按场景找入口）

### 场景 A：剪藏了一篇网页 / 想存一条推文

1. 把内容存到 `sources/clippings/<起个名字>.md`（推荐用 Obsidian Web Clipper，自动扔到 `clippings/`）
2. 在 Claude Code 里跑：
   ```
   /ingest sources/clippings/<起个名字>.md
   ```
3. 完事。LLM 会拆成多个 atomic 概念页写到 `wiki/<domain>/`，自动加 wikilink、frontmatter、更新 [[index]] 和 [[log]]。

### 场景 B：自己想沉淀一段 React / 后端的思考

两条路，看顺手：

**路径 1：先写 → 再 ingest**（推荐，跟外部内容统一流程）

把想法写到 `sources/posts/<domain>/<topic>.md`。`<domain>` 取 `aigc / frontend / obsidian` 之一（按 `sources/posts/` 现有分类），其他主题暂时用 `sources/inbox/`。frontmatter 最小模板：

```yaml
---
title: 标题
date: 2026-04-23
tags: [react, hooks]
---
```

然后跑：
```
/ingest sources/posts/frontend/your-note.md
```

**路径 2：边问边沉淀**（适合零碎念头）

直接：
```
/query 我想搞清楚 React Server Components 的边界
```

LLM 先在 `wiki/` 找；找不到就降级查 `sources/`；如果你觉得答案有沉淀价值，让它反向 ingest 回 `wiki/`。

### 场景 C：想找一个之前记过的东西

```
/query <你的问题>
```

回答优先来自 `wiki/`，引用具体页面（带 wikilink）。`wiki/` 没有相关内容时才会去翻 `sources/` 给你阶段性答案。

### 场景 D：批量导入一堆历史笔记

1. 在仓库根目录创建 `migration-backlog.md`，每行一条 source 路径：
   ```markdown
   # Migration Backlog
   - [ ] sources/posts/frontend/note-1.md
   - [ ] sources/posts/frontend/note-2.md
   - [ ] sources/clippings/article-x.md
   ```
2. 反复跑 `/migrate-next`，每次自动取下一条做 `/ingest`。
3. drain 完整批后归档到 `wiki/_orphans/migration-YYYY-MM/`，删掉根目录的 backlog。

> [!info] 当前 backlog 状态
> 空。2026-04 首批 41 条已 drain，归档于 [[wiki/_orphans/migration-2026-04|migration-2026-04]]。

## 日常维护

每周或每月跑一次：

```
/lint
```

它会自动：
- 把被 ≥3 个 wiki 页 wikilink 引用的 `draft` 升 `stable`
- 把 `last-ingested` 早于 180 天的页改 `stale`
- 报告（不修复）：孤儿页、出链不足、概念重复、真断链、frontmatter 字段非法

报告里需要人工决定的（比如真断链怎么改、孤儿页删不删），看完后直接交给 LLM 修。

平时浏览：
- 打开 [[index]]，里面用 Obsidian Bases 嵌入了"最近更新""按 status 过滤"的动态视图
- 翻 [[log]] 看时间线（`grep '## \[2026-'` 即可按月切片）

## 仓库结构（速览）

```
ai-wiki/
├── README.md           # 你正在看的这份（人类视角操作手册）
├── AGENT.md            # LLM schema（CLAUDE.md 是其符号链接）
├── index.md            # 内容目录 + Bases 视图
├── log.md              # append-only 时间线
├── sources/            # 只读原料区
│   ├── clippings/      # 网页剪藏
│   ├── posts/          # 你写的原创 / 译文
│   ├── inbox/          # 草稿
│   └── asset/          # 图片
├── wiki/               # 可改精华区（按概念域分类）
│   ├── ai-coding/
│   ├── aigc/
│   ├── frontend/
│   ├── obsidian/
│   └── _orphans/       # lint 检测出的孤儿暂存
└── .claude/commands/   # 4 个 slash command 的定义
```

详细 schema、frontmatter 字段、status 流转规则 → 看 [[AGENT]]。

## 命令速查表

| 命令 | 何时用 | 输入 | 输出 |
|---|---|---|---|
| `/ingest <source-path>` | 想把一份原料沉淀进 wiki | `sources/` 下的某个文件 | `wiki/` 下若干新 atomic 页 + index/log 更新 |
| `/query <问题>` | 想查 / 想问，基于已沉淀的知识 | 自然语言问题 | 答案 + 引用的 wiki 页 wikilink；可选反向 ingest |
| `/lint` | 周期性体检 | 无 | 自动改 status；报告其他问题 |
| `/migrate-next` | drain 存量 backlog | 读根目录 `migration-backlog.md` | 取下一条做 `/ingest` |

## 边界 / 注意事项

> [!warning] 三条硬约束
> 1. **不要手改 `sources/`**：原料区是上下文锚点，改了就失去溯源价值。新内容追加成新文件就好。
> 2. **不要直接在 `wiki/` 起新页**：必须经 `/ingest` 才能保证可追溯（frontmatter 里 `sources:` 字段会指回原料）。例外：手改已存在的 wiki 页 OK。
> 3. **不要手动维护 `log.md` / `index.md`**：slash command 自动 append。

其他规范：
- tag 用 kebab-case，每页最多 3 个
- 单页面专注一个概念（atomic），首段 TL;DR，至少 2 个 wikilink 出链
- 笔记用中文，但英文专有名词保留英文（写"Agent"，不写"代理"）
- 详细规范看 [[AGENT]] §wiki 页面规范

## 进阶

- **想改 ingest 的抽取策略 / lint 的检测规则** → 改 `.claude/commands/<cmd>.md`
- **想加新的 status / 新的领域分类** → 改 [[AGENT]]，下次 `/lint` 自动套用
- **想看历史决策** → [[log]] 里 `## [日期] schema |` 开头的条目记录了每次 schema 调整的取舍

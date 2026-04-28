---
title: wiki/ 目录重组设计
date: 2026-04-28
status: draft
---

# wiki/ 目录重组设计

## 背景

ai-wiki 现有 4 个一级目录（`ai-coding/`、`aigc/`、`frontend/`、`obsidian/`）+ `_orphans/`，共 138 个 wiki 页面。当前分类存在三个真问题：

1. **`ai-coding` 与 `aigc` 边界混乱**：`agentic-coding` 在 `ai-coding/`，但 `agentic-rag` / `agent-browser` 在 `aigc/`——同类概念被切到不同一级目录。
2. **`frontend/` 内部杂乱**：27 篇横跨网络协议（5）、React Native（4）、React 模式（5）、UI 库（6）、DOM API（2）、平台/运行时（3）、商业模式（2）；`js-盈利模式分类` 和 `per-seat-licensing` 这两篇明显跟前端无关。
3. **`ai-coding/` 与 `aigc/` 单目录页面数太多**（53 + 38），平铺浏览成本上升。

## 目标

- **浏览友好**：能更快"翻到"想找的页面（按主题更精细切，必要时引入二级目录）
- **ingest 友好**：让 LLM 在 `/ingest` 时更容易判断"新页该放哪"（一级分类边界要清晰、互斥）
- **概念地形图**：让目录本身能反映知识结构

三个目标同等重要（用户已确认）。

## 设计原则

- **必要时下沉**：大主题（≥10 篇）拆出 2-3 个二级目录；小主题（≤20 篇）保持平铺。Tree 不强求均衡，按"内容量决定层级"。
- **按"是讨论 agent 工程通用思想"还是"具体工具产品"划边界**：解决 `ai-coding` / `aigc` 历史混乱。
- **跨工具的资产独立成一级**：Skills 既给 Claude Code 也给 Codex 用，不该藏在 `aigc/` 下。
- **小目录也允许独立**（如 `business/` 仅 2 篇）：边界清晰比拥挤更重要。

---

## §1 完整目录映射

```
wiki/
├── agent-engineering/         53 篇  ← 原 ai-coding 全部 + coordinator-模式
│   ├── philosophy/            19 篇  哲学/范式/思想
│   ├── context/               12 篇  上下文与缓存工程
│   ├── workflow/              18 篇  工作流与 agent 行为模式
│   └── code-review/            4 篇  CR 与 lint
│
├── claude-code/               22 篇  Claude Code & 同类 CLI（平铺）
│
├── skills/                     7 篇  Skills 生态（平铺，独立出来）
│
├── retrieval/                  8 篇
│   ├── rag/                    4 篇
│   └── browser/                4 篇
│
├── frontend/                  25 篇
│   ├── web-platform/           5 篇
│   ├── network/                5 篇
│   ├── react-patterns/         5 篇
│   ├── react-native/           4 篇
│   └── ui-libraries/           6 篇
│
├── business/                   2 篇  js-盈利模式分类 / per-seat-licensing
│
├── obsidian/                  20 篇  保持平铺
│
└── _orphans/                   1 篇  保持现状
```

总计 138 篇，与现状一致，未丢页。

### 各叶节点的具体页面归属

**agent-engineering/philosophy/**（19）
agent-工作量分布、agentic-coding、ai-first-vs-ai-assisted、ai-first-工程前提、ai-first-适用边界、harness-engineering、harness-成熟度、opc-一人公司、plausible-code、spec-coding、vibe-coding、vibe-coding-对-saas-的通缩、vibe-coding-的代价、worse-is-better、yagni-与-dry-反论、架构师-操作员二分、约束悖论、行为正确性、高吞吐合并哲学

**agent-engineering/context/**（12）
cache-keep-alive、cache-命中率、cache-失效陷阱、compact-vs-clear、context-rot、context-window、kv-cache、prefix-cache、会话管理动作、冻结快照模式、稳定前缀-动态后缀、隐性知识与上下文

**agent-engineering/workflow/**（18）
agent-可读性、agent-等待时间、agents-md、coordinator-模式、doc-gardening、enforce-invariants、long-horizon-agent、ralph-loop、rewind-胜过纠正、self-healing-loop、subagent-driven-development、subagent-上下文隔离、writer-reviewer-模式、两次纠正规则、任务三维划分、探索-规划-编码-验证、采访驱动-spec、验证驱动

**agent-engineering/code-review/**（4）
ai-code-review、ai-写-lint、review-带宽瓶颈、shift-left

**claude-code/**（22）
claude-code、claude-code-memory、claude-code-六层架构、claude-rules、claude-health、claude-hud、hooks、settings-scopes、permission-modes、plan-mode、fail-closed-tool-defaults、read-before-edit、inline-edit、handoff-md、kairos-记忆蒸馏、auto-memory、everything-claude-code、opencli、codex、codex-plugin、codex-sandbox-approval、mcp

**skills/**（7）
agent-skills、skill-编写实践、skills-9-分类、skills-marketplace、skills-vs-automations、superpowers、渐进式披露

**retrieval/rag/**（4）
rag、agentic-rag、graph-rag、hybrid-retrieval

**retrieval/browser/**（4）
agent-browser、browser-use、cdp、cdp-能力边界

**frontend/web-platform/**（5）
bun、vercel、webcontainers、mutation-observer、resize-observer

**frontend/network/**（5）
http-3、quic、0-rtt-握手、connection-migration、head-of-line-blocking

**frontend/react-patterns/**（5）
no-useeffect-rule、usemounteffect、key-重置组件、派生状态、组件强制函数

**frontend/react-native/**（4）
flash-list、view-recycling、pressable-vs-touchable、react-native-core-components

**frontend/ui-libraries/**（6）
shadcn-ui、headless-ui、css-scrollbar-styling、overlay-scrollbar-pattern、overlayscrollbars、scrollbar-mock-vs-overlay

**business/**（2）
js-盈利模式分类、per-seat-licensing

**obsidian/**（20，保持平铺）
aliases、block-reference-use-cases、block-reference、callouts、claudian、dataview、defuddle、embed-files、inbox-工作流、json-canvas、knowledge-graph、moc-索引笔记、obsidian-bases、obsidian-cli、obsidian-skills、obsidian-web-clipper、para-方法、templater、wikilink、zettelkasten

**_orphans/**（1，不动）
migration-2026-04

### Judgment Calls（已确认）

| 页面 | 归位 | 理由 |
|---|---|---|
| `coordinator-模式` | `agent-engineering/workflow/` | 是 multi-agent 编排的通用 pattern，不是 Claude Code 独有 |
| `mcp` | `claude-code/` | MCP 是开放协议，但本 wiki 讨论几乎全绑 Claude Code 实践 |
| `handoff-md` | `claude-code/` | Claude Code 的 handoff 文件约定，工具特定 |
| `agents-md` | `agent-engineering/workflow/` | agents.md 跨 agent 通用（Claude/Codex 都用），不该绑死 claude-code |
| `行为正确性` / `架构师-操作员二分` | `agent-engineering/philosophy/` | 是范式而非工序 |

---

## §2 wikilink 重写机制

### 现状勘探

```
wiki/.md 里的 wikilink 形态：
├─ 全路径 [[wiki/<dir>/<file>]]         121 个唯一 × 362 次出现   ← 文件移动时全部会断
└─ 仅文件名 [[<file>]] 或 [[<file>|]]   大量                     ← 不受路径变化影响 ✓

sources/.md → wiki/ 的反向引用：4 处          ← 全在 sources/posts/frontend/libraries/overlayscrollbars.md
wiki/ frontmatter 的 sources: 字段：指向 sources/，不受本次重组影响 ✓
```

仅文件名 wikilink 依赖 Obsidian "vault 内文件名唯一"解析——本次只移动不改名，自动续命。真正要批改的是 121 个唯一全路径 × 362 次出现。

### 选定方案：脚本批改 + git mv（方案 A）

理由：本次改动是"一次性原子重组"，可验证性 > 灵活性；脚本可 dry-run，正则 pattern 单一（`[[wiki/<X>` 后接 `|` 或 `]]`），出错面有限。Obsidian 自动 rename（方案 B）需要 GUI 操作 138 次且难验证；混合方案 C 引入 obsidian-cli 不确定性。

### 4 步骤

```
1. 生成映射表 scripts/wiki-mapping.tsv（旧路径 → 新路径，117 行——obsidian/ 20 篇和 _orphans/ 1 篇原地不动，不进映射；由 §1 表生成）

2. git mv 全部文件（保留 git 历史）
   while read old new; do
     git mv "wiki/$old" "wiki/$new"
   done < scripts/wiki-mapping.tsv

3. 批改 wikilink（单 pass 扫描所有 wiki/**/*.md + sources/posts/frontend/libraries/overlayscrollbars.md）
   for each (old_path, new_path) in mapping:
     替换 [[wiki/<old>]]  → [[wiki/<new>]]
     替换 [[wiki/<old>|   → [[wiki/<new>|

4. 验证（详见 §4 验证清单）
```

### 跨边界处理：sources/ 里的 4 处反向引用

**已授权同步修**（破例改 sources/，理由是修死链不算改语义内容）。4 处全在 `sources/posts/frontend/libraries/overlayscrollbars.md`，全指向 `[[wiki/frontend/<file>]]`，移动后改成 `[[wiki/frontend/ui-libraries/<file>]]` 或对应新桶。

---

## §3 配套文件同步

| 文件 | 影响范围 | 处理 |
|---|---|---|
| `AGENT.md` (CLAUDE.md → AGENT.md 软链) | 2 处提及旧目录名（line 11、42 的目录树） | 手改：列表换新一级目录，目录树同步重画 |
| `.claude/commands/ingest.md` | line 24 写死了"在 ai-coding / aigc / frontend / obsidian 里选" | **重写这一段**——补"二级目录怎么选"的指引（agent-engineering 4 个、frontend 5 个、retrieval 2 个，其余平铺） |
| `.claude/commands/migrate-next.md` / `lint.md` / `query.md` | 不硬编码具体一级目录名 | 不改 ✓ |
| `index.md` | 137 个旧路径 wikilink + 手写的 `## AI Coding` 等分类 header | 内容由 §2 脚本统一批改路径；header 块单独重写为 `## Agent Engineering / ## Claude Code / ## Skills / ## Retrieval / ## Frontend / ## Business / ## Obsidian` |
| `index.base` / `log.base` | 仅用 `file.inFolder("wiki")` + `groupBy: file.folder` 通用过滤 | 不改 ✓ |
| `log.md` | 64 行历史日志含旧路径 | **不改**（保持忠实历史）；顶部加 `> [!warning] 路径迁移` 警告条 |
| `wiki/_orphans/migration-2026-04.md` | 经测无旧路径 wikilink ✓ | 不改 |
| `sources/posts/frontend/libraries/overlayscrollbars.md` | 4 处反向引用 | 同步修（§2 脚本统一处理） |
| `.obsidian/plugins/manual-sorting/data.json` | 280 处路径引用 | **不改**（plugin 内部 state，让其自然过期；用户重拖即可） |

### 决策细节

- **ingest.md 提示写完整**：把 7 个一级目录每个的二级子桶都明示，避免 LLM ingest 时再猜。
- **log.md 顶部警告条全文**：
  ```
  > [!warning] 路径迁移
  > 2026-04-28 完成 wiki/ 目录重组——本日期之前的日志条目里的 wikilink 全路径已过期（仅文件名形式的 [[xxx]] 不受影响）。
  ```
- **AGENT.md 目录树画到一级 + 二级**（不到具体文件名），与现状粒度一致。

---

## §4 执行顺序与原子性

### 核心约束：必须原子

不能"按域分批 commit"。理由：移完 `agent-engineering/` 但还没移 `claude-code/` 时，`agent-engineering/workflow/subagent-driven-development.md` 里的 `[[wiki/aigc/coordinator-模式]]` 就是死链——下一笔 commit 才把 coordinator 移走。这种"中间态有死链"的状态噪音大，code review 也不直观。

mv + wikilink rewrite **必须在同一个 commit 内**。

### 三段提交策略

| # | Commit | 内容 | 回退 |
|---|---|---|---|
| 1 | `chore: 准备 wiki 重组脚本与映射表` | `scripts/reorg-wiki.sh` + `scripts/wiki-mapping.tsv`，不动 wiki 文件 | `git revert` |
| 2 | `refactor: 重组 wiki/ 目录结构（117 文件 mv + 362 wikilink 重写）` | 跑脚本：117 个 `git mv`（obsidian/ 与 _orphans/ 原地不动）+ .md 内 wikilink 替换 + sources/.../overlayscrollbars.md 4 处反向引用修正 | `git revert`（一次还原） |
| 3 | `docs: 同步 schema 与索引到新目录结构` | AGENT.md 目录树、ingest.md 提示、index.md header 重排、log.md 顶部 reorganize 警告 | `git revert`（不影响物理结构） |

拆开 commit 3 是为了让 reviewer 能在不被 commit 2 海量 wikilink 替换噪音淹没的情况下，单独审 schema 语义。

### 执行前提

1. **新建分支 `wiki-reorg-2026-04`**——保护 main，方便随时切回旧结构对比。
2. **关闭 Obsidian app**（或至少关 vault）。Obsidian 的 "Update internal links" 会和脚本抢着改 wikilink。
3. **`git status` 必须干净**——当前有 `.obsidian/plugins/manual-sorting/data.json` modified，先 commit 或 stash。

### 验证清单（commit 2 之后必须 100% 通过）

```bash
# 1. 旧一级目录已不存在
[ ! -d wiki/ai-coding ] && [ ! -d wiki/aigc ]

# 2. 文件总数不变（138 篇）
[ "$(find wiki -name '*.md' | wc -l)" -eq 138 ]

# 3. 没有残留指向旧路径的 wikilink
[ "$(rg '\[\[wiki/(ai-coding|aigc)/' wiki/ sources/ -c | wc -l)" -eq 0 ]

# 4. 没有指向新路径但目标不存在的 wikilink（悬空检测）
#    脚本：每个 [[wiki/X]] 都能 ls 到对应文件
```

### PR 策略

走分支 + PR（即使 self-merge）。理由：commit 2 diff 极大（138 文件 mv + 362 wikilink 替换 = 数千行），用 GitHub 网页的 stat 视图浏览，留 review 痕迹。

---

## §5 风险与回退

### 5 类风险

| # | 风险 | 严重度 | 缓解 |
|---|---|---|---|
| 1 | 归位错（某文件应在另一桶） | 中 | 不 revert；做"修补 commit"挪几个文件即可（仅文件名 wikilink 不破，成本低） |
| 2 | wikilink 漏改（脚本正则未覆盖某种边缘形态） | 中 | §4 验证清单第 3 条是 hard gate；不通过不允许 commit |
| 3 | Obsidian 缓存幽灵（看似死链实为 graph/search index 没刷） | 低 | 重启 vault 一次（关再开），缓存重建后再判断 |
| 4 | manual-sorting 过期（280 处旧路径排序状态失效） | 低 | 已接受；重新拖即可，不影响知识库本身 |
| 5 | 历史 log.md 死链（64 行旧路径不点不开） | 低 | 已接受 + log.md 顶加警告条；想看历史路径用 `git log -- wiki/<old-path>` |

### 软验证（硬验证通过后做）

- Obsidian graph view 目测新结构图是否合理（同二级目录页面应该聚簇）
- 随手点开 5 个枢纽页（`harness-engineering`、`claude-code`、`agent-skills`、`vibe-coding`、`agentic-coding`），确认链接都能跳转

不是 hard gate，但发现问题成本最低。

### 回退总图

```
错的层级    →  回退方式
─────────────────────────────────────
个别归位错  →  修补 commit（移那几个文件）
wikilink 漏 →  脚本调正则，重跑 commit 2
分类大方向有误（§1 整体走偏） →  git revert commit 2 + commit 3，回到分支起点
已 merge 到 main 后才发现 →  在新分支做 revert PR；不 force push
```

---

## Out of Scope

- **仅文件名 wikilink 的二义陷阱**：现状大量 `[[kv-cache]]` 这种 wikilink 靠"vault 内文件名唯一"解析。本次重组不引入新冲突（仅是移动），但深化了对此性质的依赖。将来如果在两个不同二级目录里建了同名 `.md`，仅文件名 wikilink 会变得二义。属于后续治理债，建议加进 `/lint` 检查项（"vault 内文件名重名"作为告警），单独迭代处理。
- **`/ingest` 输出页面的 status 字段**：本次重组不动 frontmatter；`/lint` 的 draft → stable 自动升级逻辑（基于入度）不受影响（因为入度计算用的是仅文件名 wikilink 解析）。
- **PR 走 ultrareview / AI review**：本次 self-merge 即可，不强制走 AI 多 agent review。

## 验证签收

待用户 review 本 spec → 进入 writing-plans → 实施。

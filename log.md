---
title: ai-wiki Activity Log
---

# Log

> [!warning] 路径迁移
> 2026-04-28 完成 wiki/ 目录重组（详见 docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md）。本日期之前的日志条目里的 wikilink 全路径已过期（仅文件名形式的 `[[xxx]]` 不受影响）。想看历史路径用 `git log -- wiki/<old-path>`。

> append-only 时间线，记录所有 ingest / query / lint / migrate-next 操作。
> 格式：`## [YYYY-MM-DD HH:MM] <op> | <subject>`，便于 `grep '## \[2026-'`。

## [2026-05-08 12:38] ingest | Git AI - 追踪 AI 生成代码的 Git 扩展
- 新建 4 页：[[wiki/claude-code/git-ai]]（工具本身）、[[wiki/agent-engineering/workflow/ai-代码-attribution]]（自报 vs 检测的范式判断）、[[wiki/agent-engineering/workflow/git-notes-ai-元数据]]（git notes 作为 AI 工程基础设施）、[[wiki/agent-engineering/philosophy/跨厂商共识协议]]（MCP / Skills / Git AI standard 同源观察）
- 更新 3 页：[[wiki/agent-engineering/workflow/采纳率]]（追加 commit 级 attribution 互补章节）、[[wiki/agent-engineering/workflow/keep-rate]]（追加 attribution 下钻能力章节）、[[wiki/agent-engineering/workflow/continuous-checkpoint]]（追加 commit body vs git notes 的同源对比）
- 概念抽取思路：1 工具页（Git AI）+ 1 度量范式（attribution 自报 vs 检测，与 keep-rate / 采纳率 形成 commit 级 vs in-product 的两个维度）+ 1 基础设施（git notes 作为 AI 元数据载体，跟 continuous-checkpoint 的 commit body 是同源思路）+ 1 哲学层抽象（跨厂商共识协议，把 MCP / Skills / Git AI standard 串成一类东西）
- source: [[sources/posts/aigc/ai-coding/tools/Git AI - 追踪 AI 生成代码的 Git 扩展]]

## [2026-05-08 12:14] ingest | 用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践
- 新建 8 页：[[wiki/agent-engineering/philosophy/人人对齐-人机对齐]]（核心方法论：评测对齐复用到 AI Coding）、[[wiki/agent-engineering/philosophy/ai-加速腐化]]（AI 不会自动收敛复杂度）、[[wiki/agent-engineering/philosophy/经验价值边界]]（从能看全到能判断）、[[wiki/agent-engineering/workflow/专家定向-ai-穷举]]（技术债梳理人机分工）、[[wiki/agent-engineering/workflow/渐进式重构]]（顺带消化技术债）、[[wiki/agent-engineering/workflow/主r打样-sop分发]]（团队规模化 AI Coding 范式）、[[wiki/agent-engineering/workflow/ai-辅助测试-sop]]（5 步 Human-in-the-loop）、[[wiki/agent-engineering/code-review/pre-pr]]（提交前 AI 自审）
- 更新 4 页：[[wiki/agent-engineering/code-review/review-带宽瓶颈]]（追加木桶效应原话 + Pre-PR 出链）、[[wiki/agent-engineering/code-review/cross-model-second-opinion]]（追加美团高阶 judge 低阶 + 多厂商对抗实践）、[[wiki/agent-engineering/code-review/shift-left]]（在左移时机表里插入 Pre-PR 一档）、[[wiki/agent-engineering/philosophy/harness-engineering]]（追加 source 引用，"工程师角色变化"主题对应页）
- 概念抽取思路：3 哲学（人人对齐方法论 / 反直觉腐化 / 经验价值迁移）+ 4 workflow（技术债梳理 / 渐进式重构 / SOP 分发 / 测试 SOP）+ 1 code-review（Pre-PR）；核心命题"先人人对齐再人机对齐"是评测业务方法论复用到 AI Coding 治理；"渐进式重构 + 主 R 打样 SOP"是 31 万行不停业务交付完成重构的两条腿
- source: [[sources/clippings/用Agent评测思路管理AI Coding —— 31万行代码AI重构的实践]]

## [2026-05-06 22:01] fix | index.base 过滤器修正
- 现象：pending-sources 显示已 ingest 的文件，ingested-sources 全空
- 根因：`ingested-at == null` 表达式里 Bases 把字段名 `ingested-at` 解析成了 `ingested - at`（减法），导致比较恒为 null/空
- 修法：两个 view 改用 `file.hasProperty("ingested-at")`，避开表达式解析（带引号的字符串名是函数参数，不再被当成减法）
- 教训：Bases filter 表达式里凡含 `-` 的字段名都要用 `file.hasProperty()` / 引号绕开；推及未来 schema：新加 frontmatter 字段优先用 underscore 而不是 dash 可一劳永逸（但 last-ingested / ingested-at 已用 dash，存量不动）

## [2026-05-06 21:38] schema | sources 加 ingested-at 字段
- AGENT.md（CLAUDE.md）：在"三层架构"+ 新增"sources frontmatter"小节，开放 sources/ 唯一可写字段 `ingested-at`
- .claude/commands/ingest.md：新增第 7 步"回写 source ingested-at"，退出条件与禁止条款同步更新
- index.base：`pending-sources` view 加 filter `ingested-at == null`（真正"待办"清单），新增 `ingested-sources` view 列已消费 sources，properties 加 `ingested-at` 显示
- 存量回填：扫 wiki/**/*.md frontmatter 的 sources 反查映射，给 44 个已被引用的 source 写入 `ingested-at`（取所有引用方 last-ingested 的最大值）；剩余 10 个 source 真未 ingest，自动归入 pending-sources 视图
- 动机：原 pending-sources view 是"所有 sources"误导命名，无法区分待 ingest；现为可直接 filter 的精准视图，无需写反查命令

## [2026-05-06 21:12] ingest | 基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践（得物技术）
- 新建 9 页：[[wiki/agent-engineering/philosophy/mimic-first-harness]]（找模仿对象）、[[wiki/agent-engineering/philosophy/alien-code]]（AI 外星代码反例）、[[wiki/agent-engineering/workflow/codebase-indexing]]（Cursor 代码库语义索引）、[[wiki/agent-engineering/workflow/全栈工作区]]（多仓单 workspace）、[[wiki/agent-engineering/workflow/openspec]]（SDD 指令工作流）、[[wiki/agent-engineering/workflow/sdd-隐性功能陷阱]]（AI 模仿时复刻隐性行为）、[[wiki/agent-engineering/workflow/三阶段联调]]（Mock → 编译 → 联调）、[[wiki/agent-engineering/workflow/subagent-vs-team-模式]]（Claude Code 多 Agent 两种范式）、[[wiki/agent-engineering/workflow/采纳率]]（Acceptance Rate 度量）
- 概念抽取思路：2 哲学（mimic-first / 外星代码）+ 7 workflow（codebase-indexing / 全栈工作区 / openspec / sdd 隐性陷阱 / 三阶段联调 / subagent-vs-team / 采纳率）；mimic-first 是 [[wiki/agent-engineering/philosophy/harness-engineering]] 在战术层的具体形态、外星代码与 [[wiki/agent-engineering/philosophy/plausible-code]] 同族但侧重不同；采纳率与之前的 keep-rate / 语义满意度信号 形成 in-product 度量三件套
- 互链密度：9 页内部成密集网，并外链 [[wiki/agent-engineering/philosophy/harness-engineering]]、[[wiki/claude-code/cursor]]、[[wiki/claude-code/claude-code]]、[[wiki/agent-engineering/workflow/subagent-driven-development]]、[[wiki/agent-engineering/workflow/keep-rate]]、[[wiki/agent-engineering/workflow/agent-evals]]、[[wiki/agent-engineering/workflow/eval-方法矩阵]]、[[wiki/agent-engineering/philosophy/karpathy-四种失败模式]]、[[wiki/retrieval/rag/rag]] 等
- source: [[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]

## [2026-05-06 21:12] ingest | React Native 组件文档站技术栈调研
- 新建 4 页：[[wiki/frontend/react-native/react-native-component-docs-stack]]（决策矩阵与推荐架构）、[[wiki/frontend/react-native/storybook-react-native]]（Web Vite + on-device 双形态）、[[wiki/frontend/react-native/expo-snack]]（reactnative.dev 同款 + 私有包卡点）、[[wiki/frontend/react-native/csf-story-format]]（CSF 3 + TS 写法）
- 概念抽取思路：1 主决策页（选型矩阵 + Expo+Storybook 推荐架构）+ 3 工具/规范页（Storybook RN 双形态、Expo Snack 工具与限制、CSF 写法）；首批 react-native 域从纯组件性能（FlashList / View 回收）扩展到工具链（文档站 + 测试）方向
- 互链密度：4 页内部成网，并外链已有 [[wiki/claude-code/mcp]]（Storybook MCP server）
- source: [[sources/posts/frontend/React/React Native/react-native-doc-site-stack-research]]

## [2026-05-06 20:56] ingest | 持续改进我们的智能体框架（Cursor）
- 新建 9 页：[[wiki/claude-code/cursor]]（项目本体）、[[wiki/agent-engineering/context/dynamic-context]]（动态上下文 vs 静态护栏）、[[wiki/agent-engineering/context/context-anxiety]]（上下文焦虑）、[[wiki/agent-engineering/philosophy/per-model-harness]]（每模型定制框架）、[[wiki/agent-engineering/workflow/cursorbench]]（Cursor 公开 benchmark）、[[wiki/agent-engineering/workflow/keep-rate]]（保留率度量）、[[wiki/agent-engineering/workflow/语义满意度信号]]（LLM 读用户回复推断满意度）、[[wiki/agent-engineering/workflow/工具错误分类法]]（5 类预期错误 + unknown）、[[wiki/agent-engineering/workflow/mid-chat-model-switch]]（聊天中途切模型的工程挑战）
- 概念抽取思路：1 项目页 + 1 哲学（per-model）+ 2 context（dynamic / anxiety）+ 5 workflow（benchmark / 度量 / 错误分类 / 模型切换）；其中度量族（cursorbench / keep-rate / 语义满意度）补强 4-30 那次 ingest 的 [[wiki/agent-engineering/workflow/agent-evals]] 体系
- 互链密度：9 页内部成网，并外链 [[wiki/agent-engineering/philosophy/harness-engineering]]、[[wiki/claude-code/claude-code]]、[[wiki/claude-code/codex]]、[[wiki/claude-code/gstack]]、[[wiki/claude-code/everything-claude-code]]、[[wiki/agent-engineering/workflow/self-healing-loop]]、[[wiki/agent-engineering/context/context-rot]]、[[wiki/agent-engineering/context/compact-vs-clear]]、[[wiki/agent-engineering/context/prefix-cache]]、[[wiki/agent-engineering/workflow/agent-evals]]、[[wiki/agent-engineering/workflow/coding-agent-eval]]、[[wiki/agent-engineering/workflow/eval-grader-三类]]、[[wiki/agent-engineering/workflow/subagent-driven-development]] 等
- source: [[sources/clippings/持续改进我们的智能体框架]]

## [2026-05-06 20:31] ingest | gstack（Garry Tan 的 Claude Code Setup）
- 新建 11 页：[[wiki/claude-code/gstack]]（项目本体）、[[wiki/agent-engineering/workflow/sprint-七阶段范式]]（Think→Plan→Build→Review→Test→Ship→Reflect）、[[wiki/agent-engineering/workflow/specialist-roles-模型]]（多角色专家化）、[[wiki/agent-engineering/workflow/parallel-sprints]]（10–15 并行 sprint + Conductor）、[[wiki/agent-engineering/code-review/cross-model-second-opinion]]（/codex 跨模型复审）、[[wiki/agent-engineering/workflow/design-shotgun]]（mockup→HTML 流水线）、[[wiki/agent-engineering/workflow/continuous-checkpoint]]（WIP commit + 上下文恢复）、[[wiki/retrieval/browser/domain-skills]]（per-site 浏览器记忆）、[[wiki/retrieval/browser/sidebar-agent-prompt-injection-defense]]（多分类器集成防护）、[[wiki/claude-code/gbrain]]（agent 持久知识库）、[[wiki/agent-engineering/philosophy/karpathy-四种失败模式]]（AI coding 四类失败的工作流应对）
- 概念抽取思路：项目页 + 范式（七阶段 / 专家角色 / 并行）+ 工作流（review / build / 持久化 / 浏览器记忆 / 安全）+ 哲学（Karpathy 失败模式）；与已有 [[wiki/claude-code/everything-claude-code]] 形成"Claude Code 完整 setup 双代表"
- 互链密度：11 页内部成密集网，并外链 [[wiki/claude-code/everything-claude-code]]、[[wiki/skills/superpowers]]、[[wiki/agent-engineering/philosophy/harness-engineering]]、[[wiki/agent-engineering/philosophy/plausible-code]]、[[wiki/agent-engineering/workflow/探索-规划-编码-验证]]、[[wiki/agent-engineering/workflow/采访驱动-spec]]、[[wiki/agent-engineering/workflow/writer-reviewer-模式]]、[[wiki/agent-engineering/workflow/long-horizon-agent]]、[[wiki/claude-code/auto-memory]]、[[wiki/claude-code/handoff-md]]、[[wiki/claude-code/mcp]]、[[wiki/retrieval/browser/agent-browser]]、[[wiki/retrieval/browser/cdp]] 等
- source: [[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]

## [2026-05-06 15:58] ingest | Demystifying evals for AI agents
- 新建 11 页：[[wiki/agent-engineering/workflow/agent-evals]]（总览+术语）、[[wiki/agent-engineering/workflow/eval-grader-三类]]、[[wiki/agent-engineering/workflow/capability-vs-regression-eval]]（含 saturation）、[[wiki/agent-engineering/workflow/pass-at-k-vs-pass-power-k]]、[[wiki/agent-engineering/philosophy/eval-driven-development]]、[[wiki/agent-engineering/workflow/读-transcript]]、[[wiki/agent-engineering/workflow/coding-agent-eval]]、[[wiki/agent-engineering/workflow/conversational-agent-eval]]、[[wiki/agent-engineering/workflow/research-agent-eval]]、[[wiki/agent-engineering/workflow/computer-use-agent-eval]]、[[wiki/agent-engineering/workflow/eval-方法矩阵]]
- 概念抽取思路：1 个总览页（术语 + 四类 agent 索引）+ 1 个范式页 EDD（哲学层、与 spec-coding/harness-engineering 同源）+ 4 个核心机制（grader 分类 / capability-vs-regression / pass@k vs pass^k / 读 transcript）+ 4 个 agent-type 专用 eval 范式 + 1 个 Swiss Cheese 方法矩阵
- 互链密度：11 页内部形成密集网，并外链到 [[wiki/agent-engineering/philosophy/harness-engineering]]、[[wiki/agent-engineering/philosophy/spec-coding]]、[[wiki/agent-engineering/philosophy/plausible-code]]、[[wiki/agent-engineering/workflow/agent-可读性]]、[[wiki/agent-engineering/workflow/self-healing-loop]]、[[wiki/retrieval/rag/agentic-rag]]、[[wiki/retrieval/browser/cdp]] 等
- source: [[sources/clippings/Demystifying evals for AI agents]]

## [2026-04-27 13:50] lint-fix | 4 处真问题清零
- 真断链 2 → 0：handoff-md.md 把 `[[wiki/aigc/compact-vs-clear]]` 改正为 `[[wiki/ai-coding/compact-vs-clear]]`；obsidian-skills.md 把演示用的 `[[file]]` 改成 `[[wikilink]]`（依然是教学语义但不再被解析为真链接）
- 出链不足 2 → 1（剩 _orphans 归档不算）：bun.md 加链 → [[wiki/frontend/webcontainers]]；flash-list.md 加链 → [[wiki/frontend/react-native-core-components]]
- 复检：真断链 0，出链不足仅剩 _orphans/migration-2026-04（归档文件，不参与日常 lint）

## [2026-04-27 13:42] lint | weekly check
- 总文件 138；orphans 0；出链不足 3（含 1 个 _orphans 归档）；status 异常 1（_orphans 归档约定 status: done）；stale 候选 0
- **3a 自动升级 8 个 draft → stable**（入度 ≥3）：frontend 5 + obsidian 3
  - frontend: overlayscrollbars (入度 5)、view-recycling (4)、mutation-observer (3)、overlay-scrollbar-pattern (3)、resize-observer (3)
  - obsidian: wikilink (3)、block-reference (3)、obsidian-bases (3)
- §5 真断链 2 处：handoff-md.md → wiki/aigc/compact-vs-clear（应改成 wiki/ai-coding/compact-vs-clear）；obsidian-skills.md → file（疑似演示残留）
- §2 真出链不足 2 处：bun.md、flash-list.md 都只有 1 个 wiki 出链

## [2026-04-27 13:35] ingest | OverlayScrollbars · 隐藏原生滚动条的覆盖层方案
- 新建 6 页：[[wiki/frontend/overlayscrollbars]]（项目本体）、[[wiki/frontend/overlay-scrollbar-pattern]]（范式）、[[wiki/frontend/scrollbar-mock-vs-overlay]]（两派对比）、[[wiki/frontend/css-scrollbar-styling]]（CSS 原生能力）、[[wiki/frontend/resize-observer]] + [[wiki/frontend/mutation-observer]]（两个 Web 平台 API）
- 概念抽取思路：项目页 + 范式页 + 选型对比 + CSS 兜底页 + 两个 Web API 基础设施页，覆盖"为什么用 / 怎么用 / 不用什么 / 底层依赖"四个维度
- 互链密度：6 页之间形成密集 wikilink 网，并外链到既有 [[wiki/frontend/headless-ui]]、[[wiki/frontend/view-recycling]]、[[wiki/frontend/flash-list]]
- source: [[sources/posts/frontend/libraries/overlayscrollbars]]

## [2026-04-23 20:25] query | rsc 是什么？
- 来源：none（wiki/ 和 sources/ 均无实质内容，仅 Vercel DX 段落里一句带过）
- 是否 ingest：no（无原料可抽取；待用户提供 RSC 专题 source 后再 /ingest）

## [2026-04-23 19:21] doc | 新增 README.md（人类视角操作手册）
- 此前根目录只有 AGENT.md（LLM 视角 schema），缺一份给协作者 / 未来自己看的入口
- 场景驱动结构：4 个场景（剪藏 / 自己写 / 查 / 批量迁移）+ 日常维护 + 命令速查 + 边界
- 跟 AGENT.md 互补：README 讲"怎么用"，AGENT.md 讲"怎么改"，互相 wikilink

## [2026-04-23 18:20] lint-fix | 6 处真断链清零
- inbox-工作流.md：3 处 `[[../../.claude/commands/*]]` 改为标准 markdown link `[/cmd](../../.claude/commands/cmd.md)`（Obsidian wikilink 不支持跳出 vault 子树到 dot-folder）
- obsidian-web-clipper.md：`[[../../sources/inbox/]]`（指向目录）改为反引号 `sources/inbox/`；`[[ai-wiki-架构]]`（不存在）改为 `[[AGENT|三层架构]]`；`[[../../.claude/commands/ingest|/ingest]]` 同样改 markdown link
- 复检结果：真断链 0
- 顺手发现脚本两个误报源：①frontmatter 的 sources 字段 wikilink 不应纳入断链扫描（已剥 frontmatter）②`_orphans/` 文件作为目标合法（应纳入 stem_index）

## [2026-04-23 18:10] lint | weekly check + status 自动流转
- 总文件 131；orphans 0；出链不足 0；status 异常 0；stale 候选 0
- **3a 自动升级 67 个 draft → stable**（入度 ≥3）；分布：ai-coding 18 + aigc 27 + frontend 16 + obsidian 6
- 升级后 status 分布：stable 92 / draft 39 / stale 0
- 高入度 top 5：review-带宽瓶颈(17)、agentic-coding(14)、agent-skills(14)、plausible-code(13)、mcp(13)
- 概念重复：17 组高相关关键词全部为同主题集群（cache 系列、vibe-coding 系列、ai-first 系列等），无真重复候选
- 真断链 6 处：obsidian/inbox-工作流 + obsidian-web-clipper 里的 `[[../../.claude/commands/*]]`（Obsidian 解析不了相对 vault 外的路径）+ `[[ai-wiki-架构]]`（不存在）+ `[[../../sources/inbox/]]`（指向目录）

## [2026-04-23 17:55] schema | status 流转改自动切换
- 反悔：上一条定的"人工拍板"改成 /lint 自动改 frontmatter，无需 review
- lint.md 第 3a / 3b 由"报告候选"改为"自动写 frontmatter + 报告变更"；3c 字段非法仍只报告
- lint.md 顶部宣言 + 禁止段：明确 status 字段为唯一自动改的例外
- AGENT.md status 三态描述同步改为"自动切换"
- 影响：下次 /lint 会直接把符合条件的 draft → stable、过期页 → stale，不再问

## [2026-04-23 17:45] schema | status 三态流转规则
- 现状：131 页中 draft 106（80%）/ stable 25 / stale 0；stable 全是早期手工产出，2026-04 批量 migration 后无升级机制
- 根因：ingest 默认写 status: draft，但 schema 没定义如何升级到 stable / 降级到 stale
- 改动：
  - lint.md 第 3 节合并原"过时页面 + status 异常"为"status 流转"，分 3a stable 候选（draft + 入度 ≥3）/ 3b stale 候选（last-ingested > 180d）/ 3c 字段异常
  - AGENT.md wiki 页面规范追加三态流转说明：人工拍板，lint 提候选
  - stale 阈值从原 90d 调整为 180d（90d 对长尾知识太激进）
- 影响：下次 /lint 会输出升级/降级建议清单；status 字段重新有意义

## [2026-04-23 17:30] fix | log.base / index.base 修复
- 病因：①filter 比较表达式没用单引号包裹（YAML 解析后是字面量，过滤失效）②index.base 的 pending-sources view-filter 与全局 filter AND 合并导致空集
- log.base 重构：从"看 log.md 单文件"（无意义）改成跨 wiki/ 的 ingest 时间线（按 last-ingested DESC，limit 100）
- index.base 修法：删全局 filter，三个 view 各自带 filter；统一改用 file.inFolder() 函数取代 startsWith() 字符串匹配
- 影响：两个 .base 现在 Obsidian 里能正常渲染

## [2026-04-23 16:38] fix | CLAUDE.md 符号链接修复
- CLAUDE.md → AGENTS.md（不存在）改为 → AGENT.md
- AGENT.md 内残留 "AGENTS.md / CLAUDE.md" 字样同步更新（line 12 + line 31）
- 影响：Claude Code 现在能正确读到 schema（之前是空文件）

## [2026-04-23 14:55] archive | migration-backlog → _orphans
- migration-backlog.md → wiki/_orphans/migration-2026-04.md（git mv 保留历史）
- 顶部加归档说明：41 总 / 38 ingest / 3 SKIP / 起 2026-04-22 完 2026-04-23
- 同步更新 AGENT.md（顶层目录树 + /migrate-next 描述）、.claude/commands/migrate-next.md（无 backlog 时退出）、wiki/obsidian/inbox-工作流.md 引用
- 后续如有新批次：根目录新建 migration-backlog.md 即可重新驱动 /migrate-next

## [2026-04-23 14:48] lint-fix | clean
- 3 commits（ed7882d / 6550f92 / 348027d）共 12 文件修订
- 复跑结果：orphans 0 / insufficient 0 / real broken 0
- 剩 1 项假阳性（index.base 在 vault 根，工具盲区，不需修）

## [2026-04-23 14:31] lint | weekly check
- 总文件：131；orphans：0；stale：0；status 异常：0
- 出链不足（<2）：4（pressable-vs-touchable / view-recycling / webcontainers / json-canvas）
- 真正需修的断链：5 类（big-ball-of-mud-语料 ×2、radix-attention、wiki/superpowers/using-git-worktrees ×3、wiki/ai-coding/lint、two-agent-编程）
- index.md 假阳性 2（AGENT/index.base 在 vault 根，stem 解析正常）
- 概念重复：无真正候选（共 19 组高相关页面，均为同主题集群非 dupe）
- 详见对话内分项报告

## [2026-04-23 04:45] migrate-next | 39/41 · rag/intro
- 新建：[[wiki/aigc/rag]]、[[wiki/aigc/agentic-rag]]、[[wiki/aigc/graph-rag]]、[[wiki/aigc/hybrid-retrieval]]
- 备注：开 RAG 子域；rag.md 主页 + 三个增强方向页（Agentic / Graph / Hybrid）；多模态 + 模块化 RAG 暂作 rag.md 内的 inline 概念；Agentic RAG cross-link 到 long-horizon-agent / subagent-上下文隔离；GraphRAG cross-link 到 obsidian knowledge-graph
- source: sources/posts/aigc/rag/intro.md

## [2026-04-23 04:25] migrate-next | SKIP 38/41 · browser-use/introduction
- SKIP 原因：仅 26 行外链目录，2 段链接均指向已 ingest 的源（33/41 + 35/41），其余是三个工具官网，无新概念
- source: sources/posts/aigc/browser-use/introduction.md

## [2026-04-23 04:15] migrate-next | 37/41 · OpenCLI/Agent-Browser/Browser-Use 深度横向评测
- 增补：[[wiki/aigc/agent-browser]]（量化基准 -82% Token + 95% 首试成功率 + Cloudflare 软肋）
- 增补：[[wiki/aigc/browser-use]]（83.3% 可靠性 / 113s 平均耗时 / 配 Bright Data 98.44% + 间接 Prompt Injection 80% ASR + CVE）
- 增补：[[wiki/aigc/opencli]]（CDP 端口暴露的安全警告：本地任意进程可绕过同源策略）
- source: sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/OpenCLI、Agent-Browser 与 Browser-Use 深度横向评测.md
- 备注：纯追加补充模式；横向评测主要补 1) 量化基准 2) 安全模型 两大缺角

## [2026-04-23 03:55] migrate-next | 36/41 · 三种浏览器控制流派对比
- 增补：[[wiki/aigc/agent-browser]]（从 stub 扩到完整页：Rust Daemon + Accessibility Tree + Refs + 安全六件套 + 多 Provider + Electron 命名会话 + 反 MCP）
- 增补：[[wiki/aigc/opencli]]（5-Command Pattern + 8 桌面应用 + AppleScript 降级 + 认证级联 PUBLIC→COOKIE→HEADER→BROWSER→CDP）
- 增补：[[wiki/aigc/browser-use]]（Element Index + 视觉 BBox + 三种模式 + Cloud v2/v3 + Skill 系统 + --mcp）
- source: sources/posts/aigc/browser-use/blog/对比OpenCLI、agent-browser、browser-use CLI/AI Agent 的三种浏览器控制流派.md
- 备注：纯追加补充模式；按计划"不再建对比专页"，三流派对比直接落到三页里

## [2026-04-23 03:35] migrate-next | 35/41 · 了解 CDP：browser-use 背后的隐藏功臣
- 增补：[[wiki/aigc/cdp]]（追加 JSON-RPC over WebSocket 协议格式 + Browser/JavaScript Protocol 二分 + Domain 三步式生命周期 + Target × Session 一对多 + AI 写 CDP 翻车 tip）
- source: sources/posts/aigc/browser-use/blog/了解 CDP：browser-use 背后的隐藏功臣.md
- 备注：纯追加补充模式，未新建页面；CDP 主页从"能力边界"维度延伸到"协议机制"维度

## [2026-04-23 03:20] migrate-next | 34/41 · OpenCLI：把网站变成 AI Agent 的 CLI
- 新建：[[wiki/aigc/opencli]]、[[wiki/aigc/agent-browser]]（stub）
- 增补：[[wiki/aigc/browser-use]]（frontmatter sources 追加）
- source: sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具.md
- 备注：OpenCLI 走"LLM 调命令而非看截图"路线；agent-browser 先建 stub，待 36/41 / 37/41 横向评测补全

## [2026-04-23 03:00] migrate-next | 33/41 · CDP 视角下的 Browser 控制边界
- 新建：[[wiki/aigc/cdp]]、[[wiki/aigc/cdp-能力边界]]、[[wiki/aigc/browser-use]]
- source: sources/posts/aigc/browser-use/blog/CDP 视角下的 Browser 控制边界.md
- 备注：建立 CDP 主页 + 能力边界查表 + Browser-Use 主页；后续 35/41 走"追加补充"补 JSON-RPC/Domain/Target 协议细节

## [2026-04-23 02:35] migrate-next | 32/41 · some-skills
- 新建：[[wiki/aigc/claude-health]]、[[wiki/aigc/skills-marketplace]]
- 增补：[[wiki/aigc/claude-code-六层架构]]（claude-health 自动审计示例）
- source: sources/posts/aigc/ai-coding/tools/some-skills.md

## [2026-04-23 02:15] migrate-next | 31/41 · Superpowers
- 新建：[[wiki/aigc/superpowers]]、[[wiki/ai-coding/subagent-driven-development]]
- 增补：[[wiki/ai-coding/subagent-上下文隔离]]（极致用法链接）、[[wiki/ai-coding/采访驱动-spec]]（Superpowers brainstorming Skill）
- source: sources/posts/aigc/ai-coding/tools/Superpowers - AI 编码工作流框架.md

## [2026-04-23 01:50] migrate-next | 30/41 · Codex Best Practices
- 新建：[[wiki/aigc/codex]]、[[wiki/aigc/codex-sandbox-approval]]、[[wiki/aigc/skills-vs-automations]]
- 增补：[[wiki/ai-coding/agents-md]]（Codex 三层 + retrospective）、[[wiki/aigc/skill-编写实践]]、[[wiki/aigc/mcp]]
- source: sources/posts/aigc/ai-coding/codex/Codex Best Practices.md

## [2026-04-23 01:25] migrate-next | 29/41 · claude-code-tools
- 新建：[[wiki/aigc/everything-claude-code]]、[[wiki/aigc/claude-hud]]、[[wiki/aigc/codex-plugin]]
- 增补：[[wiki/ai-coding/writer-reviewer-模式]]（Codex 异系 reviewer）
- source: sources/posts/aigc/ai-coding/claude-code/🛠️claude-code-tools.md

## [2026-04-23 01:05] migrate-next | 28/41 · claude-tips
- 新建：[[wiki/aigc/settings-scopes]]
- 增补：[[wiki/aigc/permission-modes]]（CLI 临时覆盖）、[[wiki/aigc/claude-code]]（frontmatter source）
- source: sources/posts/aigc/ai-coding/claude-code/💡claude-tips.md

## [2026-04-23 00:45] migrate-next | 27/41 · Claude Code 源码深度解析
- 新建：[[wiki/aigc/fail-closed-tool-defaults]]、[[wiki/aigc/read-before-edit]]、[[wiki/aigc/kairos-记忆蒸馏]]、[[wiki/aigc/coordinator-模式]]、[[wiki/ai-coding/agent-工作量分布]]
- 增补：[[wiki/ai-coding/稳定前缀-动态后缀]]（getSystemPrompt 7 段）、[[wiki/ai-coding/subagent-上下文隔离]]（Worker-not-Manager + Fork 占位符）、[[wiki/ai-coding/compact-vs-clear]]（三层压缩 87%）、[[wiki/aigc/auto-memory]]（Sonnet top-5 检索 + KAIROS）、[[wiki/aigc/claude-code]]（OS 类比）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密.md

## [2026-04-22 16:30] init | ai-wiki 重构落地
- 建立 sources/ wiki/ .claude/commands/ 骨架
- 写入 4 个 slash commands
- 改写 AGENTS.md 为 LLM Wiki schema
- 创建 index.md / log.md / migration-backlog.md / *.base

## [2026-04-22 17:30] migrate-next | 1/41 · Agentic Coding 的边界
- 新建：[[wiki/ai-coding/agentic-coding]]、[[wiki/ai-coding/plausible-code]]、[[wiki/ai-coding/yagni-与-dry-反论]]、[[wiki/ai-coding/review-带宽瓶颈]]、[[wiki/ai-coding/隐性知识与上下文]]、[[wiki/ai-coding/worse-is-better]]
- source: sources/inbox/Agentic Coding 的边界.md

## [2026-04-22 17:36] migrate-next | 2/41 · Prefix Cache：Long Horizon Agent 的效率基石
- 新建：[[wiki/ai-coding/prefix-cache]]、[[wiki/ai-coding/kv-cache]]、[[wiki/ai-coding/long-horizon-agent]]、[[wiki/ai-coding/cache-命中率]]、[[wiki/ai-coding/cache-失效陷阱]]、[[wiki/ai-coding/稳定前缀-动态后缀]]、[[wiki/ai-coding/冻结快照模式]]
- source: sources/inbox/Prefix Cache：Long Horizon Agent 的效率基石.md

## [2026-04-22 17:42] migrate-next | 3/41 · 为什么你的"AI 优先"战略可能大错特错？
- 新建：[[wiki/ai-coding/ai-first-vs-ai-assisted]]、[[wiki/ai-coding/harness-engineering]]、[[wiki/ai-coding/vibe-coding]]、[[wiki/ai-coding/ai-first-工程前提]]、[[wiki/ai-coding/ai-first-适用边界]]、[[wiki/ai-coding/self-healing-loop]]、[[wiki/ai-coding/架构师-操作员二分]]
- source: sources/inbox/为什么你的"AI 优先"战略可能大错特错？.md

## [2026-04-22 17:51] migrate-next | 4/41 · 使用 Claude Code：会话管理与 100 万 上下文【译】
- 新建：[[wiki/ai-coding/context-window]]、[[wiki/ai-coding/context-rot]]、[[wiki/ai-coding/会话管理动作]]、[[wiki/ai-coding/compact-vs-clear]]、[[wiki/ai-coding/rewind-胜过纠正]]、[[wiki/ai-coding/subagent-上下文隔离]]
- source: sources/inbox/使用 Claude Code：会话管理与 100 万 上下文【译】.md
- 备注：subagent-上下文隔离 同时引用 source 7（搞懂缓存机制），届时 ingest 7 时复用

## [2026-04-22 17:55] migrate-next | 5/41 · 告别复制粘贴：浏览器一键剪藏到 Obsidian
- 新建：[[wiki/obsidian/obsidian-web-clipper]]、[[wiki/obsidian/inbox-工作流]]
- source: sources/inbox/告别复制粘贴：浏览器一键剪藏到 Obsidian.md
- 备注：obsidian 域首次 ingest，index.md Obsidian 段从占位符切到实链

## [2026-04-22 18:02] migrate-next | 6/41 · 我的 Vibe Coding 项目
- 新建：[[wiki/ai-coding/opc-一人公司]]、[[wiki/ai-coding/vibe-coding-的代价]]
- 更新：[[wiki/ai-coding/vibe-coding]]（加 cross-link 到代价）、[[wiki/ai-coding/架构师-操作员二分]]（加 idoubicc OPC 实证案例）
- source: sources/inbox/我的 Vibe Coding 项目.md

## [2026-04-22 18:15] migrate-next | 7/41 · 搞懂缓存机制，从 Gemma4 到 Claude Code 省 80% Token
- 新建：[[wiki/ai-coding/cache-keep-alive]]
- 更新：[[wiki/ai-coding/kv-cache]]（加 QKV 三角色 + Decoder-only 前提 + Gemma vs Qwen 实验）、[[wiki/ai-coding/prefix-cache]]（加 Claude Code 4-block 内部结构 + 两档 TTL + 断裂检测）、[[wiki/ai-coding/稳定前缀-动态后缀]]（加 DYNAMIC_BOUNDARY 源码佐证）、[[wiki/ai-coding/cache-失效陷阱]]（加第 6 陷阱"切换模型"）、[[wiki/ai-coding/subagent-上下文隔离]]（加 querySource+agentId 源码细节）
- source: sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token.md
- 备注：inbox 全部 7 条 ingest 完毕，下一步进入 posts/* 阶段

## [2026-04-22 18:30] migrate-next | 8/41 · 从投资视角分析 JS 开发者市场
- 新建：[[wiki/frontend/vercel]]、[[wiki/frontend/js-盈利模式分类]]、[[wiki/frontend/per-seat-licensing]]、[[wiki/frontend/headless-ui]]、[[wiki/frontend/shadcn-ui]]、[[wiki/frontend/webcontainers]]、[[wiki/frontend/bun]]、[[wiki/ai-coding/vibe-coding-对-saas-的通缩]]
- 更新：[[wiki/ai-coding/vibe-coding-的代价]]（加 cross-link 到 SaaS 通缩 + frontmatter 加 source）
- source: sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析.md
- 备注：frontend 域首次 ingest，index.md FrontEnd 段从占位符切到实链；posts/frontend 还剩 4 条

## [2026-04-22 18:42] migrate-next | 9/41 · No useEffect：Factory 团队的前端规则
- 新建：[[wiki/frontend/no-useeffect-rule]]、[[wiki/frontend/派生状态]]、[[wiki/frontend/usemounteffect]]、[[wiki/frontend/key-重置组件]]、[[wiki/frontend/组件强制函数]]
- source: sources/posts/frontend/React/Blog/Why we banned React's useEffect.md
- 备注：5 个 React 模式页面全部互链；强制函数 cross-link 到 ai-coding/agentic-coding + plausible-code

## [2026-04-22 18:59] migrate-next | 10/41 · FlashList
- 新建：[[wiki/frontend/flash-list]]、[[wiki/frontend/view-recycling]]
- source: sources/posts/frontend/React/React Native/learning/flash-list.md
- 备注：React Native 域首次 ingest；2 个页面互链

## [2026-04-22 19:05] migrate-next | 11/41 · React Native 核心组件
- 新建：[[wiki/frontend/react-native-core-components]]、[[wiki/frontend/pressable-vs-touchable]]
- source: sources/posts/frontend/React/React Native/learning/react-native-core-components.md
- 备注：核心组件页 cross-link 到 flash-list / view-recycling / pressable-vs-touchable

## [2026-04-22 19:08] migrate-next | SKIP · react-native tips
- SKIP 原因：源文件仅含一条外链（vercel-react-native-skills），无可抽取概念
- source: sources/posts/frontend/React/React Native/react-native tips.md

## [2026-04-22 20:44] migrate-next | 12/41 · HTTP/3 入门指南
- 新建：[[wiki/frontend/http-3]]、[[wiki/frontend/quic]]、[[wiki/frontend/head-of-line-blocking]]、[[wiki/frontend/0-rtt-握手]]、[[wiki/frontend/connection-migration]]
- source: sources/posts/obsidian/HTTP3 入门指南.md

## [2026-04-22 20:46] migrate-next | SKIP · Cross Walls
- SKIP 原因：仅为机场/客户端链接收藏，无可抽取概念，且主题不在 4 个 wiki domain 内
- source: sources/posts/obsidian/🧱Cross Walls.md

## [2026-04-22 20:55] migrate-next | 13/41 · obsidian-quick-start
- 新建：[[wiki/obsidian/knowledge-graph]]、[[wiki/obsidian/templater]]、[[wiki/obsidian/dataview]]、[[wiki/obsidian/para-方法]]、[[wiki/obsidian/zettelkasten]]、[[wiki/obsidian/moc-索引笔记]]
- 备注：Callouts/block-reference/内部链接 留给后续专题 source 各自专门页面
- source: sources/posts/obsidian/obsidian/🚀obsidian-quick-start.md

## [2026-04-22 21:05] migrate-next | 14/41 · Claudian - Obsidian × Claude Code
- 新建：[[wiki/obsidian/claudian]]、[[wiki/aigc/plan-mode]]、[[wiki/aigc/inline-edit]]、[[wiki/aigc/mcp]]、[[wiki/aigc/permission-modes]]
- 备注：aigc/ 首批入驻；Skills/Custom Agents 留给后续专题 source
- source: sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code.md

## [2026-04-22 21:18] migrate-next | 15/41 · obsidian-claude/skills (kepano)
- 新建：[[wiki/aigc/agent-skills]]、[[wiki/obsidian/obsidian-skills]]、[[wiki/obsidian/obsidian-bases]]、[[wiki/obsidian/json-canvas]]、[[wiki/obsidian/defuddle]]、[[wiki/obsidian/obsidian-cli]]
- source: sources/posts/obsidian/obsidian/obsidian-claude/skills.md

## [2026-04-22 21:25] migrate-next | 16/41 · obsidian-callouts
- 新建：[[wiki/obsidian/callouts]]
- 备注：单页面综合 Callout 语法/13 种内置类型/折叠/嵌套/CSS 自定义
- source: sources/posts/obsidian/obsidian/obsidian-tips/obsidian-callouts.md

## [2026-04-22 21:32] migrate-next | 17/41 · block-link-demo
- 新建：[[wiki/obsidian/block-reference]]
- 备注：source 主要是块引用语法演示；下一条 block reference use cases 会补充使用场景页
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/block-link-demo.md

## [2026-04-22 21:38] migrate-next | 18/41 · block reference use cases
- 新建：[[wiki/obsidian/block-reference-use-cases]]
- 更新：[[wiki/obsidian/block-reference]]（frontmatter sources 追加）
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 block reference use cases.md

## [2026-04-22 21:48] migrate-next | 19/41 · 内部链接（Internal Links）
- 新建：[[wiki/obsidian/wikilink]]、[[wiki/obsidian/embed-files]]、[[wiki/obsidian/aliases]]
- 备注：块引用部分已在 17/41、18/41 沉淀，此次不重复
- source: sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 内部链接（Internal Links）.md

## [2026-04-23 00:10] migrate-next | 26/41 · Claude Code 深度使用指南 - HiTw93
- 新建：[[wiki/aigc/claude-code-六层架构]]、[[wiki/aigc/handoff-md]]
- 更新：[[wiki/aigc/mcp]]（追加 MCP 隐形成本 + defer_loading）、[[wiki/aigc/skill-编写实践]]（追加三种类型 + 描述符 token 优化 + auto-invoke 频率分级）、[[wiki/ai-coding/compact-vs-clear]]（追加 Compact Instructions）、[[wiki/aigc/hooks]]（追加三层叠加：CLAUDE.md+Skill+Hook）、[[wiki/aigc/claude-code]]（链接六层架构 + HANDOFF.md）、[[wiki/aigc/claude-code-memory]]（NEVER/ALWAYS 模板 + #追加技巧）、[[wiki/aigc/agent-skills]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93.md
- 备注：本条主要走"追加补充"模式，深度指南扩展 25/41 建立的 CC 主框架

## [2026-04-22 23:35] migrate-next | 25/41 · Claude Code 最佳实践
- 新建：[[wiki/aigc/claude-code]]、[[wiki/ai-coding/验证驱动]]、[[wiki/ai-coding/探索-规划-编码-验证]]、[[wiki/aigc/hooks]]、[[wiki/ai-coding/两次纠正规则]]、[[wiki/ai-coding/writer-reviewer-模式]]、[[wiki/ai-coding/采访驱动-spec]]
- 更新：[[wiki/aigc/claude-code-memory]]、[[wiki/ai-coding/compact-vs-clear]]、[[wiki/ai-coding/rewind-胜过纠正]]、[[wiki/aigc/plan-mode]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践.md
- 备注：建立 wiki/aigc/claude-code.md 主框架页，后续 26/41 深度指南、28/41 claude-tips 走追加补充

## [2026-04-22 23:08] migrate-next | 24/41 · Claude Code Memory 机制详解
- 新建：[[wiki/aigc/claude-code-memory]]、[[wiki/aigc/claude-rules]]、[[wiki/aigc/auto-memory]]
- 更新：[[wiki/ai-coding/agents-md]]（指向 Claude Code 实现）
- source: sources/posts/aigc/ai-coding/claude-code/blog/Claude Code Memory 机制详解.md

## [2026-04-22 22:58] migrate-next | 23/41 · Harness Engineering：Agent-First 时代利用 Codex
- 新建：[[wiki/ai-coding/agent-可读性]]、[[wiki/ai-coding/enforce-invariants]]、[[wiki/ai-coding/doc-gardening]]、[[wiki/ai-coding/高吞吐合并哲学]]
- 更新：[[wiki/ai-coding/harness-engineering]]（追加 Codex 案例 + 关联）、[[wiki/ai-coding/agents-md]]（追加 OpenAI 实证：目录而非百科）、[[wiki/aigc/渐进式披露]]（同原则映射到根目录）
- source: sources/posts/aigc/ai-coding/blog/🤖 Harness Engineering：在 Agent-First 时代利用 Codex.md

## [2026-04-22 22:48] migrate-next | 22/41 · 构建 Claude Code 的经验：如何使用 Skills
- 新建：[[wiki/aigc/skills-9-分类]]、[[wiki/aigc/渐进式披露]]、[[wiki/aigc/skill-编写实践]]
- 更新：[[wiki/aigc/agent-skills]]（追加深入章节，frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/blog/🛠️ 构建 Claude Code 的经验：如何使用 Skills.md

## [2026-04-22 22:38] migrate-next | 21/41 · AI CR 的理想与现实
- 新建：[[wiki/ai-coding/ai-code-review]]、[[wiki/ai-coding/shift-left]]、[[wiki/ai-coding/ai-写-lint]]
- 更新：[[wiki/ai-coding/review-带宽瓶颈]]（frontmatter sources 追加）
- source: sources/posts/aigc/ai-coding/blog/🔍 AI CR 的理想与现实：别让 AI 帮你做 Lint 的苦力！.md

## [2026-04-22 21:57] migrate-next | 20/41 · 从 Spec Coding 到 Harness
- 新建：[[wiki/ai-coding/spec-coding]]、[[wiki/ai-coding/约束悖论]]、[[wiki/ai-coding/ralph-loop]]、[[wiki/ai-coding/agent-等待时间]]、[[wiki/ai-coding/agents-md]]、[[wiki/ai-coding/行为正确性]]、[[wiki/ai-coding/harness-成熟度]]、[[wiki/ai-coding/任务三维划分]]
- 更新：[[wiki/ai-coding/harness-engineering]]（追加约束悖论/反应式生长/三层成熟度等关联，frontmatter sources 追加）、[[wiki/ai-coding/vibe-coding]]（TL;DR 补 Karpathy 出处与"大号 demo"，frontmatter sources 追加）
- 备注：开启 posts/aigc 第一条；OpenClaw / 自定义 Skills / Bytedcli 等留作后续 source 专题
- source: sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结.md

## [2026-04-28 15:16] query | 目前收录了哪些 skill
- 来源：wiki
- 是否 ingest：no（仅为盘点，结论：可在 index.md 补 Skills 全景小节）

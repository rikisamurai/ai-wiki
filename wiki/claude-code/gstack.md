---
title: gstack（Garry Tan 的 Claude Code Setup）
tags: [claude-code, harness, skills-pack]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: draft
---

gstack 是 [Garry Tan](https://x.com/garrytan)（YC President）开源的 Claude Code skills 包——**23 个专家角色 slash command + 8 个 power tool**，把 Claude Code 改造成"CEO + 设计师 + 工程经理 + QA + 安全官 + 发布工程师"的虚拟团队。MIT 协议，定位类似 [[everything-claude-code|Everything Claude Code]] 但更强调"sprint 流水线 + 多角色互审"。

## 核心定位：从工具集到流水线

> [!important] gstack 是流程，不是工具堆
> gstack 的 README 反复强调："**gstack is a process, not a collection of tools**"。23 个 skill 严格按 sprint 阶段（[[sprint-七阶段范式|Think → Plan → Build → Review → Test → Ship → Reflect]]）排列，每一步的产物自动喂给下一步——`/office-hours` 写的 design doc 被 `/plan-ceo-review` 读、`/plan-eng-review` 写的测试矩阵被 `/qa` 拾起、`/review` 抓的 bug 由 `/ship` 验证修复。
>
> "Nothing falls through the cracks because every step knows what came before it."

## 23 角色覆盖一个完整 sprint

参见 [[specialist-roles-模型]] 详细解释多角色互审的范式。粗分如下：

| 阶段 | 角色 | 代表 skill |
|---|---|---|
| Think | YC Office Hours / CEO / Eng Manager / Designer / DX Lead | `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/plan-devex-review` |
| Plan 自动编排 | Review Pipeline | `/autoplan`（CEO → design → eng → DX 全跑） |
| Build | Designer / Design Engineer | `/design-consultation`、`/design-shotgun`、`/design-html` |
| Review | Staff Engineer / Debugger / Designer / Security Officer | `/review`、`/investigate`、`/design-review`、`/cso` |
| Test | QA Lead / DX Tester | `/qa`、`/qa-only`、`/devex-review` |
| Ship | Release Engineer / SRE / Performance / Tech Writer | `/ship`、`/land-and-deploy`、`/canary`、`/benchmark`、`/document-release` |
| Reflect | Eng Manager / Memory | `/retro`、`/learn` |

## 8 个 power tool（横切关注点）

> [!note] 不属于 sprint 主线但常用
> - `/codex`——独立第二意见（[[cross-model-second-opinion]]，调用 OpenAI Codex CLI）
> - `/careful` / `/freeze` / `/guard` / `/unfreeze`——[[fail-closed-tool-defaults|Fail-closed]] 风格的安全护栏
> - `/open-gstack-browser`——sidebar agent 浏览器（含 [[sidebar-agent-prompt-injection-defense|prompt injection 多层防护]]）
> - `/setup-deploy` / `/setup-gbrain` / `/gstack-upgrade`——配置/升级类
> - 标准 CLI 二进制：`gstack-model-benchmark`、`gstack-taste-update`

## 与 [[everything-claude-code|ECC]] 的差异

> [!compare] 同族但取向不同
> | 维度 | gstack | Everything Claude Code |
> |---|---|---|
> | 体量 | 23 skills + 8 power tools，专精 sprint 流程 | 28 subagents + 125+ skills + 60 commands，铺面广 |
> | 主张 | "process not tools"——每个 skill 在 sprint 链路里有明确位置 | "完整 [[claude-code-六层架构|六层架构]] 参考实现"——每层都填满 |
> | 多角色化 | CEO / Designer / EM / QA / CSO 等强 persona | Planner / Architect / Security 等技术 persona |
> | 浏览器 | gstack Browser（自带 sidebar agent + 反爬 + [[domain-skills|domain skills]]） | 不含 |
> | 多工具支持 | 10 个 AI agent（Codex / Cursor / Factory / Slate / Kiro / Hermes / OpenClaw / GBrain / OpenCode / Claude Code） | 跨平台同套 skills |
> | 配套基础设施 | [[gbrain|GBrain]]（持久知识库）、Conductor（[[parallel-sprints|10-15 并行 sprint]]） | PM2 编排 + AgentShield 安全扫描 |
> | 模型理念 | "AI 写大部分代码"，反对 raw LOC 度量 | "Token 优化 + memory persistence + eval" |

两者都是 [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]] 的具体形态——研究"完整 Claude Code 配置长什么样"时建议同时读。

## 安装与命名空间

> [!tip] --prefix vs --no-prefix
> 默认装出来是 `/qa`、`/ship` 这种短名；如果你已经在用别的 skill 包（容易冲突），用 `cd ~/.claude/skills/gstack && ./setup --prefix` 切换为 `/gstack-qa`、`/gstack-ship`。这是 [[claude-code|Claude Code]] skill 包发行需要解决的命名冲突问题，gstack 的处理方式可参考。

支持团队模式：`./setup --team` 把 gstack 锁进 repo 的 `.claude/`（required 模式直接 block 缺失的队友、optional 模式只 nudge）。每个 Claude Code 会话启动时自动检查升级（每小时一次、限速、网络失败安全）。

## 与 [[wiki/agent-engineering/philosophy/yagni-与-dry-反论|YAGNI 反论]] 同构的工具单一职责

每个 skill 只做一件事——`/office-hours` 不写代码、`/qa` 不规划、`/cso` 不做 design review。这是 [[self-healing-loop|Self-Healing Loop]] 那篇里讲的"工具单一职责"原则的另一个实例：**没有哪个 skill 试图包揽一切，组合起来才形成可被 AI 编排的链路**。

## 关联

- 同族：[[everything-claude-code|Everything Claude Code]]、[[wiki/skills/superpowers|Superpowers]]
- 范式：[[sprint-七阶段范式]]、[[specialist-roles-模型]]、[[parallel-sprints]]
- 工具子项：[[gbrain]]、[[domain-skills]]、[[design-shotgun]]、[[continuous-checkpoint]]、[[cross-model-second-opinion]]、[[sidebar-agent-prompt-injection-defense]]
- 反例 / 灵感来源：[[karpathy-四种失败模式|Karpathy 的四种 AI coding 失败模式]]——gstack 的 workflow skill 声称"已经覆盖了这四类"
- 上下游：[[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]、[[wiki/agent-engineering/philosophy/opc-一人公司|OPC（一人公司）]]

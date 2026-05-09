---
title: Sub-agent 纪律（每问一文件 + verdict-first）
tags: [sub-agent, workflow, agent-skills]
date: 2026-05-09
sources:
  - "[[sources/clippings/bgclick-rev-skillbgclick-rev-skill.md at main]]"
last-ingested: 2026-05-09
status: draft
---

[[wiki/skills/bgclick-rev-skill|bgclick-rev]] 这个深度逆向 Skill 在它的 §"Sub-agent discipline" 段沉淀了 5 条铁律：每个 sub-agent 第一动作读 briefing、只拥有一个 question、只写一个文件、文件第一行就是 verdict、不改源码。这是任何"主线程派出 N 个并行 sub-agent 做研究"的 Skill 都可以直接抄的契约——把它从 RE 场景抽出来，本质是给 [[subagent-driven-development|Subagent-Driven Development]]补上"研究型"分支的运行规范。

## 5 条铁律

> [!important] 写在 Skill 正文里给 sub-agent 看
> 1. **第一动作 = 读 `SHARED-CONTEXT.md`**。所有 sub-agent 共用一份 briefing 文档，里面写清楚目标、命名约定、共享背景知识。任何 sub-agent 不读 briefing 就开干 = 上下文割裂的高发场景。
> 2. **每个 sub-agent 只拥有一个 question 或一个 function**。不允许"顺便把另一个问题也答了"——这是 [[subagent-上下文隔离|Subagent 上下文隔离]]从"上下文层面"延伸到"任务层面"的强约束。
> 3. **每个 sub-agent 只产出一个文件**，命名形如 `research/findings/<slug>.md` 或 `research/sub_<addr>-<label>.md`。一个 sub-agent ↔ 一个 question ↔ 一个文件，三者一一对应。
> 4. **输出文件第一行就是一句话 verdict**，证据放后面。这让主线程读 sub-agent 报告时可以"先看结论，按需展开证据"——本质是给主线程做了 [[wiki/agent-engineering/context/context-window|context window]] 优化。
> 5. **Sub-agent 不修改源码，只写研究档**。所有 mutation 留给主线程——和 [[subagent-driven-development|Subagent-Driven Development]]里"主线程负责 review + 决策"对齐。

## 为什么这 5 条会同时出现

> [!compare] 5 条铁律的协同
> | 铁律 | 解决什么 |
> |---|---|
> | 读 SHARED-CONTEXT 优先 | sub-agent 上下文是空白的，必须先注入共享前提 |
> | 一 sub-agent 一 question | 防止 sub-agent 自我扩张任务边界 |
> | 一 sub-agent 一文件 | 给主线程一个稳定的"按文件名 lookup 结论"的 index |
> | Verdict-first | 主线程 review 时不必读完全文 |
> | 不改源码 | 主线程仍是唯一 mutation 入口，避免并行写冲突 |

5 条不是孤立约束，而是一组**让"主线程 = 协调者 + 决策者，sub-agent = 研究者 + 写作者"这个角色二分能稳态运行**的最小契约。少任何一条，要么主线程会被 sub-agent 的不可控行为污染，要么 review 成本会爆炸。

## 与既有 sub-agent 模式的关系

> [!example] 三种 sub-agent 用法 + 对应纪律侧重
> | 模式 | 纪律侧重 |
> |---|---|
> | [[subagent-上下文隔离\|临时派遣]] | 主要靠"返回时只给一段结论"——5 条不是必需 |
> | [[subagent-driven-development\|Subagent-Driven]]（每 plan task 一个） | 用 plan + TDD 控制 sub-agent，5 条里"verdict-first / 一文件"较弱 |
> | **研究型 Skill 内嵌的并行 sub-agent**（本页） | 5 条全部强约束 |

研究型 Skill 的特殊性在于：sub-agent 之间彼此独立、并行启动、产物会被主线程综合成一份 [[wiki/skills/bgclick-rev-skill|FINAL-REPORT]]。这种结构最像"博士导师带 N 个 RA"，纪律契约自然要更严。

## 如何把 5 条搬进自己的 Skill

> [!tip] 抄作业模板
> 在 Skill 正文加一段 §"Sub-agent discipline" 即可：
>
> ```markdown
> ## Sub-agent discipline
>
> - Every sub-agent reads `<workspace>/SHARED-CONTEXT.md` as its first action.
> - Every sub-agent owns exactly one <question | task | function>.
> - Every sub-agent writes exactly one file named `<workspace>/<convention>/<slug>.md`.
> - First line of every output file: one-sentence verdict. Evidence follows.
> - Sub-agents do not modify source code. They only write research docs.
> ```
>
> 关键词替换 `<question>` / `<convention>` 即可适配自己的领域——同样适用于"安全审计 skill"、"性能 profiling skill"、"代码考古 skill"等任何"主线程派多个 sub-agent 做调查"的场景。

---
title: OpenSpec（SDD 指令工作流）
tags: [workflow, spec-driven, sdd]
date: 2026-05-06
sources:
  - "[[sources/clippings/基于 Harness + SDD + 多仓管理模式的 AI 全栈开发实践｜得物技术]]"
last-ingested: 2026-05-06
status: draft
---

OpenSpec 是 [[spec-coding|Spec Coding]] 在 IDE 工具里的指令族落地——把"想 → 做 → 收"三步用 `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` 三个 slash 命令固化下来，配套 explore / verify / archive 等辅助指令。得物文章给出了完整 4 类场景下的指令组合模板。

## 最简形态：想-做-收

> [!important] 极简工作流
> 文章原话：**"想（openspec-propose）、做（openspec-apply-change）、收（openspec-archive-change）"**——三条命令是稳态使用的极简骨架，其它指令按需上。
>
> | 阶段 | 指令 | 产物 |
> |---|---|---|
> | 想 | `openspec-propose "..."` | 设计提案（spec.md / proposal.md / tasks.md） |
> | 做 | `openspec-apply-change` | 按提案执行代码变更 |
> | 收 | `openspec-archive-change` | 归档当前 change，进入下一轮 |

## 4 类典型场景

> [!example] 不同场景的指令组合
> | 场景 | 指令链 |
> |---|---|
> | **入门引导** | `openspec-onboard` → `openspec-continue-change` → `openspec-ff-change` |
> | **A. 初次开发** | `openspec-explore`（调研）→ `openspec-propose`（生成设计）→ `openspec-apply-change`（写代码）→ `openspec-verify-change`（自测）→ `openspec-archive-change`（收尾） |
> | **B. 二次开发 / 修改迭代** | `openspec-explore`（定位旧代码/旧 spec）→ `openspec-propose "修改..."` → `openspec-apply-change` → `openspec-verify-change` → `openspec-archive-change` |
> | **C. 二次修改 + 需求变更** | A 流程 + 中间穿插 `openspec-explore "需求变更：xxx"` → 二次 `openspec-propose` → 重跑 apply/verify → archive |
> | **D. 季度大清理** | `openspec-bulk-archive-change --before 2024-12-31`（批量归档过期 spec） |

## 与 [[spec-coding|Spec Coding]] / [[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]] 的层次

> [!compare] Spec 范式三层
> | 层 | 角色 |
> |---|---|
> | [[spec-coding\|Spec Coding]] | 哲学层——主张"先 spec 后 code" |
> | [[wiki/agent-engineering/workflow/采访驱动-spec\|采访驱动 SPEC]] | 战术层——AI 反过来采访用户填 spec |
> | **OpenSpec** | 工具层——把上面两层固化成可重复执行的 slash 命令 |
>
> OpenSpec 的价值不在于发明新概念，而在于**把流程刚化**——团队成员不会因为忘了顺序而漏跑 verify 或 archive。

## verify-change 的存在意义

> [!important] 自验证 = SDD 的反幻觉机制
> `openspec-verify-change` 的作用：**校验代码与 SDD 文档是否对应**——agent 在 apply 阶段可能漏实现某些 task、或者引入了 SDD 未提及的 [[sdd-隐性功能陷阱|隐性功能]]。verify 是在 archive 前的最后一道关。
>
> 这跟 [[wiki/agent-engineering/workflow/读-transcript|读 transcript]] 同源——**不专门 verify，sdd 完成度不可知**。

## 跟 [[openspec|gstack /office-hours]] 的差异

> [!compare] 两条 spec 路线
> | 维度 | OpenSpec | gstack `/office-hours` + `/autoplan` |
> |---|---|---|
> | 工作单元 | 一个 change（spec 文档 + 代码 + 归档） | 一个 sprint（[[sprint-七阶段范式\|7 阶段]]） |
> | spec 形式 | 显式 markdown（spec.md / proposal.md / tasks.md） | 设计文档喂下游 review 链 |
> | 适合场景 | 中型变更、需要可追溯的 change history | 完整 feature、需要多角色 review |
> | 工具栈 | Cursor + IDE 插件 | Claude Code + skills |

两条路线非互斥——可以在一个 sprint 内跑多个 OpenSpec change。

## 关联

- 上游范式：[[spec-coding]]、[[wiki/agent-engineering/workflow/采访驱动-spec|采访驱动 SPEC]]
- 配套基础：[[全栈工作区]]、[[codebase-indexing]]、[[mimic-first-harness]]
- 下游验证：[[sdd-隐性功能陷阱]]、[[三阶段联调]]
- 同族 sprint 范式：[[sprint-七阶段范式]]、[[gstack]]
- 工具栈：[[cursor]]

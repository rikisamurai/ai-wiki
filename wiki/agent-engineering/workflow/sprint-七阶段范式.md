---
title: Sprint 七阶段范式（Think → Plan → Build → Review → Test → Ship → Reflect）
tags: [workflow, sprint, methodology]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: stable
---

[[gstack]] 提出的 7 阶段 sprint 模板：**Think → Plan → Build → Review → Test → Ship → Reflect**，每一步的产物自动喂给下一步。它是 [[探索-规划-编码-验证|探索-规划-编码-验证四阶段]] 的扩展——把 review、test、ship、reflect 从"实现"中拆出来分别配 [[specialist-roles-模型|专家角色]]。

## 七阶段对照

> [!example] 每个阶段的产物喂给下一步
> | # | 阶段 | 典型 skill | 产物 |
> |---|---|---|---|
> | 1 | **Think** | `/office-hours`（YC 风格强制提问） | design doc（含场景痛点 / 5 个隐性能力 / 3 个实现路径） |
> | 2 | **Plan** | `/plan-ceo-review` / `/plan-eng-review` / `/plan-design-review` / `/autoplan` | 锁定的方案 + 架构图 + 测试矩阵 |
> | 3 | **Build** | `/design-shotgun` + `/design-html`、自由实现 | 代码 + 真实可用的 HTML/CSS |
> | 4 | **Review** | `/review`（Staff Engineer）、`/cso`（安全官）、`/codex`（[[cross-model-second-opinion|跨模型]]） | bug 列表 + 自动修复 + 风险报告 |
> | 5 | **Test** | `/qa`（真浏览器测试 + 自动生成回归测试）、`/devex-review` | 通过的测试 + 新增的回归测试 |
> | 6 | **Ship** | `/ship`、`/land-and-deploy`、`/canary`、`/document-release` | PR、合并、生产验证、文档同步 |
> | 7 | **Reflect** | `/retro`、`/learn` | 周复盘 + 跨会话知识沉淀 |

## 与四阶段的关系

> [!compare] 四阶段 vs 七阶段
> | 维度 | [[探索-规划-编码-验证|探索-规划-编码-验证]] | gstack 七阶段 |
> |---|---|---|
> | 核心动作 | 思考-执行分离 | 思考-执行分离 + 多角色互审 + 文档反馈环 |
> | Review 处理 | 算在"验证"里 | 拆成 `/review` + `/cso` + `/codex` 三类独立 review |
> | Test 处理 | 算在"验证"里 | 拆出 `/qa`（真浏览器）+ `/devex-review`（DX 审计） |
> | Ship 处理 | 不在范围 | 含 `/ship` / `/land-and-deploy` / `/canary` |
> | Reflect | 不在范围 | 显式 `/retro` / `/learn` 沉淀经验 |
>
> **何时升级到七阶段**：当一个人/小队同时跑 [[parallel-sprints|多个并行 sprint]]（≥3 条），四阶段的"探索/规划/编码/验证"容易把 review 和 test 混进编码导致回退；七阶段强制把它们排成显式步骤，每一步可独立检查 readiness。

## "Nothing falls through the cracks"

> [!important] 阶段间的 artifact handoff
> gstack 的关键设计：**每一步的产物自动喂给下一步**。
> - `/office-hours` 的 design doc 喂给所有 `/plan-*-review`
> - `/plan-eng-review` 写的测试矩阵被 `/qa` 拾起
> - `/review` 抓到的 bug 由 `/ship` 验证修复
>
> 这是 [[doc-gardening|Doc Gardening]] 在 sprint 内部的应用——产出的 markdown 文件就是流水线的 message bus。**没有 artifact handoff 的 sprint 范式只是名字游戏**。

## 怎么知道处于哪个阶段

> [!tip] Skill 推荐与 stage 感知
> gstack 的 "Proactive skill suggestions" 会观察你在做什么——brainstorming / reviewing / debugging / testing——然后推荐对应阶段的 skill。这是把"流程感知"做进 [[wiki/agent-engineering/workflow/coordinator-模式|Coordinator 模式]] 的具体方式。

## 跳过阶段的判定

不是每个改动都要跑七阶段。原则跟四阶段一致：

> [!example] 何时跳到中段
> - 修 typo / 改日志 / 重命名变量 → 直接 Build + Test
> - 已有 design doc 的小特性 → 跳过 Think，直接 Plan
> - 已合并 PR 的 hotfix → 直接 Ship + Canary
>
> 经验法则同 [[探索-规划-编码-验证|四阶段]]：**能一句话描述 diff，就跳到 Build**。

## 关联

- 上游范式：[[探索-规划-编码-验证|探索-规划-编码-验证四阶段]]、[[harness-engineering]]
- 多角色拆分：[[specialist-roles-模型]]
- 并行扩展：[[parallel-sprints]]
- 具体 skill 归属：[[gstack]]
- 反例：[[plausible-code]] 在不跑 review/test 时高发

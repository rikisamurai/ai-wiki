---
title: diagnose 系统化调试六步
tags: [debugging, workflow, technique]
date: 2026-05-26
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Matt Pocock Skills - 人类满分工程师的自我蒸馏]]"
last-ingested: 2026-05-26
status: draft
---

`/diagnose` 是 [[wiki/skills/matt-pocock-skills|Matt Pocock Skills]] 里的调试 SOP——把"科学调试法"沉淀成 AI 可执行的六步循环：**复现 → 最小化 → 假设 → 检测 → 修复 → 回归测试**。它的对手是 AI 在没有方向时"乱改一通看哪个能跑"的发散式调试模式。

> [!example] 六步标准化流程
> 1. **复现 (Reproduce)** — 在受控环境下稳定触发 bug；不能稳定复现的 bug 没有资格进调试
> 2. **最小化 (Minimize)** — 删掉与 bug 无关的代码，逼出最小可复现样本（MRE）
> 3. **假设 (Hypothesize)** — 提出**一个**可证伪的根因猜想，写下来
> 4. **检测 (Test)** — 设计能区分"假设成立 / 不成立"的实验
> 5. **修复 (Fix)** — 只针对被验证的根因改，不顺手优化
> 6. **回归测试 (Regression Test)** — 写一个测试覆盖此 bug，纳入 [[wiki/agent-engineering/workflow/tdd-red-green-refactor|TDD]] 套件，防复发

## 为什么 AI 容易跳过这套流程

> [!warning] AI 的默认调试模式 ≈ 盲改
> 没有显式约束时，AI 拿到报错喜欢直接修改它认为"看起来可疑"的代码——常常修复了表象、没修复根因，或者引入新 bug。原因有二：
> - **缺反馈通道**：AI 看不到运行时状态变化，只能从静态代码推测
> - **奖励错配**：训练目标偏向"产出代码看起来合理"，不是"先验证再动手"
>
> 强制走 `/diagnose` 六步等于给 AI 装上**显式的科学方法约束**。

## 与其他调试系框架对比

| 框架 | 来源 | 核心动作 |
|------|------|---------|
| `/diagnose` (Matt Pocock) | Matt Pocock Skills | 6 步线性流程 |
| `systematic-debugging` ([[wiki/skills/superpowers\|Superpowers]]) | obra/superpowers | 假设-实验-验证循环 |
| 工程师常识：二分查找 + git bisect | 经验法 | 二分定位回归引入点 |

> [!compare] /diagnose 与 systematic-debugging 的差异
> `/diagnose` 显式列出"复现"和"最小化"两个前置步骤——更适合**新出现的、未稳定复现**的 bug；`systematic-debugging` 假设你已经能复现，重点在"假设-实验"循环——更适合**已知发生但不知道原因**的场景。两者本质同源，互相是真子集关系。

## 与 [[wiki/agent-engineering/workflow/tdd-red-green-refactor|TDD]] 的衔接

第 6 步"回归测试"直接接到 TDD 循环——bug 复现的 MRE 本身就是一个 [[wiki/agent-engineering/workflow/tdd-red-green-refactor|RED 测试]]，第 5 步的修复让它变 GREEN。这样**每个 bug 都自动增厚测试套件**，下次 AI 重构时这个 bug 不会回来。

## 关联

- 上层：[[wiki/skills/matt-pocock-skills|Matt Pocock Skills]]
- 配套：[[wiki/agent-engineering/workflow/tdd-red-green-refactor|TDD 红绿重构]]、[[wiki/agent-engineering/workflow/验证驱动|验证驱动]]
- 反面：[[wiki/agent-engineering/philosophy/plausible-code|Plausible Code]] —— AI 跳过 diagnose 时的典型产物

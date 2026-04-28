---
title: No useEffect 规则
tags: [react, best-practices, ai-coding]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/React/Blog/Why we banned React's useEffect]]"
last-ingested: 2026-04-22
status: stable
---

Factory 团队前端代码库的一条简单规则：**禁止直接使用 useEffect**。听起来极端，但实践下来代码库更易理解、更难意外破坏。规则通过 lint 强制 + 在 `AGENTS.md` 写给 AI Agent，配合 [[wiki/frontend/react-patterns/usemounteffect|useMountEffect]] 做兜底。

> [!warning] AI 时代为什么更需要这条规则
> 当 Agent 在写代码时，useEffect 经常被"以防万一"地添加，恰恰是下一个竞态条件或无限循环的种子。禁用这个 Hook 迫使逻辑变得**声明式和可预测**——这是 [[wiki/agent-engineering/philosophy/plausible-code|似是而非代码]] 的天然防护栏。

## useEffect 的四类问题

- **脆弱性**：依赖数组隐藏耦合，无关重构悄悄改变 Effect 行为
- **无限循环**：`state 更新 → 渲染 → effect → state 更新`，在依赖列表被逐步"修复"时尤其常见
- **依赖地狱**：Effect 链（A 设置状态触发 B）是基于时间的控制流，难追踪
- **调试困难**：你最终会问"这为什么执行了？"，没有 handler 那样清晰的入口点

React 官方有一篇完整指南：[You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)。

## 5 条替代规则速览

| 规则 | 替代 useEffect 做什么 | 详见 |
| --- | --- | --- |
| 1 | [[wiki/frontend/react-patterns/派生状态\|派生状态]]，而非同步状态 | 直接内联计算 |
| 2 | 用数据请求库（TanStack Query 等） | 处理竞态/缓存/取消 |
| 3 | 事件处理器，而非 Effect | handler 里直接做事 |
| 4 | [[wiki/frontend/react-patterns/usemounteffect\|useMountEffect]] 用于一次性外部同步 | 命名清晰意图 |
| 5 | 用 [[wiki/frontend/react-patterns/key-重置组件\|key 重置]]，而非依赖编排 | 强制干净的重新挂载 |

## 选择你的 bug

> [!compare] 失败模式对比
> | | useMountEffect | 直接 useEffect |
> | --- | --- | --- |
> | 失败模式 | 二元且明显（执行了或没执行） | 逐渐退化，表现为 flaky、性能问题或循环 |
>
> 没有团队能做到零 bug，但你可以选择"明显的失败"还是"潜伏的退化"。

## 如何落地

- **lint 规则**：禁用裸 useEffect，强制走包装
- **AGENTS.md**：给 AI Agent 写清楚替代方案，避免它默认补 useEffect
- **批量修复**：用 Factory Missions 这类工具把存量违规改造成新模式
- **设计层面**：把这条规则当成 [[wiki/frontend/react-patterns/组件强制函数|组件强制函数]]——它推着你写更干净的组件树

**不是反 React，是反"用错 React"**：useEffect 本身没问题，但**默认选它**会让团队从"显式的事件驱动逻辑"滑向"隐式的同步逻辑"。Factory 的禁用本质上是把这个默认值翻转：能不用就不用，必须用时显式包成 useMountEffect。

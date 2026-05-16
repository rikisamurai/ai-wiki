---
title: Freeze-on-First-Read（首读冻结）
tags: [feature-flag, configuration, agent-engineering]
date: 2026-05-16
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/cc-haha-computer-use]]"
last-ingested: 2026-05-16
status: draft
---

**Freeze-on-First-Read** 是一种配置/feature flag 管理模式：某个配置值在被首次读取时立即冻结，之后整个会话生命周期内不再响应远程配置变更。

来源：Claude Code cc-haha 的 `gates.ts` 中，`coordinateMode`（像素坐标 vs 归一化坐标）在首次读取时被 freeze。原因：如果会话中途 GrowthBook 远程标志翻转，模型已经以"像素"为假设调用了多次工具，而 Harness 突然切换到"归一化"模式，会导致坐标解释错乱，引发难以排查的静默错误。

## 实现思路

```typescript
let frozenCoordinateMode: 'pixels' | 'normalized' | undefined

function getCoordinateMode(): 'pixels' | 'normalized' {
  if (frozenCoordinateMode !== undefined) return frozenCoordinateMode
  frozenCoordinateMode = fetchFromGrowthBook('coordinateMode') ?? 'pixels'
  return frozenCoordinateMode
}
```

首次调用之后，`frozenCoordinateMode` 非 undefined，后续所有调用都直接返回缓存值，GrowthBook 的变化不再生效。

## 何时应该用

> [!note] 适用条件
> 1. 配置值改变会导致**同一会话内的前后操作语义不一致**（坐标系、单位、API 版本）
> 2. 会话内部有**隐式的状态积累**（模型已在某个假设下生成了 N 步动作）
> 3. 配置的**变更频率**和**会话的生命周期**在同一时间尺度（远程 AB 实验）

> [!warning] 不适用条件
> - 配置改变是幂等的（如颜色主题、语言设置），改了就改了，无前后一致性问题
> - 短暂的单次调用（无状态积累），每次都读最新值反而更好

## 在 Agent 系统中的意义

Agent 系统里的 feature flag 有个特殊风险：模型在同一个 session 内积累了大量上下文和中间状态。如果 Harness 的行为在会话中途改变（坐标解释、工具参数格式、权限策略），模型的推理会基于错误前提继续运行，而错误可能在很多步后才显现。

Freeze-on-First-Read 是防止这类**上下文前提漂移**的轻量手段，比在每个工具调用都检查是否有 flag 变更简单得多。

## 相关页面

- [[agent-engineering/context/context-rot|Context Rot]] — 配置漂移是上下文腐烂的一种形式
- [[claude-code/computer-use-架构|Computer Use 架构]] — 该模式的来源场景
- [[agent-engineering/philosophy/harness-engineering|Harness Engineering]] — Harness 应保证会话内部的一致性

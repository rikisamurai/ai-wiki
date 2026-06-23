---
title: SPA 冷启动闪现-回退
tags: [react-patterns, spa, performance]
date: 2026-06-17
sources:
  - "[[sources/clippings/把 hydration 从 React UI 里解耦：一次 SPA 启动期边界纠正  静かな森]]"
last-ingested: 2026-06-17
status: draft
---

SPA 冷启动时的特定视觉故障：业务内容先短暂出现（~100ms 闪现），随后退回 loading 状态，再过一两秒才稳定。根因几乎总是持久化数据的 hydration 被绑在 React UI 的生命周期上。解法是 [[wiki/frontend/react-patterns/spa-hydration-decoupling|SPA Hydration 解耦]]。

## 故障机制

```
loading screen → ~100ms 闪现业务 UI → 退回 Suspense fallback → 稳定 UI
```

触发路径：

1. React Provider 挂载，同时启动异步 hydration（打开 IndexedDB）
2. 子树同步挂载，订阅 SWR key，cache 还没回来 → 命中空值 → 触发 fetch
3. 子树跌入 Suspense fallback，UI 回退
4. hydration 完成，cache 注入，Suspense 解析，业务 UI 回归

这个闪现-回退不是偶发抖动，而是**结构性问题**——只要 hydration 的发起时机由 React 调度决定，这条失败链路就会在 cache 尚未就绪的窗口里稳定复现。

## 为什么旧指标发现不了

常见的首屏指标是「`#loading-screen` 节点消失」。但这种指标观察盲区在于：loading-screen 卸下之后，Suspense 完全可以接着进来制造下一次 loading 状态。指标绿了，体感更差。

→ 需要换用 [[wiki/frontend/react-patterns/stable-fmp-metric|稳定业务首屏指标]]，包含连续无回退时间窗口。

## 复现特征

- Electron 包冷启更明显（无浏览器 disk cache 加速）
- 3 次冷启中 2 次可见（LobeHub 实测）
- 与网络无关，是本地 I/O 时序问题

> [!note] 与普通渲染抖动的区分
> 普通渲染抖动是随机的、短暂的像素级变化；闪现-回退是**完整 UI 状态的退化**（业务 UI → Suspense fallback），且几乎每次冷启都在固定阶段复现。

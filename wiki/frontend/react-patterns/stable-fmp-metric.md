---
title: 稳定业务首屏指标
tags: [react-patterns, performance, metrics]
date: 2026-06-17
sources:
  - "[[sources/clippings/把 hydration 从 React UI 里解耦：一次 SPA 启动期边界纠正  静かな森]]"
last-ingested: 2026-06-17
status: draft
---

传统首屏指标（如「`#loading-screen` 消失」）无法捕捉 Suspense 回退，会在 [[wiki/frontend/react-patterns/spa-cold-start-flash|SPA 冷启动闪现-回退]]发生时给出假阳性绿灯。稳定业务首屏指标在 DOM 节点检查之外增加一个**连续无回退时间窗口**，真正度量用户感受到的应用就绪。

## 旧指标的盲区

常见 FMP 定义：「`#loading-screen` 节点不存在」或「`[data-app-loading]` 消失」。

这种指标**无法捕捉 Suspense 回退**：loading-screen 卸下之后，Suspense 完全可以接着进来制造下一次 loading 状态。当 [[wiki/frontend/react-patterns/spa-hydration-decoupling|hydration]] 还在错位时，闪现-回退就发生在这个观察盲区里——指标变绿，体感更差。

## 稳定首屏定义

需同时满足以下条件，且在满足后**连续 1500ms 不回退**：

```
✓ #root 可见
✓ 导航面板出现业务文本
✓ 首页主输入区出现
✓ #root 可见文本达到业务阈值
✓ #loading-screen 不存在
✓ 以上条件满足后连续 1500ms 不回退  ← 关键
```

最后一条把 Suspense 回退捕获进指标定义里——任何「闪现一下」的退化都会被算成未达到。

> [!note] 1500ms 窗口的意义
> hydration 完成到 Suspense 解析通常在数十到数百毫秒内发生。1500ms 窗口足够长以捕捉所有典型回退，又足够短以不影响测试速度。具体阈值可根据项目 I/O 特性调整。

## 基线测量两个陷阱

> [!example] 陷阱一：dev server 不算数
> Vite dev server、HMR、source map、未压缩依赖都会污染指标。必须在**生产构建产物**里测：
> ```bash
> npm run package:local --prefix=./apps/desktop
> ```

> [!example] 陷阱二：worktree 的 node_modules 会跨版本污染
> 直接在当前 worktree 上 `git checkout` 旧分支，`node_modules` 和 workspace symlink 仍指向当前包源代码。用 `git worktree` 开干净环境，独立装依赖：
> ```bash
> git worktree add --detach /tmp/baseline-old origin/canary
> cd /tmp/baseline-old && pnpm install
> ```

## 判断规则

**首屏指标必须能区分「出现」与「稳定」**。如果你的指标在 fallback 回退过程中给出绿灯，它在度量的是加载动画，而不是用户感受到的应用就绪。

---
title: 用 key 重置组件
tags: [react, patterns]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/React/Blog/Why we banned React's useEffect]]"
last-ingested: 2026-04-22
status: stable
---

React 的 `key` prop 不只是 list rendering 用的——它还能强制组件**完全卸载并重新挂载**。这是替代"用 Effect 编排重置逻辑"的干净模式，也是 [[wiki/frontend/no-useeffect-rule|No useEffect 规则]] 的第五条。

> [!example] 反模式 vs 正模式
> ```typescript
> // ❌ BAD: Effect 试图模拟重新挂载行为
> function VideoPlayer({ videoId }) {
>   useEffect(() => { loadVideo(videoId); }, [videoId]);
> }
>
> // ✅ GOOD: key 强制干净的重新挂载
> function VideoPlayer({ videoId }) {
>   useMountEffect(() => { loadVideo(videoId); });
> }
>
> function VideoPlayerWrapper({ videoId }) {
>   return <VideoPlayer key={videoId} videoId={videoId} />;
> }
> ```

**工作原理**：React 用 `(组件位置, key)` 这对值识别组件实例。当 key 变化时：

1. 旧实例完全卸载（state、ref 全部销毁）
2. 新实例从零挂载（[[wiki/frontend/usemounteffect|useMountEffect]] 重新执行）
3. 没有任何"残留"——比 Effect 模拟的"reset state + reload data + cleanup subscriptions"清爽得多

## Smell Test

> [!tip] 看到这两种代码该用 key
> - 你在写一个唯一作用是"当 ID/prop 变化时重置本地状态"的 Effect
> - 你希望组件对每个实体表现得像一个全新实例

## 何时不用 key

- 列表渲染中，key 必须是稳定标识（不能用 index）
- 频繁变化的 key 会让重渲染变成重挂载，性能损耗大——只有真的需要"全新实例"时才用
- 如果只是想清空一两个 state，直接用 [[wiki/frontend/派生状态|派生状态]] 或在事件 handler 里重置更轻量

## 关联

- 配合：[[wiki/frontend/usemounteffect|useMountEffect]]——key 触发的新挂载会重新跑 useMountEffect
- 设计原则：[[wiki/frontend/组件强制函数|组件强制函数]]——父组件用 key 控制子组件生命周期，比 Effect 链清晰得多

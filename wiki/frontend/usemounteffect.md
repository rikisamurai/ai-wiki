---
title: useMountEffect
tags: [react, hooks, patterns]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/React/Blog/Why we banned React's useEffect]]"
last-ingested: 2026-04-22
status: draft
---

`useMountEffect` 是 `useEffect(callback, [])` 的命名包装，用来明确"这是一次挂载时执行的副作用"。它是 [[wiki/frontend/no-useeffect-rule|No useEffect 规则]] 体系下唯一允许的 Effect 用法。

```typescript
function useMountEffect(callback: () => void | (() => void)) {
  useEffect(callback, []);
}
```

> [!note] 命名比实现更重要
> 这个 Hook 的代码就一行，但价值在于**意图明示**：
> - 看到 `useMountEffect` 一眼知道是一次性副作用
> - 看到 `useEffect(..., [])` 还得脑补依赖数组为空的含义
> - lint 规则可以禁用裸 `useEffect` 而放行 `useMountEffect`，强制开发者走显式路径

**适用场景**（必须是与外部世界同步）：

- **DOM 集成**：focus、scroll、measure
- **第三方 widget 生命周期**：jQuery 插件、地图 SDK
- **Browser API 订阅**：`addEventListener`、`MutationObserver`、`IntersectionObserver`
- **一次性外部资源加载**：WebGL context、Canvas 初始化

> [!example] 配合条件挂载——把"是否执行"前置到组件树
> ```typescript
> // ❌ BAD: Effect 内部守卫
> function VideoPlayer({ isLoading }) {
>   useEffect(() => {
>     if (!isLoading) playVideo();
>   }, [isLoading]);
> }
>
> // ✅ GOOD: 前置条件满足后再挂载
> function VideoPlayerWrapper({ isLoading }) {
>   if (isLoading) return <LoadingScreen />;
>   return <VideoPlayer />;
> }
>
> function VideoPlayer() {
>   useMountEffect(() => playVideo());
> }
> ```
>
> 父组件负责"什么时候挂载"，子组件假设"前置条件已满足"。这是 [[wiki/frontend/组件强制函数|组件强制函数]] 的典型应用。

> [!compare] 失败模式更可预测：useMountEffect vs 裸 useEffect
> | | useMountEffect | 直接 useEffect |
> | --- | --- | --- |
> | 触发时机 | 仅一次（挂载时） | 依赖数组任一变化 |
> | 失败模式 | 二元（执行/没执行） | 逐渐退化、flaky |
> | 调试 | 看是否挂载 | 还要追依赖谁变了 |

## 关联

- 上层规则：[[wiki/frontend/no-useeffect-rule|No useEffect 规则]]
- 配合模式：[[wiki/frontend/key-重置组件|key 重置组件]]——用 key 强制重新挂载，让 useMountEffect 重新跑
- 替代方向：[[wiki/frontend/派生状态|派生状态]]——能不用 Effect 就别用

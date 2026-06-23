---
title: SPA Hydration 解耦
tags: [react-patterns, spa, hydration]
date: 2026-06-17
sources:
  - "[[sources/clippings/把 hydration 从 React UI 里解耦：一次 SPA 启动期边界纠正  静かな森]]"
last-ingested: 2026-06-17
status: draft
---

把持久化数据的 hydration（水合）从 React 组件树中提升到 [[wiki/frontend/react-patterns/app-bootstrap-layer|App Bootstrap 层]]，UI 只消费已经准备好的运行时状态，不参与 hydration 的触发决策。这是消除 [[wiki/frontend/react-patterns/spa-cold-start-flash|SPA 冷启动闪现-回退]]的根本修法。

## 问题根因

SWR、React Query、Redux Persist 等需要从持久化存储（IndexedDB、localStorage）水合内存状态的库，最常见的接入位置是 Provider 或根组件的 `useEffect`。这些写法的共同点：**把 hydration 的发起时机绑在 React 内部的调度上**。

两条本该分开的时间轴被强行绑死：

- **hydration 时间轴**：由持久化层的 I/O 决定（IndexedDB 打开、读取、注入）
- **React 渲染时间轴**：由 Provider 挂载、effect 运行、子树 commit 决定

UI 成了 hydration 的隐式触发器，闪现-回退迟早出现。

> [!example] 典型失败链路
> 1. React 渲染 Provider，Provider 启动 hydration（异步打开 IndexedDB）
> 2. 子树同步挂载，订阅 SWR key
> 3. cache 还没回来，订阅命中空值，触发 fetch，子树跌入 Suspense fallback
> 4. hydration 完成，cache 注入，子树再次解析，业务 UI 回归
>
> 用户看到：业务内容闪一下，又退回 loading。

## 解耦方案

hydration 放到 [[wiki/frontend/react-patterns/app-bootstrap-layer|App Bootstrap 层]]，**在 `createRoot` 之前发起**；React tree 通过一个原子 gate（如 Jotai atom）决定「业务 UI 什么时候可以显示」，而不决定「什么时候开始水合」。

```ts
// bootstrap.ts
export const startAppInitialization = () => {
  if (started) return;
  started = true;

  startSWRCacheScopeSync();         // 同步提升为 app 级 singleton
  startImportSettingsFromUrl();
  registerBuiltinToolSurfaces();    // 显式注册，避免 import 副作用

  void initializeApp()
    .catch((error) => {
      console.error('[SPA Initialize] failed', error);
    })
    .finally(() => {
      flushSync(() => {
        setAppReady(true);          // 原子 gate 切换，flushSync 保证同帧
      });
      startPostRenderInitialization();
    });
};
```

SWR Provider 只消费 singleton cache，不再决定时机：

```ts
export const appSWRCacheProvider = swrCacheProvider(getCacheScope);

export const hydrateAppSWRCache = async (): Promise<void> => {
  await appSWRCacheProvider.hydrateScope?.();
};
```

> [!note] `flushSync` 为何必要
> `flushSync(() => setAppReady(true))` 保证 ready 状态在同一个微任务内同步切换，避免「ready 已设但下一帧才渲染」造成的可见空白。

## 判断规则

看到任何把 hydration 写进 Provider / `useEffect` / 子树挂载流程里的代码，先问：这份数据的「可用时刻」是不是被这段 UI 代码的「挂载时刻」隐式决定了？如果是，UI 就成了 hydration 的隐式触发器。

**Hydration 不属于 React UI；它属于 app bootstrap，UI 只消费结果。**

## 实测收益（LobeHub Electron）

| 指标 | 改造前 | 改造后 |
| --- | --- | --- |
| 稳定业务首屏中位数 | 2615.8 ms | 1465.8 ms（**-44%**） |
| 业务内容闪现后回退 | 2 / 3 次 | 0 / 3 次 |

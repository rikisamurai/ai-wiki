---
title: App Bootstrap 层
tags: [react-patterns, spa, initialization]
date: 2026-06-17
sources:
  - "[[sources/clippings/把 hydration 从 React UI 里解耦：一次 SPA 启动期边界纠正  静かな森]]"
last-ingested: 2026-06-17
status: draft
---

App Bootstrap 层是 SPA 中在 `createRoot` 之前建立的显式初始化层，负责持久化数据水合、全局注册等与 React 渲染无关的工作，是 [[wiki/frontend/react-patterns/spa-hydration-decoupling|SPA Hydration 解耦]]的关键落点。

## 核心原则

Bootstrap 层与 React render 层是**两条并行的时间轴**，通过一个原子 gate 协调可见性——不是串行依赖。

> [!compare] 错误 vs 正确
>
> ❌ **串行（错误）**：async I/O 占用主线程时，React 模块求值被完全阻塞
> ```ts
> await initializeApp();          // IndexedDB 打开 + 读取 50-200ms
> createRoot(root).render(<App />); // React 解析排到 I/O 之后
> ```
>
> ✅ **并行（正确）**：两条线同时跑，hydration 完成后用 flushSync 切换可见性
> ```tsx
> startAppInitialization(); // 同步返回，内部 void 异步任务
>
> const router = createAppRouter(webRoutes);
>
> createRoot(document.getElementById('root')!).render(
>   <ThemeProvider>
>     <RouterProvider router={router} />
>   </ThemeProvider>,
> );
> ```

**「不显示」≠「不解析」**。React tree 在 hydration 没完成时就开始解析，路由、布局、provider 全部就位；只有 AppLayer 按 `appReady` 原子决定渲染 loading screen 还是业务子树。

## 两条并行流

| 流 | 内容 |
| --- | --- |
| I/O 线 | IndexedDB 打开、cache 读出、塞回 in-memory map |
| CPU 线 | React 模块求值、router 构建、provider chain 解析 |

Hydration 完成的微任务里 `flushSync(() => setAppReady(true))`，业务 UI 直接出现，**不额外等待任何帧**。

## 职责边界

Bootstrap 层应该承接：
- 持久化数据 hydration（[[wiki/frontend/react-patterns/spa-hydration-decoupling|SPA Hydration 解耦]]）
- 全局 registry 的显式注册（避免 [[wiki/frontend/react-patterns/import-side-effects-hazard|import 副作用隐患]]）
- URL 参数导入（`startImportSettingsFromUrl`）
- 渲染后才启动的任务（`startPostRenderInitialization`）

**不该**承接：路由定义、UI 逻辑、React state 管理。

## 判断规则

任何 bootstrap 阶段都要问：这段 `await` 期间，React tree 是否本可以同时被解析？能并行的工作，不要串行。「等待」与「串行」是两件事；「可见性」也不等于「解析」。

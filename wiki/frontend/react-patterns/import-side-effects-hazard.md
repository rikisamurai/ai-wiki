---
title: Import 副作用隐患
tags: [react-patterns, bundler, module-graph]
date: 2026-06-17
sources:
  - "[[sources/clippings/把 hydration 从 React UI 里解耦：一次 SPA 启动期边界纠正  静かな森]]"
last-ingested: 2026-06-17
status: draft
---

模块顶层做全局注册（map push、订阅、registry 写入），使运行时正确性隐性依赖 bundler 的模块求值顺序。当 [[wiki/frontend/react-patterns/app-bootstrap-layer|App Bootstrap 层]]的 import 顺序改变时，原本被掩盖的循环依赖（TDZ 问题）会立刻浮出水面。

## 反模式：import 时做注册

```ts
// 子包顶层——反模式
import { surfaceRegistry } from '@/registry';
surfaceRegistry.register('my-tool', { /* ... */ }); // import 时写入全局 map

export const myExecutor = () => { /* ... */ };
```

调用方只需要 `import './my-tool'`，注册自动发生。看起来优雅，实际把**模块图的求值顺序变成了运行时正确性的一部分**。

> [!example] TDZ 错误案例
> LobeHub 解耦动作刚跑起来，控制台立刻给出：
> ```
> Uncaught ReferenceError: Cannot access 'AgentManagerRuntime' before initialization
>     at executor.ts:40:17
> ```
> 根因：模块 A 顶层引用了模块 B 顶层的 `const`，B 又链回 A——B 求值时 A 还没把那个 `const` 写进 module record。原本可工作，仅因为 React tree 内部的 import 顺序碰巧让 A 先求值完成；解耦换了 entry，环就浮出来。

**动态 import 是伪修法**：`const mod = await import('./my-tool')` 只把炸点推后，副作用仍然挂在模块顶层，触发时间不等于所有权。另一条调用路径在更早时间点拉进同一包，TDZ 又回来了。

## 正确做法：显式注册函数

```ts
// 子包：副作用退到函数体内
import { surfaceRegistry } from '@/registry';

export const registerMyTool = () => {
  surfaceRegistry.register('my-tool', { /* ... */ });
};

export const myExecutor = () => { /* ... */ };
```

```ts
// app bootstrap：一处统一调度
import { registerMyTool } from '@lobechat/my-tool/register';

export const registerBuiltinToolSurfaces = () => {
  registerMyTool();
  // ... 其他显式注册
};
```

「谁负责注册」和「何时注册」都变成一阶问题，不再由 bundler 求值顺序间接决定。

## 识别规则

看到一个包顶层有**非纯计算**（数组 push、map set、订阅注册、副作用函数调用），立刻问：

1. 这件事谁拥有？
2. 什么时候应该发生？

把答案落在显式函数里，而不是 import 行为里。这条规则对任何会被 bundler 重排序的代码都适用，不限于 SPA 启动期。

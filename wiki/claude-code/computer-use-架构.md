---
title: Computer Use 架构与 MCP 借壳模式
tags: [computer-use, claude-code, mcp]
date: 2026-05-16
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/cc-haha-computer-use]]"
last-ingested: 2026-05-16
status: draft
---

Claude Code 的 Computer Use 工具链有一个反直觉的设计：**MCP server 是个幌子**。`setup.ts` 把 Computer Use 注册为 `type: 'stdio'` 的 MCP server，但 `command/args` 从未被真正 spawn——`client.ts` 按 server 名称拦截，直接走进程内的 `bindSessionContext` 派发函数。

> [!note] 为什么要"借壳"MCP
> 1. 让 `mcp__computer-use__*` 工具名出现在 `allowedTools` 里，跳过权限弹窗（CU 有自己的 `request_access` 流程）
> 2. 让 API backend 检测到 `mcp__computer-use__*` 前缀，触发系统 prompt 注入 `COMPUTER_USE_MCP_AVAILABILITY_HINT`
>
> 这种"复用 MCP 协议的工具命名约定，但实际派发在进程内"的模式可以称为 **MCP 借壳模式**。

## 完整派发链路

```
模型发出 mcp__computer-use__screenshot
  ↓
client.ts（Claude Code 内核）
  ↓
wrapper.tsx → getComputerUseMCPToolOverrides(toolName).call(args, context)
  ↓
bindSessionContext（上游包 @ant/computer-use-mcp）的 dispatcher
  ├─ 锁检查 → computerUseLock.ts（O_EXCL 文件锁）
  ├─ 权限检查 → ComputerUseApproval（React 弹窗，setToolJSX + Promise）
  ├─ 调用 hostAdapter.executor[xxx]
  │     ↓（cc-haha 替换层）
  │     executor.ts → callPythonHelper(command, payload)
  │     ↓
  │     pythonBridge.ts → execFile python3 mac_helper.py command --payload {...}
  │     ↓
  │     runtime/mac_helper.py（pyautogui/mss/AppKit）
  └─ 返回 MCP 内容块 → 转 Anthropic API base64 image block
```

## wrapper.tsx 的核心设计

`wrapper.tsx`（444 行）是整个链路的胶水层，解决了一个关键问题：**dispatcher 需要跨调用持久化状态（如截图 blob），但 `ToolUseContext` 是 per-call 的**。

```typescript
let binding: Binding | undefined          // 进程级缓存，跨调用持久化
let currentToolUseContext: ToolUseContext | undefined  // per-call，每次 call 更新

function tuc(): ToolUseContext {
  return currentToolUseContext!  // 所有回调通过此 ref 取最新 context
}
```

**模块级 let + per-call ref** 是有意为之的桥接模式：dispatcher 闭包需要进程级缓存，但 context（abortController、setToolJSX）是 per-call 的。

## setToolJSX + Promise 权限弹窗模式

```typescript
return await new Promise<CuPermissionResponse>((resolve, reject) => {
  const signal = context.abortController.signal
  if (signal.aborted) { reject(...); return }
  const onAbort = () => reject(new Error('aborted'))
  signal.addEventListener('abort', onAbort)

  setToolJSX({
    jsx: React.createElement(ComputerUseApproval, {
      request: req,
      onDone: resp => { signal.removeEventListener('abort', onAbort); resolve(resp) },
    }),
    shouldHidePromptInput: true,
  })
})
```

这是 Claude Code 内置的同步交互范式——工具调用过程中渲染 React 组件等待用户确认，并正确处理 abort 信号（防止 Ctrl+C 后 hang）。

## MCP 借壳模式的适用场景

当你需要：
1. 某个工具名出现在 MCP 命名空间里（以便触发系统 prompt 注入或特殊处理逻辑）
2. 但实际执行逻辑在进程内（性能要求高，或需要访问进程内状态）

可以注册一个 `type: 'stdio'` 的假 MCP 配置，在 client 层按 server 名称拦截并转发到进程内实现。

## 相关页面

- [[computer-use-lock|Computer Use 跨进程文件锁（O_EXCL）]]
- [[mac-computer-use|Mac Computer Use 架构（视觉 + AX + 事件 + 权限）]]
- [[cc-haha|cc-haha 项目概述]]
- [[mcp|MCP（Model Context Protocol）]]

---
title: cc-haha 的 Computer Use 实现拆解
tags:
  - claude-code
  - computer-use
  - ai-coding
date: 2026-05-15
source-url: https://github.com/NanmiCoder/cc-haha/tree/fd1617522c15e3acc95db21f0d57516db014a45d/src/utils/computerUse
source-commit: fd1617522c15e3acc95db21f0d57516db014a45d
---

# cc-haha 的 Computer Use 实现拆解

> [!abstract] 是什么
> [cc-haha](https://github.com/NanmiCoder/cc-haha) 是基于 2026-03-31 从 Anthropic npm registry 泄露的 Claude Code 源码二次修复的"桌面端 Claude Code 工作台"。原版 Claude Code 是终端工具，没有窗口，Computer Use 走 Anthropic 内部的 Swift/Rust 原生模块（`@ant/computer-use-mcp`）。cc-haha 用一套 Python 子进程桥接（pyautogui + mss）替换掉原生模块，把 Computer Use 跑通在它的 Tauri 桌面壳里。`src/utils/computerUse/` 这个目录就是这个替换层。

> [!info] 上游依赖
> 这个目录里所有文件都依赖 `../../vendor/computer-use-mcp/`——那是 Anthropic 内部包 `@ant/computer-use-mcp`，它定义了 `ComputerExecutor`、`ComputerUseHostAdapter`、`ComputerUseSessionContext` 等接口，并提供了核心调度器 `bindSessionContext` 和 `createComputerUseMcpServer`。cc-haha 不重写调度器，只重写"宿主适配层"。

## 整体架构

模型调用 Computer Use 工具的链路：

```
模型发出 mcp__computer-use__screenshot
  ↓
client.ts (Claude Code 内核)
  ↓
wrapper.tsx getComputerUseMCPToolOverrides(toolName).call(args, context)
  ↓
bindSessionContext (上游包) 的 dispatcher
  ├─ 锁检查 (checkCuLock / acquireCuLock → computerUseLock.ts)
  ├─ 权限检查 (onPermissionRequest → React 弹窗 ComputerUseApproval)
  ├─ 调用 hostAdapter.executor[xxx]
  │     ↓
  │     executor.ts → callPythonHelper(command, payload)
  │     ↓
  │     pythonBridge.ts → execFile python3 mac_helper.py command --payload {...}
  │     ↓
  │     runtime/mac_helper.py 或 win_helper.py (pyautogui/mss/AppKit)
  └─ 返回 MCP 内容块 → 转 Anthropic API base64 image block
```

关键点：**MCP server 是个幌子**。`setup.ts` 里把 MCP config 注册成 `type: 'stdio'`，但 `command/args` 实际从未被 spawn——`client.ts` 按 server 名拦截，直接走进程内 `bindSessionContext` 派生的 `dispatch` 函数。MCP 这层存在主要是为了让 API backend 看到 `mcp__computer-use__*` 工具名，从而注入 `COMPUTER_USE_MCP_AVAILABILITY_HINT` 到系统 prompt。

## 文件总览

```
src/utils/computerUse/  (22 files, ~115KB)
├── 入口 / 注册
│   ├── setup.ts                  # 注册假 MCP config + allowedTools
│   ├── mcpServer.ts              # 子进程 --computer-use-mcp 入口（仅 ListTools）
│   └── wrapper.tsx (444 lines)   # 真正的 .call() 派发器，胶水层
├── 适配 / 执行
│   ├── hostAdapter.ts            # ComputerUseHostAdapter 单例
│   ├── executor.ts               # ComputerExecutor 实现，全部委托给 Python
│   ├── pythonBridge.ts           # venv bootstrap + execFile 调度
│   ├── inputLoader.ts            # 占位：原生 input 模块的 stub（throw）
│   ├── swiftLoader.ts            # 占位：原生 Swift 模块的 stub
│   └── drainRunLoop.ts           # 占位：CFRunLoop pump 的 no-op 替换
├── 状态 / 锁
│   ├── computerUseLock.ts        # ~/.claude/computer-use.lock 文件锁
│   └── cleanup.ts                # turn 末尾 unhide + 释放锁
├── 配置 / 权限
│   ├── gates.ts                  # GrowthBook 'tengu_malort_pedway' + env 开关
│   ├── permissions.ts            # macOS Accessibility / ScreenRecording 归一化
│   ├── preauthorizedConfig.ts    # ~/.claude/cc-haha/computer-use-config.json
│   └── escHotkey.ts              # 占位：CGEventTap 全局 Esc no-op
├── 工具元信息
│   ├── common.ts                 # 平台能力声明 + 终端 bundleId 探测
│   ├── appNames.ts               # 已安装应用名过滤（为模型生成提示）
│   └── toolRendering.tsx (17KB)  # 工具调用 React 渲染层（最大文件）
└── 测试 (4 个 .test.ts)
```

## 关键模块拆解

### 1. setup.ts —— 注册"假"MCP server

```ts
// setupComputerUseMCP() 返回
{
  mcpConfig: {
    'computer-use': {
      type: 'stdio',
      command: process.execPath,     // 自己的可执行文件
      args: ['--computer-use-mcp'],   // 永远不会真的被执行
      scope: 'dynamic',
    }
  },
  allowedTools: ['mcp__computer-use__screenshot', ...] // 直接放行
}
```

注释明确说："command/args are never spawned — client.ts intercepts by name and uses the in-process server"。意思是这套配置只是为了：

1. 让 MCP 工具名出现在 `allowedTools` 里，跳过权限弹窗（CU 自己有 `request_access`）
2. 让 API backend 检测到 `mcp__computer-use__*` 前缀，从而触发系统 prompt 注入 CU 提示

这是一种"借壳上市"——复用 MCP 协议的工具命名约定，但实际派发完全在进程内。

### 2. wrapper.tsx —— 进程内派发器

整个目录最关键的文件（444 行）。核心结构：

```ts
let binding: Binding | undefined          // 进程级缓存
let currentToolUseContext: ToolUseContext | undefined  // 每次 call 更新

function tuc(): ToolUseContext {
  return currentToolUseContext!  // 所有回调通过这个 ref 取最新 context
}

// 模块级 let 是有意为之：dispatcher 闭包要持久化截图 blob，
// 但 ToolUseContext 是 per-call 的——用 ref 桥接两边。
```

`buildSessionContext()` 返回一大堆 getter/setter，把 cc-haha 的 `appState.computerUseMcpState` 映射到 `@ant/computer-use-mcp` 期望的 `ComputerUseSessionContext` 接口：

| 接口方法 | 实现 |
|---|---|
| `getAllowedApps` / `getGrantFlags` | 读 `appState.computerUseMcpState.allowedApps/grantFlags` |
| `onPermissionRequest` | 弹 React `ComputerUseApproval` 组件，await Promise |
| `onAllowedAppsChanged` | 持久化到 appState（包内已 dedupe） |
| `onScreenshotCaptured` | 把 dims 缓存到 appState 供下一次坐标换算 |
| `checkCuLock` / `acquireCuLock` | 委托给 `computerUseLock.ts` |
| `onAppsHidden` | 记录被 hide 的 bundleId，turn 末尾 unhide |
| `onDisplayPinned` / `onResolvedDisplayUpdated` | 多显示器选中态 |

权限弹窗的实现细节值得抄：

```ts
return await new Promise<CuPermissionResponse>((resolve, reject) => {
  const signal = context.abortController.signal
  if (signal.aborted) { reject(...); return }   // 防止 Ctrl+C 后 hang
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
// finally: setToolJSX(null)
```

是 `setToolJSX + Promise` 的标准模式（注释里说和 `spawnMultiAgent.ts:419-436` 的 `It2SetupPrompt` 一样）。

桌面端模式还有个 `runDesktopPermissionDialog` 走 `CC_HAHA_DESKTOP_SERVER_URL` 的 HTTP 桥——把弹窗委托给 Tauri 主进程。如果失败 fallback 回 `setToolJSX`。

### 3. computerUseLock.ts —— O_EXCL 文件锁

`~/.claude/computer-use.lock` 单文件锁，保证多个 Claude Code 会话不会同时操控同一台机器。锁内容：

```ts
{ sessionId: string, pid: number, acquiredAt: number }
```

核心是用 `writeFile(lockPath, data, { flag: 'wx' })`（即 `O_EXCL`）做原子 test-and-set。检查链路：

1. 尝试 O_EXCL 创建——成功就 fresh acquire
2. 失败说明已有锁，读出来：
   - 同 sessionId → reentrant
   - 不同 sessionId 但 PID 还活（`process.kill(pid, 0)`）→ blocked
   - 不同 sessionId 且 PID 死了 → stale，unlink 后重试 O_EXCL
3. 注册 `cleanupRegistry` 兜底——`/exit` 中途也能释放

`checkComputerUseLock` 是 `request_access` / `list_granted_applications` 这类"只查不锁"工具用的——避免它们触发"进入 CU 模式"的通知。

> [!note] PID 复用窗口
> 注释明确承认 stale 检测有 PID 复用的小窗口（owner 死了同时新进程拿到同 PID），实践中"极不可能"。不做 fcntl advisory lock 的原因是要保留跨进程感知能力。

### 4. pythonBridge.ts —— Python venv 自举

每次 `callPythonHelper(command, payload)` 都会：

1. `ensureBootstrapped()`（懒加载 + Promise 缓存）
   - 把 `runtime/mac_helper.py` 和 `runtime/requirements.txt` 同步到 `~/.claude/.runtime/`（每次都覆盖，避免 stale）
   - 如果 venv 不存在，`python3 -m venv ~/.claude/.runtime/venv`
   - 校验 `requirements.txt` 的 sha256，变了就 `pip install -r`，使用清华源
2. 然后 `execFileNoThrow(pythonBin, [helperPath, command, '--payload', JSON.stringify(payload)])`
3. 解析 stdout 的 `{ ok, result, error }` JSON

值得抄的细节：

- **国内源**：`PIP_INDEX_URL = 'https://pypi.tuna.tsinghua.edu.cn/simple/'` 写死。这是给国内用户开箱即用做的妥协
- **Windows 编码**：调 Python 时强制 `PYTHONIOENCODING=utf-8` 和 `PYTHONUTF8=1`，避免 GBK 乱码
- **可配 Python 路径**：`preauthorizedConfig.ts` 的 `pythonPath` 字段，可以指定系统已有的 Python 解释器
- **依赖摘要 stamp**：`requirements.sha256` 文件，命中就跳过 pip install——大幅缩短二次启动

性能影响：每次工具调用都 fork 一个 Python 子进程。对一次性的 click/key 还能接受（~50ms 启动开销），但 `screenshot` 之类涉及大数据返回的会有压力。原版 Swift/Rust 模块是 Node N-API 直接调用，无进程边界，差异很大。

### 5. executor.ts —— ComputerExecutor 适配

接口大约 20 个方法，全部 thin wrapper 到 `callPythonHelper`：

- 输入类：`click / mouseDown / mouseUp / drag / moveMouse / scroll / key / holdKey / type`
- 截图类：`screenshot / zoom / resolvePrepareCapture` （经过 `targetImageSize` 计算目标分辨率，JPEG quality 0.75）
- 显示器：`getDisplaySize / listDisplays / findWindowDisplays`
- 应用：`getFrontmostApp / appUnderPoint / listInstalledApps / listRunningApps / openApp`
- 剪贴板：`readClipboard / writeClipboard`

特别精彩的是 `typeViaClipboard`：

```ts
async function typeViaClipboard(text: string): Promise<void> {
  let saved: string | undefined
  try { saved = await readClipboard() } catch {}
  try {
    await writeClipboard(text)
    if (process.platform === 'darwin') {
      await sleep(40)         // NSPasteboard 落盘
      await callPythonHelper('paste_clipboard', {})
      await sleep(180)         // 等 Electron/WebView 字段消费
    } else {
      await callPythonHelper('key', { keySequence: 'ctrl+v', repeat: 1 })
      await sleep(100)
    }
  } finally {
    if (typeof saved === 'string') {
      try { await writeClipboard(saved) } catch {}  // 还原原剪贴板
    }
  }
}
```

`hide before action`、`mouse animation`、`prepare for action`（隐藏所有窗口）这些原版有的功能在 cc-haha 都退化成 no-op 或简化版——Python pyautogui 没那么细的 API。

### 6. gates.ts —— 双层开关

```
CLAUDE_COMPUTER_USE_ENABLED env (硬开关)
       ↓
GrowthBook 'tengu_malort_pedway' (远程配置)
       ↓
ChicagoConfig {
  enabled, pixelValidation, clipboardPasteMultiline,
  mouseAnimation, hideBeforeAction, autoTargetDisplay,
  clipboardGuard, coordinateMode
}
```

`coordinateMode` 在第一次读取时被 freeze（避免会话中途 GB flag 翻转造成"模型以为是 pixels 但实际按 normalized 转"的不一致）。这种 freeze-once-at-first-read 模式值得抄。

注：代号 `chicago` / `tengu_malort_pedway` 是 Anthropic 内部 codename，泄露源里直接保留了。`malort` 是芝加哥的一种利口酒。

### 7. preauthorizedConfig.ts —— 桌面端预授权

`~/.claude/cc-haha/computer-use-config.json`，桌面端在 Settings 里勾选过的应用、剪贴板/系统快捷键 grant flags、自定义 Python 路径都存在这里。

`wrapper.tsx` 的 `loadPreAuthorizedApps()` 在第一次工具调用时把这些 app inject 进 appState，之后 `getAllowedApps()` 直接命中——模型不需要再走一遍 `request_access` 流程。

这是相对原版 CLI 的一个**桌面端独有增强**：CLI 模式没有持久化授权列表的概念，每次会话都要重授权。

### 8. 占位文件们

- `escHotkey.ts`：原版用 macOS CGEventTap 注册全局 Esc 键来 abort——cc-haha 用 Python 跑，没法做这件事，全部 no-op。回退到 Ctrl+C
- `drainRunLoop.ts`：原版 Swift 模块要在 Node 主线程跑 CFRunLoop pump，cc-haha 的 Python 是同步子进程，no-op
- `inputLoader.ts` / `swiftLoader.ts`：原版的 native module 加载点，throw `'Native input module replaced by Python bridge'`

这些"功能性退化"的注释清楚交代了取舍——值得作为案例理解"用解释型语言桥接换实现成本"的代价。

### 9. cleanup.ts —— turn 末尾收尾

每次会话 turn 结束（自然结束 / abort streaming / abort tools 三个入口）调用：

1. 把 `prepareForAction` hide 的 app 重新 unhide（5s 超时）
2. 反注册 Esc hotkey（占位实现，no-op）
3. 释放 `computerUseLock`，发 OS 通知"Claude is done using your computer"

`isLockHeldLocally()` 是个 zero-syscall 的本地标记，让非 CU turn 不会触碰磁盘。

## 值得抄进 wiki 的几个点

1. **MCP 借壳模式**：把 MCP server config 当作"工具命名 + 系统 prompt 注入"的载体，实际派发走进程内闭包。`setup.ts` 是范例
2. **dispatcher 模块级 let + per-call ref**：跨调用持久化（截图 blob）+ per-call context（abortController、setToolJSX）的桥接模式。`wrapper.tsx` 顶部的 `binding` + `currentToolUseContext` + `tuc()`
3. **O_EXCL 跨进程协作锁**：`writeFile(path, data, { flag: 'wx' })` + PID 探活 + stale 恢复，单文件实现可重入、可恢复的多进程互斥
4. **Python venv 自举**：sha256 stamp 跳过 pip install、镜像源、UTF-8 编码、可配 Python 路径——这套模式可以套用在任何"Node 项目要嵌 Python"的场景
5. **freeze-on-first-read 的 feature flag**：`gates.ts` 的 `coordinateMode` 防止会话中途 flag 翻转造成不一致
6. **setToolJSX + Promise 模式**：mid-call 渲染 React 弹窗等用户输入，并正确处理 abort 信号，是 Claude Code 内置的同步交互范式
7. **clipboard-based type**：要解决 IME / Electron 输入框打字慢的标准做法，并要兼顾原剪贴板还原。可以和 [[💡claude-tips]] 里其他技巧并列

## 和原版 / 同类项目的对照

| 维度 | 原版 Claude Code | cc-haha | Anthropic Cowork（桌面端） |
|---|---|---|---|
| 输入/截图 | Swift/Rust native module | Python pyautogui + mss | Swift native |
| 全局 Esc | CGEventTap | 无（Ctrl+C 替代） | CGEventTap |
| 权限弹窗 | TUI（setToolJSX） | TUI + 桌面端 HTTP 桥 | Electron 主进程 |
| 锁 | 同（O_EXCL 文件锁） | 同 | N/A（单进程） |
| 预授权应用 | 无 | 桌面端 Settings 持久化 | 有 |
| MCP server | 假 stdio | 假 stdio | 自建工具数组 |
| 跨平台 | macOS only | macOS + Windows | macOS only |

cc-haha 在权限弹窗和预授权两块上**比原版做了更多**——是为了适配 Tauri 桌面壳，把这些状态外化给图形 UI。

## 适合派生的 wiki 页面方向

- `wiki/claude-code/computer-use-architecture.md`：MCP 借壳 + 派发链路
- `wiki/claude-code/computer-use-lock.md`：O_EXCL 跨进程锁实现
- `wiki/claude-code/python-bridge.md`：Node 嵌 Python venv 的自举模式
- `wiki/agent-engineering/feature-flag-freeze.md`：freeze-on-first-read 模式
- `wiki/agent-engineering/cli-react-prompt.md`：setToolJSX + Promise（如果还没有）
- `wiki/claude-code/cc-haha-overview.md`：cc-haha 项目本身的定位（泄露源 + 桌面端壳 + Python 桥）

## 相关链接

- 仓库：https://github.com/NanmiCoder/cc-haha
- 本次拆解的 commit：`fd1617522c15e3acc95db21f0d57516db014a45d`
- 目录：`src/utils/computerUse/`
- 上游接口（vendored）：`src/vendor/computer-use-mcp/`（即 Anthropic 内部包 `@ant/computer-use-mcp`）
- Anthropic Computer Use 官方介绍：https://www.anthropic.com/news/3-5-models-and-computer-use

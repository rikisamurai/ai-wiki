---
title: cc-haha（Claude Code 桌面端工作台）
tags: [computer-use, claude-code, open-source]
date: 2026-05-16
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/cc-haha-computer-use]]"
last-ingested: 2026-05-16
status: draft
---

cc-haha 是基于 2026-03-31 从 Anthropic npm registry 泄露的 Claude Code 源码二次修复的**桌面端 Claude Code 工作台**。原版 Claude Code 是终端工具，cc-haha 用 Tauri 壳套了一层图形界面，并用 Python 子进程桥接（pyautogui + mss）替换掉 Anthropic 内部的 Swift/Rust 原生 Computer Use 模块。

> [!note] 项目定位
> - 仓库：https://github.com/NanmiCoder/cc-haha
> - 泄露源 commit：`fd1617522c15e3acc95db21f0d57516db014a45d`
> - 替换目标：`src/vendor/computer-use-mcp/`（即 `@ant/computer-use-mcp` 内部包）
> - 替换实现：`src/utils/computerUse/`（22 文件，约 115KB）

## 与原版的核心差异

| 维度 | 原版 Claude Code | cc-haha |
|---|---|---|
| 输入/截图 | Swift/Rust native module（N-API，无进程边界） | Python pyautogui + mss（子进程 fork，~50ms 开销） |
| 全局 Esc 键 | macOS CGEventTap 注册 | no-op（退化为 Ctrl+C） |
| 权限弹窗 | TUI（setToolJSX + Promise） | TUI + Tauri 桌面端 HTTP 桥 |
| 预授权应用 | 无（每次会话重授权） | 桌面端 Settings 持久化（`~/.claude/cc-haha/computer-use-config.json`） |
| 跨平台 | macOS only | macOS + Windows |

**核心取舍**：用 Python 解释型语言桥接换取实现成本降低，代价是每次工具调用多一次子进程 fork，`screenshot` 等大数据返回场景压力较大。

## 架构亮点

cc-haha 引入了几个工程上值得借鉴的模式：

1. **[[computer-use-架构|MCP 借壳模式]]** — 注册假 `stdio` MCP 配置，从不真正 spawn，只用于工具命名和系统 prompt 注入
2. **[[computer-use-lock|O_EXCL 跨进程文件锁]]** — `~/.claude/computer-use.lock`，防止多个 Claude Code 会话并发操控同一台机器
3. **Python venv 自举** — sha256 stamp 跳过 pip install、清华镜像源、UTF-8 编码、可配 Python 路径
4. **[[agent-engineering/workflow/freeze-on-first-read|freeze-on-first-read feature flag]]** — `coordinateMode` 在首次读取时冻结，防止 GrowthBook 远程配置中途翻转造成不一致

## 相关页面

- [[computer-use-架构|Computer Use 架构与 MCP 借壳模式]]
- [[computer-use-lock|Computer Use 跨进程文件锁]]
- [[mac-computer-use|Mac Computer Use 架构（视觉 + AX + 事件 + 权限）]]
- [[agent-engineering/workflow/freeze-on-first-read|freeze-on-first-read feature flag]]

---
title: Claude Code 常用命令
tags:
  - ai-coding
  - claude-code
  - cheatsheet
date: 2026-03-16
---

# Claude Code 常用命令

> [!abstract] 概览
> Claude Code 常用命令速查表，涵盖启动、会话管理、斜杠命令、CLI 参数等。

## 基础启动

```bash
claude                    # 启动交互式 REPL
claude "query"            # 直接提问，完成后退出
claude -p "query"         # 纯文本模式（无交互 UI，适合管道）
claude -p "query" --json  # JSON 输出模式
```

## 管道输入

```bash
cat file.py | claude "review this code"           # 管道输入文件内容
git diff | claude -p "summarize these changes"     # 管道输入 diff
```

## 会话管理

```bash
claude --resume            # 恢复上一次会话
claude --continue          # 继续上一次会话（不确认直接继续）
```

## 常用斜杠命令

在交互式会话中输入：

| 命令 | 说明 |
|------|------|
| `/help` | 查看帮助信息 |
| `/clear` | 清空当前上下文（释放 token） |
| `/compact` | 压缩对话历史，保留关键信息 |
| `/cost` | 显示当前会话的 token 消耗和费用 |
| `/model` | 切换模型（如 sonnet、opus、haiku） |
| `/vim` | 切换 vim 编辑模式 |
| `/permissions` | 查看和管理工具权限 |
| `/config` | 打开配置设置 |
| `/bug` | 报告 Bug |
| `/quit` | 退出 Claude Code |

> [!tip] 自定义斜杠命令
> 在项目根目录创建 `.claude/commands/` 文件夹，添加 Markdown 文件即可注册自定义命令。例如 `.claude/commands/review.md` 会注册为 `/project:review`。

## CLI 配置与管理

```bash
claude config list                    # 列出所有配置项
claude config set theme dark          # 设置主题为暗色
claude config set preferredNotifChannel terminal  # 通知方式
```

## MCP Server 管理

```bash
claude mcp list                       # 列出已配置的 MCP Server
claude mcp add <name> <command>       # 添加 MCP Server
claude mcp remove <name>              # 移除 MCP Server
```

## 权限模式

```bash
claude --dangerously-skip-permissions  # 跳过所有权限检查（CI/脚本用）
claude --allowedTools "Edit,Write"     # 只允许指定工具
```

> [!warning] 注意
> `--dangerously-skip-permissions` 仅用于非交互式环境（如 CI/CD），日常使用请勿开启。

## 多实例与后台运行

> [!info] 并行工作
> 可以在不同终端窗口启动多个 Claude Code 实例，分别处理不同任务。配合 Git worktree 使用效果更佳，避免文件冲突。

## 实用技巧

- **Shift + Tab**：在输入框中切换自动接受编辑的模式
- **`#`**：在输入中使用 `#` 引用文件路径，Claude 会自动读取
- **`@`**：引用文件或文件夹
- **拖拽图片**：直接拖拽图片到输入框，Claude 可以分析图片内容
- **Escape 两次**：快速退出当前操作

## 相关笔记

- [[Claude Code 最佳实践]]
- [[Claude Code Memory 机制详解]]
- [[Claude Code 深度使用指南 - HiTw93]]

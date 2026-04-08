---
title: Claude Code 工具推荐
tags:
  - claude-code
  - ai-coding
  - tool
date: 2026-03-25
---

# Claude Code 工具推荐

汇总 Claude Code 生态中实用的周边工具。

## Claude HUD

Claude Code 的 statusline 插件，基于原生 statusline API，无需 tmux 或额外窗口，在终端输入区域下方实时显示会话状态，包括：

| 信息 | 说明 |
| --- | --- |
| **Context 健康度** | 可视化进度条，绿→黄→红，提前预警上下文即将耗尽 |
| **Usage 限额** | 订阅用户的速率限制消耗情况（5h / 7d） |
| **Tool 活动** | 实时显示 Claude 正在读取、编辑、搜索哪些文件 |
| **Agent 追踪** | 查看 subagent 运行状态及耗时 |
| **Todo 进度** | 任务完成进度追踪 |

**效果示例：**

```
[Opus] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

### macOS 安装

> [!info] 前置条件
> - Claude Code v1.0.80+
> - Node.js 18+ 或 Bun

在 Claude Code 中依次运行：

```bash
# 1. 添加 marketplace
/plugin marketplace add jarrodwatts/claude-hud

# 2. 安装插件
/plugin install claude-hud

# 3. 配置 statusline
/claude-hud:setup
```

安装完成后**重启 Claude Code** 即可生效。

### 自定义配置

运行 `/claude-hud:configure` 进入交互式配置，可选择预设方案：

- **Full** — 全部信息开启（tools、agents、todos、git、usage 等）
- **Essential** — 活动信息 + git 状态
- **Minimal** — 仅显示 model 名称和 context 进度条

也可直接编辑 `~/.claude/plugins/claude-hud/config.json` 进行高级配置。

**项目链接：** [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud)

## Everything Claude Code

AI Agent harness 性能优化系统，由 Anthropic Hackathon 获奖者开发，GitHub 50K+ stars。不仅仅是配置集合，而是一套完整的 Agent 工作流体系，涵盖 skills、agents、memory 优化、持续学习、安全扫描等，支持 Claude Code、Codex、Cursor、OpenCode 等多平台。

### 核心组件

| 组件 | 数量 | 说明 |
| --- | --- | --- |
| **Agents** | 28 | 专用 subagent（planner、architect、TDD guide、security reviewer 等） |
| **Skills** | 125+ | 覆盖前后端、多语言（TS/Python/Go/Java/Kotlin/Rust/C++ 等）、TDD、安全审查等 |
| **Commands** | 60 | `/plan`、`/security-scan`、`/harness-audit`、`/multi-execute` 等 |
| **Rules** | 多语言 | 按 `common/` + 语言目录组织，按需安装 |

### 亮点功能

- **持续学习** — 自动从会话中提取模式，生成可复用 skills
- **AgentShield** — 内置安全扫描，1282 项测试、102 条规则
- **多 Agent 编排** — PM2 管理 + multi-plan/multi-execute 命令
- **Token 优化** — model routing、strategic compact、memory persistence
- **Verification Loop** — checkpoint 与持续验证，确保代码质量
- **跨平台** — 支持 macOS / Linux / Windows，自动检测包管理器

### 安装

在 Claude Code 中运行：

```bash
# 1. 添加 marketplace
/plugin marketplace add affaan-m/everything-claude-code

# 2. 安装插件
/plugin install everything-claude-code@everything-claude-code

# 3. 安装 rules（插件无法自动分发 rules，需手动）
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
npm install
./install.sh typescript    # 按需选择语言：python / golang / swift / php
```

> [!tip]
> 安装后可用 `/everything-claude-code:plan "Add user authentication"` 等命令快速上手。

### 配套指南

- **精简指南（从这里开始）：** [The Shorthand Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2012378465664745795)
- **详细指南（高级）：** [The Longform Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2014040193557471352)

| 指南 | 内容 |
| --- | --- |
| **Shorthand Guide** | 安装、基础概念、设计哲学（推荐先读） |
| **Longform Guide** | Token 优化、memory 持久化、eval、并行化 |
| **Security Guide** | 攻击向量、沙箱、sanitization、CVE、AgentShield |

**项目链接：** [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

## Codex Plugin for Claude Code

把 Codex 接到 Claude Code 里的插件，适合已经习惯在 Claude Code 中工作，但希望临时调用 Codex 做 code review、对实现方案做压力测试，或者把某个排障/修复任务委派出去的场景。

### 什么时候适合用

- **只读代码审查** — 用 `/codex:review` 看当前未提交改动，或对比 `main` 做一次独立复审
- **挑战当前方案** — 用 `/codex:adversarial-review` 专门质疑实现方向、隐藏假设、可靠性和边界条件
- **委派后台任务** — 用 `/codex:rescue` 把 bug 排查、修复尝试、延续上次任务交给 Codex，在后台慢慢跑

### 常用命令

| 命令                          | 用途                                                |
| --------------------------- | ------------------------------------------------- |
| `/codex:review`             | 对当前改动做普通只读 review，支持 `--base main`、`--background` |
| `/codex:adversarial-review` | 做带攻击性的 review，重点挑战设计、取舍和风险点                       |
| `/codex:rescue`             | 把任务委派给 Codex subagent，可用于排障、修复、续跑上次任务             |
| `/codex:status`             | 查看当前仓库里正在运行或最近完成的 Codex 任务                        |
| `/codex:result`             | 查看后台任务的最终结果，适合和 `--background` 搭配                 |

### 最小安装步骤

> [!info] 前置条件
> - ChatGPT 订阅（含 Free）或 OpenAI API key
> - Node.js 18.18+

在 Claude Code 中依次运行：

```bash
# 1. 添加 marketplace
/plugin marketplace add openai/codex-plugin-cc

# 2. 安装插件
/plugin install codex@openai-codex

# 3. 重载插件
/reload-plugins

# 4. 完成 setup
/codex:setup
```

如果本机还没安装 Codex CLI，也可以手动执行：

```bash
npm install -g @openai/codex
!codex login
```

### 一个顺手的实战流

先把 review 放到后台，再回来拿结果：

```bash
/codex:review --background
/codex:status
/codex:result
```

如果你想让它专门质疑某个方向，可以这样用：

```bash
/codex:adversarial-review --background look for race conditions and question the chosen approach
```

如果是排障或修复任务，直接委派：

```bash
/codex:rescue --background investigate why the tests started failing
```

对于主要在 Claude Code 中开发的人来说，这个插件的价值不是“替代 Claude”，而是把 Codex 作为第二审阅者和后台执行器接进现有工作流里。

**项目链接：** [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)

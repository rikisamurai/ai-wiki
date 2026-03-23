---
tags:
  - obsidian
  - claude
source: https://github.com/YishenTu/claudian
created: 2026-03-12
---

# Claudian — 在 Obsidian 中嵌入 Claude Code

Claudian 是一个 Obsidian 插件，将 **Claude Code** 作为 AI 协作者直接嵌入你的笔记库。它把整个 vault 变成 Claude 的工作目录，拥有完整的 agentic 能力：文件读写、搜索、Bash 执行、多步骤工作流，一切都在 Obsidian 内完成。

> [!tip] 一句话总结
> Claudian = Obsidian + Claude Code agent，让 AI 在你的第二大脑里"住下来"。

---

## 核心功能一览

| 功能 | 说明 |
|------|------|
| **全 Agent 能力** | 读写编辑文件、搜索、执行 Bash 命令 |
| **上下文感知** | 自动附加当前笔记；`@` 引用文件；按 tag 排除敏感笔记；支持编辑器选区 |
| **视觉支持** | 拖拽 / 粘贴 / 路径引入图片，Claude 可分析图像内容 |
| **Inline Edit** | 选中文本 + 快捷键，原地编辑并预览 word-level diff |
| **指令模式 (`#`)** | 在聊天输入框用 `#` 添加自定义指令到 system prompt |
| **Slash Commands** | `/command` 触发可复用的 prompt 模板，支持参数占位符和 `@file` 引用 |
| **Skills** | 可复用能力模块，根据上下文自动调用，兼容 Claude Code skill 格式 |
| **自定义 Agents** | 定义子 agent，可限制工具和覆盖模型 |
| **MCP 支持** | 通过 Model Context Protocol 连接外部工具（stdio / SSE / HTTP） |
| **模型控制** | Haiku / Sonnet / Opus 切换；自定义模型（环境变量）；thinking budget 微调 |
| **Plan Mode** | `Shift+Tab` 切换，先探索设计再实施 |
| **安全机制** | YOLO / Safe / Plan 三级权限；命令黑名单；vault 路径限制 |

---

## 安装方法

### 方式一：GitHub Release（推荐）

1. 前往 [Releases 页面](https://github.com/YishenTu/claudian/releases) 下载 `main.js`、`manifest.json`、`styles.css`
2. 在 vault 中创建文件夹：`.obsidian/plugins/claudian/`
3. 将下载的文件放入该文件夹
4. Obsidian → **Settings → Community plugins** → 启用 **Claudian**

### 方式二：BRAT（自动更新）

1. 安装 [BRAT](https://github.com/TfTHacker/obsidian42-brat) 插件
2. BRAT Settings → **Add Beta plugin** → 输入 `https://github.com/YishenTu/claudian`
3. 启用 Claudian

### 方式三：从源码构建

```bash
cd /path/to/vault/.obsidian/plugins
git clone https://github.com/YishenTu/claudian.git
cd claudian
npm install
npm run build
```

> [!info] 前置要求
> - **Claude Code CLI** 已安装（推荐原生安装）
> - **Obsidian v1.8.9+**
> - Claude 订阅 / API key（也支持 Openrouter、Kimi、GLM、DeepSeek 等兼容 Anthropic API 的提供商）
> - 仅桌面端（macOS / Linux / Windows）

---

## 使用指南

### 打开聊天

- 点击左侧 ribbon 栏的机器人图标
- 或使用命令面板（Command Palette）

### 上下文管理

| 操作 | 方法 |
|------|------|
| 自动附加当前笔记 | 打开笔记后直接聊天，Claude 自动读取 |
| `@` 引用文件 | 输入 `@` 触发下拉菜单，选择 vault 内文件 |
| `@Agents/` | 选择自定义 agent |
| `@mcp-server` | 激活带 context-saving 的 MCP 服务器 |
| `@folder/` | 过滤外部目录文件 |
| 编辑器选区 | 选中文本后发送消息，选区自动包含在上下文中 |
| 图片 | 拖拽、粘贴或输入路径 |
| 外部目录 | 点击工具栏文件夹图标添加 vault 外目录 |

### Inline Edit（原地编辑）

不用开聊天面板，直接在编辑器里选中文本让 Claude 就地修改。

1. ✏️ 在编辑器中选中一段文本（不选中则在光标处插入）
2. ⌨️ 按 Inline Edit 快捷键（Settings → Hotkeys 中绑定）
3. 💬 输入修改指令（如"翻译成英文"、"语气更正式"、"修复 bug"）
4. 👀 预览 word-level diff → ✅ 确认应用 / ❌ 取消撤回

> [!note] 与聊天模式的区别
> Inline Edit 下 Claude 只有**只读**权限（可读取其他文件获取上下文，但不能修改选区以外的内容），适合快速、局部的一次性编辑。



### Slash Commands（斜杠命令）

在聊天框输入 `/` 触发自定义 prompt 模板：

- 支持参数占位符
- 支持 `@file` 引用
- 支持内联 Bash 替换
- 可在 Settings 中创建、编辑、导入、导出

### Skills（技能模块）

将 `skill.md` 放到以下路径即可自动发现：

- 全局：`~/.claude/skills/`
- Vault 级：`{vault}/.claude/skills/`

Skills 会根据上下文自动触发，兼容 Claude Code 原生格式。

### Custom Agents（自定义 Agent）

将 `agent.md` 放到：

- 全局：`~/.claude/agents/`
- Vault 级：`{vault}/.claude/agents/`

通过 `@Agents/` 在聊天中选择，或让 Claude 自行调用。可限制工具集和覆盖模型。

### Plan Mode（规划模式）

按 `Shift+Tab` 切换。在此模式下 Claude 先探索和设计方案，呈交计划供你审批后再执行。适合复杂多步骤任务。

---

## 配置详解

### Settings 面板关键项

| 分类 | 设置项 | 说明 |
|------|--------|------|
| **用户** | User name | 个性化称呼 |
| **用户** | Excluded tags | 防止带特定 tag 的笔记被自动加载（如 `sensitive`） |
| **用户** | Media folder | 图片附件存储路径 |
| **用户** | Custom system prompt | 额外系统指令（`#` 模式保存于此） |
| **模型** | Model selection | Haiku / Sonnet / Opus |
| **模型** | Thinking budget | 微调推理深度 |
| **安全** | Permission mode | YOLO（无确认）/ Safe（逐次确认）/ Plan（先规划） |
| **安全** | Command blocklist | 正则匹配阻止危险命令 |
| **安全** | Allowed export paths | vault 外可写路径，默认 `~/Desktop`、`~/Downloads` |
| **环境** | Custom variables | 环境变量（`KEY=VALUE`），支持 `export` 前缀 |
| **环境** | Environment snippets | 保存/恢复变量配置方案 |
| **高级** | Claude CLI path | 自定义 CLI 路径（自动检测失败时手动设置） |

### 使用第三方模型

通过环境变量配置兼容 Anthropic API 的提供商：

```
ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1
ANTHROPIC_API_KEY=sk-or-xxxx
```

支持的提供商：Openrouter、Kimi、GLM、DeepSeek 等。

---

## 最佳实践

### 工作流建议

1. **用 Plan Mode 处理复杂任务** — `Shift+Tab` 切换，让 Claude 先出方案再动手，避免走弯路
2. **善用 `@` 引用** — 不要手动粘贴笔记内容，直接 `@filename` 让 Claude 自动读取
3. **敏感笔记加 Excluded Tag** — 在 Settings 中设置排除标签（如 `#private`），防止日记、密码等被自动加载
4. **Slash Commands 模板化高频操作** — 把常用 prompt 做成 `/command`，减少重复输入
5. **Skills 积累领域能力** — 为常见场景编写 skill（如代码审查、笔记整理），Claude 会根据上下文自动调用
6. **Inline Edit 微调文本** — 小范围修改不必开聊天，选中 + 快捷键即可原地编辑

### 安全建议

- 默认 **YOLO mode** 无需确认，效率最高但需信任 Claude 的操作
- 重要 vault 建议使用 **Safe mode**，每次工具调用都需确认
- 启用 **Command blocklist** 阻止 `rm -rf`、`git push --force` 等危险命令
- **Allowed export paths** 控制 vault 外写入范围

### 常见问题排查

> [!warning] `spawn claude ENOENT` / CLI 找不到
> 使用 nvm / fnm / volta 等 Node 版本管理器时常见。
>
> **解决**：运行 `which claude`（macOS/Linux）或 `where.exe claude`（Windows），将路径填入 **Settings → Advanced → Claude CLI path**。
>
> 示例路径：
> - macOS: `/Users/you/.volta/bin/claude`
> - Windows: `C:\Users\you\AppData\Local\Claude\claude.exe`

> [!warning] npm 安装的 CLI 与 Node.js 不在同一目录
> GUI 应用（如 Obsidian）可能找不到 Node.js。
>
> **解决**：推荐改用原生安装；或在 **Settings → Environment** 中添加 `PATH=/path/to/node/bin`。

---

## 数据与隐私

| 数据类型 | 存储位置 |
|----------|----------|
| 发送到 API 的内容 | 用户输入、附加文件、图片、工具输出（默认 Anthropic，可通过 `ANTHROPIC_BASE_URL` 自定义） |
| 本地设置 / 元数据 | `vault/.claude/` |
| 对话消息 | `~/.claude/projects/`（SDK 原生）；旧版在 `vault/.claude/sessions/` |
| 遥测 | **无**（除配置的 API 提供商外不发送任何数据） |

---

## 相关链接

- [Claudian GitHub](https://github.com/YishenTu/claudian)
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [BRAT 插件管理器](https://github.com/TfTHacker/obsidian42-brat)
- [Openrouter Claude Code 集成指南](https://openrouter.ai/docs/guides/guides/claude-code-integration)

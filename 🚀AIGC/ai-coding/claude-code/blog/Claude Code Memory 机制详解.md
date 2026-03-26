---
title: Claude Code Memory 机制详解
source: https://code.claude.com/docs/en/memory
tags:
  - claude-code
  - ai-coding
  - memory
date: 2026-03-13
---

# Claude Code Memory 机制详解

| 维度 | CLAUDE.md | `.claude/rules/` | Auto Memory |
| --- | --- | --- | --- |
| **谁写的** | 你 | 你 | Claude |
| **路径** | 项目根目录 `/CLAUDE.md` | `.claude/rules/*.md` | `~/.claude/projects/.../memory/` |
| **是否在 git 里** | ✅ 是 | ✅ 是 | ❌ 否 |
| **形式** | 单个文件 | 多个模块化规则文件 | 索引 + 主题文件 |
| **内容** | 项目指令与规则 | 细粒度/条件化规则 | 学习到的模式和偏好 |
| **作用域** | 项目/用户/组织 | 项目级，可按路径限定 | 每个工作目录（机器本地） |
| **加载方式** | 每次会话完整加载 | 匹配路径时按需加载 | 前 200 行 + 按需读取 |
| **共享** | 版本控制 | 版本控制 / 符号链接 | 不共享（本地） |
| **适合** | 通用编码标准、工作流 | 特定文件类型的规范 | 构建命令、调试心得 |


> [!abstract] 概览
> Claude Code 每次会话都从全新上下文开始。两种机制让知识跨会话持久化：
> - **CLAUDE.md 文件**：你手写的持久化指令
> - **Auto Memory**：Claude 根据你的纠正和偏好自动记录的笔记

## CLAUDE.md vs Auto Memory

| 维度 | CLAUDE.md | Auto Memory |
| --- | --- | --- |
| **谁写的** | 你 | Claude |
| **内容** | 指令和规则 | 学习到的模式和偏好 |
| **作用域** | 项目 / 用户 / 组织 | 每个工作目录 |
| **加载方式** | 每次会话完整加载 | 每次加载前 200 行 |
| **适合** | 编码标准、工作流、项目架构 | 构建命令、调试心得、偏好发现 |

## CLAUDE.md 文件

### 存放位置与作用域

| 作用域      | 路径                                                         | 用途                  | 共享范围     |
| -------- | ---------------------------------------------------------- | ------------------- | -------- |
| **托管策略** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md` | 组织级指令（IT/DevOps 管理） | 组织内所有用户  |
| **项目指令** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md`                      | 团队共享的项目指令           | 通过版本控制共享 |
| **用户指令** | `~/.claude/CLAUDE.md`                                      | 个人偏好（所有项目）          | 仅自己      |

> [!tip] 快速初始化
> 运行 `/init` 可自动生成项目 CLAUDE.md。Claude 会分析代码库并创建包含构建命令、测试指令和项目约定的文件。

### 编写有效指令的原则

- **大小**：每个 CLAUDE.md 文件控制在 ==200 行以内==，过长会消耗上下文并降低遵循度
- **结构**：使用 Markdown 标题和列表分组相关指令
- **具体性**：写可验证的具体指令，如 "Use 2-space indentation" 而非 "Format code properly"
- **一致性**：避免不同文件间的指令冲突，定期清理过时规则

### 导入外部文件

CLAUDE.md 支持 `@path/to/import` 语法导入其他文件：

```text
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

个人偏好可以指向 home 目录下的文件，不会被提交到版本控制：

```text
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

### 加载机制

- Claude Code 从当前工作目录==向上遍历==目录树，逐级加载 CLAUDE.md
- 子目录中的 CLAUDE.md 在 Claude 读取该目录文件时==按需加载==
- 使用 `--add-dir` 添加额外目录时，需设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` 来加载其 CLAUDE.md


举例：Claude Code 通过从当前工作目录向上遍历目录树来读取 CLAUDE.md 文件，检查沿途的每个目录。这意味着如果您在 `foo/bar/` 中运行 Claude Code，它会从 `foo/bar/CLAUDE.md` 和 `foo/CLAUDE.md` 加载指令。

如果在大型 monorepo 中工作，其中其他团队的 CLAUDE.md 文件被拾取，请使用 [`claudeMdExcludes`](https://code.claude.com/docs/zh-CN/memory#exclude-specific-claudemd-files) 跳过它们。


## .claude/rules/ 规则系统

将指令拆分为模块化的规则文件，便于团队维护：

```text
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md    # 代码风格
    ├── testing.md       # 测试约定
    └── security.md      # 安全要求
```

### 路径限定规则

通过 YAML frontmatter 的 `paths` 字段，让规则仅在匹配文件时生效：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
```

常用 glob 模式：

| 模式 | 匹配 |
| --- | --- |
| `**/*.ts` | 任意目录下的 TypeScript 文件 |
| `src/**/*` | `src/` 下所有文件 |
| `src/components/*.tsx` | 指定目录下的 React 组件 |

### 跨项目共享规则

支持通过==符号链接==共享规则：

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

### 排除不相关的 CLAUDE.md

在大型 monorepo 中，通过 `claudeMdExcludes` 跳过不相关的文件：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

## Auto Memory

Auto Memory 让 Claude 自动积累跨会话知识：构建命令、调试心得、架构笔记、代码风格偏好等。

> [!info] 版本要求
> 需要 Claude Code v2.1.59 或更高版本。

### 开关控制

- 默认开启，通过 `/memory` 命令切换
- 或在项目设置中配置 `"autoMemoryEnabled": false`
- 环境变量：`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

### 存储结构

每个项目的 memory 目录位于 `~/.claude/projects/<project>/memory/`：

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 索引文件，每次会话加载前 200 行
├── debugging.md       # 调试模式笔记
├── api-conventions.md # API 设计决策
└── ...
```

> [!important] 关键特性
> - 同一 git 仓库的所有 worktree 和子目录==共享同一个== auto memory 目录
> - Auto memory 是==机器本地的==，不跨机器或云环境共享
> - `MEMORY.md` 仅加载前 200 行，详细内容由 Claude 按需读取 topic 文件

### 自定义存储路径

通过 `autoMemoryDirectory` 设置（仅接受 policy/local/user 级别，==不接受== project 级别以防安全风险）：

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

## /memory 命令

- 列出当前会话加载的所有 CLAUDE.md 和 rules 文件
- 切换 auto memory 开关
- 提供打开 auto memory 文件夹的链接
- 选择任意文件在编辑器中打开

> [!tip] 主动记忆
> 对 Claude 说 "always use pnpm, not npm" 或 "remember that API tests require local Redis"，Claude 会保存到 auto memory。如果想写入 CLAUDE.md，需明确说 "add this to CLAUDE.md"。

## 常见问题排查

### Claude 不遵循 CLAUDE.md

> [!warning] CLAUDE.md 是上下文，不是强制配置
> Claude 会读取并尝试遵循，但无法保证严格执行，尤其对模糊或冲突的指令。

排查步骤：
1. 运行 `/memory` 确认文件是否被加载
2. 检查 CLAUDE.md 是否在正确的加载路径上
3. 让指令更具体
4. 检查不同文件间是否有冲突指令
5. 使用 `InstructionsLoaded` hook 记录加载细节

### CLAUDE.md 太大

- 超过 200 行的文件消耗更多上下文，可能降低遵循度
- 使用 `@path` 导入拆分内容
- 使用 `.claude/rules/` 模块化管理

### /compact 后指令丢失

- CLAUDE.md ==完整保留== compact 操作
- 如果指令消失，说明它只在对话中提到过，未写入 CLAUDE.md
- 将重要指令持久化到 CLAUDE.md 中

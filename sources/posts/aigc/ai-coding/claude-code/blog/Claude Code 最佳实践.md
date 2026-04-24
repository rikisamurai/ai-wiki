---
title: Claude Code 最佳实践
tags:
  - ai-coding
  - claude-code
  - best-practices
  - workflow
date: 2026-03-16
source: https://code.claude.com/docs/en/best-practices
---
# Claude Code 最佳实践

> [!abstract] 概览\
> \
> Claude Code 是一个**代理式编码环境**——它不只是回答问题，而是能主动读取文件、执行命令、修改代码并自主解决问题。本文总结了 Anthropic 内部团队和社区工程师验证过的高效使用模式，核心围绕一个关键约束展开：==上下文窗口是最重要的资源==。

## 核心原则：管理上下文窗口

Claude 的上下文窗口承载了整个对话的所有内容——消息、读取的文件、命令输出。一次调试或代码探索就可能消耗数万 token。随着上下文填满，LLM 性能会下降，Claude 可能会"遗忘"早期指令或犯更多错误。

> [!warning] 关键约束\
> \
> 上下文窗口是最重要的资源。应持续追踪上下文使用量，并积极采取策略减少 token 消耗。

***

## 1. 让 Claude 验证自己的工作

==提供测试、截图或预期输出==，让 Claude 能自我检查，这是**最高杠杆**的做法。

没有明确的成功标准时，Claude 可能产出"看起来对但实际不工作"的代码，你只能靠自己逐一检查。

| 策略          | 改进前          | 改进后                                                                    |
| ----------- | ------------ | ---------------------------------------------------------------------- |
| **提供验证标准**  | "实现一个邮箱验证函数" | "写一个 validateEmail 函数，测试用例：`a@b.com` → true，`invalid` → false。实现后运行测试" |
| **视觉验证 UI** | "让仪表盘更好看"    | "[贴截图] 实现这个设计，截图对比差异并修复"                                               |
| **定位根因**    | "构建失败了"      | "构建报这个错误：[贴错误]。修复并验证构建成功，要解决根因而非压制错误"                                  |

> [!tip] 验证方式\
> \
> 可以是测试套件、Linter、Bash 命令、截图对比，甚至 Chrome 扩展实时检查 UI。投资于**可靠的验证机制**。

***

## 2. 先探索，再规划，再编码

让 Claude 直接写代码可能解决错误的问题。使用 **Plan Mode** 分离探索与执行。

推荐的四阶段工作流：

1. **探索**——让 Claude 阅读相关代码、理解现有模式
2. **规划**——让 Claude 输出方案，你审核后再执行
3. **实现**——按计划编码
4. **验证**——运行测试确认正确

> [!note] 何时跳过规划？\
> \
> 当任务范围清晰且改动很小时（修 typo、加日志行、重命名变量），可以直接让 Claude 执行。==如果你能一句话描述 diff，就跳过规划==。

***

## 3. 提供具体上下文

提示词越精确，需要纠正的次数越少。Claude 能推断意图，但无法读心。

| 策略         | 改进前                               | 改进后                                                         |
| ---------- | --------------------------------- | ----------------------------------------------------------- |
| **限定范围**   | "给 foo.py 加测试"                    | "给 foo.py 写测试，覆盖用户已登出的边界情况，不用 mock"                         |
| **指向来源**   | "ExecutionFactory 的 API 为什么这么奇怪？" | "查看 ExecutionFactory 的 git history，总结其 API 的演变"             |
| **参考已有模式** | "加一个日历组件"                         | "查看首页已有的 widget 实现方式，HotDogWidget.php 是好例子。按同样模式实现一个日历组件…"  |
| **描述症状**   | "修复登录 bug"                        | "用户反馈 session 超时后登录失败。检查 src/auth/ 的 token 刷新。写一个复现测试，然后修复" |

### 提供丰富内容

- `@` **引用文件**——Claude 会在回答前先读取文件
- **粘贴图片**——直接拖拽或粘贴截图到提示词
- **提供 URL**——文档和 API 参考链接，用 `/permissions` 允许常用域名
- **管道输入**——`cat error.log | claude` 直接发送文件内容
- **让 Claude 自取**——告诉它用 Bash 命令、MCP 工具或文件读取获取所需上下文

***

## 4. 配置你的环境

几步配置就能让 Claude Code 在所有会话中显著提效。

### CLAUDE.md

运行 `/init` 生成初始 CLAUDE.md，然后逐步完善。它是每次对话开始时 Claude 自动读取的文件，用于提供**持久上下文**。

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, not the whole test suite
```

| 应写入                 | 不应写入              |
| ------------------- | ----------------- |
| Claude 猜不到的 Bash 命令 | Claude 读代码就能推断的内容 |
| 与默认不同的代码风格规则        | 标准语言规范            |
| 测试指令和首选测试运行器        | 详细 API 文档（改用链接）   |
| 仓库规范（分支命名、PR 约定）    | 频繁变化的信息           |
| 项目特有的架构决策           | 冗长的教程或解释          |

> [!warning] 保持精简\
> \
> CLAUDE.md 过长会导致 Claude ==忽略你的实际指令==。对每一行都问："删掉它 Claude 会犯错吗？"如果不会，就删。定期修剪，像维护代码一样维护它。

**放置位置**：

- `~/.claude/CLAUDE.md` — 全局，适用于所有会话
- `./CLAUDE.md` — 项目根目录，提交到 git 与团队共享
- 父目录/子目录 — monorepo 场景自动拉取

### 权限配置

用 `/permissions` 允许安全命令（如 `npm run lint`、`git commit`），或用 `/sandbox` 启用 OS 级隔离。减少重复确认的打断。

### CLI 工具

告诉 Claude 使用 `gh`、`aws`、`gcloud`、`sentry-cli` 等 CLI 工具与外部服务交互——这是==最节省上下文==的方式。

### MCP 服务器

运行 `claude mcp add` 连接 Notion、Figma、数据库等外部工具，让 Claude 能直接从 issue tracker 实现功能、查询数据库、分析监控数据。

### Hooks

用于**必须每次都执行、零例外**的操作。与 CLAUDE.md 的"建议性"不同，Hooks 是确定性的保证。

```text
示例：
- 每次文件编辑后自动运行 eslint
- 阻止对 migrations 目录的写入
```

### Skills

在 `.claude/skills/` 中创建 `SKILL.md`，赋予 Claude 领域知识和可复用工作流。Claude 在相关时自动应用，也可通过 `/skill-name` 手动调用。

### 自定义 Subagents

在 `.claude/agents/` 中定义专门的助手，Claude 可以委派隔离任务给它们，各自拥有独立的上下文和工具权限。

### Plugins

运行 `/plugin` 浏览市场。插件将 Skills、Hooks、Subagents 和 MCP 打包为一键安装单元。

***

## 5. 有效沟通

### 像问高级工程师一样提问

在新代码库中上手时，直接问 Claude：

- "日志系统是怎么工作的？"
- "怎么新建一个 API 端点？"
- "foo.rs 第 134 行的 `async move { ... }` 是什么意思？"
- "这段代码为什么调 `foo()` 而不是 `bar()`？"

### 让 Claude 采访你

对于较大的功能，先让 Claude 采访你，再开始编码：

```text
我想构建 [简要描述]。用 AskUserQuestion 工具深入采访我。

问技术实现、UI/UX、边界情况、顾虑和权衡。不要问显而易见的问题，挖掘我可能没考虑到的难点。

采访完成后，将完整规格写入 SPEC.md。
```

> [!tip] 新会话执行\
> \
> 规格完成后，==开启新会话==执行。新会话拥有干净的上下文，完全专注于实现。

***

## 6. 管理会话

### 及时纠正

发现 Claude 偏离方向时立即纠正：

- `Esc`——中止当前操作，上下文保留，可重新指导
- `Esc + Esc` **或** `/rewind`——回退到之前的检查点
- **"撤销"**——让 Claude 回滚修改
- `/clear`——在不相关任务之间重置上下文

> [!important] 两次纠正规则\
> \
> 如果同一会话中对同一问题纠正超过两次，上下文已被失败方案污染。==运行 `/clear` 重新开始==，用更精确的提示词。

### 积极管理上下文

- 任务间频繁使用 `/clear` 重置
- 自动压缩触发时，Claude 会总结关键代码模式、文件状态和决策
- 手动控制：`/compact <指令>`，如 `/compact 聚焦 API 变更`
- 快速问题用 `/btw`——答案显示在浮层中，==不进入对话历史==

### 使用子代理调研

将调研委派给子代理，它们在独立上下文中探索，只返回摘要，==不污染主对话==：

```text
使用子代理调查我们的认证系统如何处理 token 刷新，
以及是否有现成的 OAuth 工具可以复用。
```

### 检查点回退

Claude 的每个操作都会创建检查点。双击 `Escape` 或运行 `/rewind` 可恢复对话、代码或两者。

> [!note] 注意\
> \
> 检查点只追踪 Claude 的变更，不追踪外部进程。这不能替代 git。

### 恢复对话

```bash
claude --continue    # 恢复最近的对话
claude --resume      # 从最近对话列表中选择
```

用 `/rename` 给会话起描述性名称，如 `"oauth-migration"`，方便后续查找。

***

## 7. 自动化与扩展

掌握了单个 Claude 的使用后，可以通过并行会话和非交互模式成倍提升产出。

### 非交互模式

```bash
claude -p "prompt"                          # 一次性查询
claude -p "列出所有 API 端点" --output-format json   # 结构化输出
claude -p "分析日志" --output-format stream-json      # 流式输出
```

适用于 CI 流水线、pre-commit hooks 和自动化脚本。

### 多会话并行

- **桌面应用**——可视化管理多个本地会话，各自隔离工作树
- **Web 版**——在 Anthropic 云基础设施的隔离 VM 中运行
- **Agent Teams**——多会话自动协调，共享任务和消息

**Writer/Reviewer 模式**：

| 会话 A（编写者）            | 会话 B（审查者）                           |
| -------------------- | ----------------------------------- |
| `实现 API 限流中间件`       |                                     |
|                      | `审查 rateLimiter.ts 的实现，检查边界情况、竞态条件` |
| `根据审查反馈修改：[会话 B 输出]` |                                     |

### 文件级分发

```bash
# 批量处理多个文件
for file in src/*.py; do
  claude -p "重构 $file" --allowedTools Edit,Read &
done
```

用 `--allowedTools` 限定批量操作的权限范围。

***

## 常见反模式

| 反模式               | 问题                     | 解决方案                     |
| ----------------- | ---------------------- | ------------------------ |
| **大杂烩会话**         | 一个会话混杂不相关任务，上下文充满无关信息  | 任务间用 `/clear` 清理         |
| **反复纠正**          | 多次纠正同一错误，上下文被失败方案污染    | 两次失败后 `/clear`，写更好的初始提示词 |
| **臃肿的 CLAUDE.md** | 文件过长，重要规则被淹没           | 无情修剪；Claude 已经做对的事就不需要写  |
| **信任-验证缺口**       | 产出看似合理但未处理边界情况         | 始终提供验证手段（测试、脚本、截图）       |
| **无限探索**          | 不限范围的"调查"导致读取大量文件填满上下文 | 限定调查范围，或使用子代理            |

***

## 培养直觉

这些模式不是铁律，而是有效的起点。随着实践积累，你会发展出指南无法涵盖的直觉：

- 何时保持具体、何时保持开放
- 何时规划、何时探索
- 何时清理上下文、何时让它积累

> [!quote] 关键心法\
> \
> 当 Claude 输出优秀时，注意你做了什么——提示词结构、提供的上下文、所处的模式。当 Claude 挣扎时，问为什么——上下文太嘈杂？提示词太模糊？任务太大？

***

## 相关链接

- [Claude Code 工作原理](https://code.claude.com/docs/en/how-claude-code-works) — 代理循环、工具和上下文管理
- [扩展 Claude Code](https://code.claude.com/docs/en/features-overview) — Skills、Hooks、MCP、Subagents 和 Plugins
- [常见工作流](https://code.claude.com/docs/en/common-workflows) — 调试、测试、PR 等步骤指南
- [CLAUDE.md 指南](https://code.claude.com/docs/en/memory) — 存储项目约定和持久上下文

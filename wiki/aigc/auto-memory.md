---
title: Auto Memory（自动记忆）
tags: [claude-code, memory, auto]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code Memory 机制详解]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-22
status: draft
---

Auto Memory 是 [[claude-code-memory|Claude Code Memory 体系]]里**唯一由 Claude 自己写**的那一层——根据你的纠正和偏好自动积累跨会话知识：构建命令、调试心得、架构笔记、代码风格偏好。需要 Claude Code v2.1.59+，默认开启，通过 `/memory` 切换或在设置里 `"autoMemoryEnabled": false` 关闭。

**关键特性**

- 存储路径：`~/.claude/projects/<project>/memory/`——**机器本地，不跨机器或云环境共享**
- 同一 git 仓库的所有 [[wiki/aigc/superpowers|worktree]] 和子目录**共享同一个** auto memory 目录
- `MEMORY.md` 是索引文件，**每次会话加载前 200 行**；详细内容由 Claude 按需读取 topic 文件

> [!example] 典型存储结构
> ```
> ~/.claude/projects/<project>/memory/
> ├── MEMORY.md          # 索引（前 200 行加载）
> ├── debugging.md       # 调试模式笔记
> ├── api-conventions.md # API 设计决策
> └── ...
> ```

> [!tip] 主动记忆 vs 持久化指令
> 对 Claude 说 "always use pnpm, not npm" 或 "remember that API tests require local Redis"——Claude 会保存到 auto memory。如果想写入 [[claude-code-memory|CLAUDE.md]]（团队共享、走版本控制），**必须明确说**"add this to CLAUDE.md"。

**与 CLAUDE.md 的分工**

| | CLAUDE.md | Auto Memory |
|---|---|---|
| **来源** | 你显式写 | Claude 隐式记 |
| **是否共享** | git 共享给团队 | 机器本地，不共享 |
| **适合内容** | 不变的工程约定 | 个人化的快捷信号、调试心得 |
| **风险** | 改一行影响所有人 | 只影响自己 |

**自定义存储路径**：通过 `autoMemoryDirectory` 设置（仅接受 policy/local/user 级别，**不接受 project 级别**——避免一个克隆下来的恶意项目改你的全局 memory 路径）。

> [!warning] Auto Memory 不是版本控制的备忘录
> 因为它是机器本地的，换机器、换 worktree 容器、换云环境就丢。**真正重要的约定要 promote 到 CLAUDE.md 或 [[claude-rules|.claude/rules/]]**——这与 [[harness-engineering|Harness Engineering]] 的"promote the rule into code"是同一思路：把"暂时记住的"提升为"永久执行的"。

> [!important] 检索机制：用 AI 选记忆，精确度优先
> Auto Memory 不是关键词搜索——Claude Code 用**另一个 Sonnet 模型**扫描所有记忆文件的标题和描述，选出**最多 5 条**最相关的全文注入当前对话。策略明确：**精确度优先于召回率**——宁可漏一个可能有用的记忆，也不塞一个不相关的污染上下文。这意味着记忆文件的 frontmatter `description` 字段质量直接决定召回——和 [[wiki/aigc/skill-编写实践|Skill 描述符]] 是 if-then 条件是同一回事。

> [!example] KAIROS 模式：写入和提炼分离
> 在 KAIROS 实验模式下，长会话的记忆**实时**追加到按日期的原始日志，再由 `/dream` 技能在低活跃期**异步蒸馏**成结构化主题文件。详见 [[kairos-记忆蒸馏]]——这套设计把昂贵的归类工作从用户路径移到了离线 ETL。

> [!important] 源码层：用另一个 AI 选记忆
> 检索阶段不是关键词匹配，而是让 **Sonnet** 扫描所有记忆文件的标题和描述，**最多选 5 条**最相关的全文注入对话。策略是**精确度优先于召回率**——宁可漏一条可能有用的，也不塞一条不相关的污染上下文。这条选择反过来要求**记忆文件的 description 必须写得像 if-then 条件**（参考 [[skill-编写实践|Skill 描述符写法]]），否则 Sonnet 选不准。
>
> 进阶玩法：**KAIROS 模式**用追加日志 + 离线 [[kairos-记忆蒸馏|/dream 蒸馏]]生成结构化主题文件，让 Sonnet 检索质量更高。

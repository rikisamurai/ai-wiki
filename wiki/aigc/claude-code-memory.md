---
title: Claude Code Memory 体系
tags: [claude-code, memory, context-engineering]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code Memory 机制详解]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-22
status: draft
---

Claude Code 每次会话从全新上下文开始，Memory 体系是让知识跨会话持久化的三层结构：**CLAUDE.md（你写）+ `.claude/rules/`（你写、模块化）+ Auto Memory（Claude 自写）**。三者互补，各有作用域和加载机制。

> [!compare] 三种 Memory 对比
> | 维度 | CLAUDE.md | [[claude-rules\|.claude/rules/]] | [[auto-memory\|Auto Memory]] |
> |---|---|---|---|
> | **谁写的** | 你 | 你 | Claude |
> | **路径** | 项目根 / 用户家目录 | `.claude/rules/*.md` | `~/.claude/projects/.../memory/` |
> | **是否在 git 里** | ✅ | ✅ | ❌ |
> | **加载方式** | 每次会话完整加载 | 匹配路径时按需加载 | 前 200 行 + 按需读取 |
> | **共享** | 版本控制 | 版本控制 / 符号链接 | 不共享（机器本地） |
> | **适合** | 通用编码标准、工作流 | 特定文件类型规范 | 构建命令、调试心得 |

## CLAUDE.md 的作用域层级

| 作用域 | 路径 | 用途 |
|---|---|---|
| **托管策略** | `/Library/Application Support/ClaudeCode/CLAUDE.md` | 组织级（IT/DevOps 管理） |
| **项目** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享，走版本控制 |
| **用户** | `~/.claude/CLAUDE.md` | 个人偏好，所有项目 |

加载机制：从当前工作目录**向上遍历**目录树，逐级加载；子目录的 CLAUDE.md 在 Claude 读到该目录文件时**按需加载**。在大型 monorepo 里用 `claudeMdExcludes` 跳过不相关团队的 CLAUDE.md。

> [!tip] 200 行经验法则
> 每个 CLAUDE.md 控制在 200 行以内——过长会消耗上下文并降低遵循度。超长就用 `@path/to/import` 拆分，或迁到 [[claude-rules|.claude/rules/]]。这与 [[渐进式披露]] 是同一原则在 CLAUDE.md 这一层的应用。

## 与跨工具概念的关系

CLAUDE.md 是 [[agents-md|AGENTS.md]]（跨 Agent 的项目级备忘录）在 Claude Code 这个具体工具里的实现。相同原则：**信息密度 > 内容多寡**，**目录而非百科全书**。OpenAI Codex 团队的"~100 行 AGENTS.md + 完整 docs/" 结构同样适用。

> [!warning] CLAUDE.md 是上下文，不是强制配置
> Claude 会读取并尝试遵循，但**无法保证严格执行**，尤其对模糊或冲突的指令。如果发现不遵循：① 用 `/memory` 确认是否被加载 ② 让指令更具体 ③ 检查文件冲突 ④ 用 `InstructionsLoaded` hook 记录加载细节。/compact 后保留 CLAUDE.md，但只在对话里提过、没写进文件的指令会丢。

> [!example] NEVER / ALWAYS 模板
> Tw93 的 CLAUDE.md 模板里把"安全栏杆"显式列出来——比写散文式的注意事项更稳定触发：
> ```markdown
> ## NEVER
> - Modify `.env`, lockfiles, or CI secrets without explicit approval
> - Remove feature flags without searching all call sites
> - Commit without running tests
>
> ## ALWAYS
> - Show diff before committing
> - Update CHANGELOG for user-facing changes
> ```
> 真正"必须不能违反"的事项考虑升级到 [[hooks|Hooks]]——CLAUDE.md 是声明，Hook 是执行。

> [!tip] 让 Claude 维护自己的 CLAUDE.md
> 每次纠正错误后说一句："Update your CLAUDE.md so you don't make that mistake again."。或者输入 `#` 把当前对话内容直接追加进 CLAUDE.md。一开始可以什么都不写，**用着用着自然知道该补什么**——这与 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 的"反应式生长"是同构的。

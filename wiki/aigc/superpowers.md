---
title: Superpowers（AI 编码工作流框架）
tags: [claude-code, workflow, framework, plugin]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Superpowers - AI 编码工作流框架]]"
last-ingested: 2026-04-23
status: stable
---

Superpowers 是 Jesse Vincent（@obra）做的开源 [[wiki/ai-coding/agentic-coding|agentic coding]] 工作流框架——把"agent 该如何做软件开发"沉淀成一套可组合的 [[agent-skills|Skills]]。它不是一个工具，是一套**纪律**：动手前必须先 brainstorm、规划必须细到每个任务 2-5 分钟、执行用 subagent 串起来。让 Claude 能自主跑数小时不偏离计划。

> [!important] 它解决的核心问题
> "vibe coding 跑 10 分钟方向就跑偏" 的根因是**没有结构**——Agent 想到哪写到哪。Superpowers 用 Skills 强制注入 4 个不变量：**brainstorm → plan → subagent execute → verify**。每一步都不能跳。这是 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 的具体落地，也是 [[wiki/ai-coding/spec-coding|Spec Coding]] 的工作流版本。

> [!compare] 4 条核心原则
> | 原则 | 翻译 | 对应 wiki 页面 |
> |---|---|---|
> | **Test-driven development** | 永远先写测试 | [[subagent-driven-development\|TDD 是基础]] |
> | **Systematic > ad-hoc** | 用流程代替猜测 | [[wiki/ai-coding/探索-规划-编码-验证\|四阶段工作流]] |
> | **降低复杂度** | 简洁优先 | [[wiki/ai-coding/yagni-与-dry-反论\|YAGNI + DRY]] |
> | **证据 > 断言** | 声称完成前必须验证 | [[wiki/ai-coding/验证驱动\|验证驱动]] |
>
> 这 4 条原则不是 Superpowers 发明的——它们散落在 Claude Code 最佳实践里。Superpowers 的贡献是**用 Skills 把它们强制工程化**，而不是靠 Claude 记住或人工督促。

**6 阶段工作流**

```
启动 Agent
  ↓
[brainstorming] 苏格拉底式挖需求
  ↓
[using-git-worktrees] 创建隔离工作区
  ↓
[writing-plans] 生成 2-5 分钟粒度的实施计划
  ↓
[subagent-driven-development] 每个任务派独立 subagent 执行
  ↓
[test-driven-development] 每任务强制 TDD（RED → GREEN → REFACTOR）
  ↓
[requesting-code-review] 任务间审查
  ↓
[finishing-a-development-branch] 合并 / PR / 清理
```

每一步都是一个独立的 [[agent-skills|Skill]]——可以单独调用、组合使用、或在自己的工作流里只挑几个。

> [!tip] 最值得抄的 3 个 Skill
> 不必整套照搬，先借鉴这 3 个最具普适性的：
> 1. **`brainstorming`** — 苏格拉底式提问把模糊需求变具体（与 [[wiki/ai-coding/采访驱动-spec|采访驱动 SPEC]]同思路，但流程更严格）
> 2. **`subagent-driven-development`** — 每个任务一个 subagent，主线程只做 review（[[wiki/ai-coding/subagent-上下文隔离|预防式上下文管理]]的极致）
> 3. **`verification-before-completion`** — 不允许 Claude 自称"完成"，必须证据（直接对应 [[wiki/ai-coding/验证驱动|验证驱动]]）

**安装**：跨平台插件市场都有

```bash
# Claude Code 官方
/plugin install superpowers@claude-plugins-official

# Cursor
/add-plugin superpowers

# Gemini CLI
gemini extensions install https://github.com/obra/superpowers
```

> [!example] 怎么验证装上了
> 新开会话说"帮我规划一个 X"或"我们来 debug 这个问题"——Agent 应该自动触发 `brainstorming` 或 `systematic-debugging` skill。如果它直接开写代码，要么没装好、要么 Skill 选取层（[[wiki/aigc/auto-memory|Sonnet top-5]]）没选中。

> [!warning] Skills 多 ≠ 效果好
> Superpowers 的 Skills 总共十几个，每个文件几百到几千 token——全装会推高 context 占用 + 拉低 [[wiki/ai-coding/cache-命中率|cache 命中率]]。建议姿势：**只装真正会触发的几个**，或参考 [[everything-claude-code|Everything Claude Code]] 那种"借鉴 prompt 写法 + 选装"的策略。

**关联**：[[everything-claude-code|Everything Claude Code]]（另一个完整 Harness） / [[wiki/aigc/coordinator-模式|Coordinator 模式]]（subagent 编排的理论） / [[agent-skills|Skills 规范]] / [[wiki/ai-coding/harness-engineering|Harness Engineering]]

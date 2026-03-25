---
title: Codex Best Practices
tags:
  - ai-coding
  - codex
  - openai
date: 2026-03-16
source: https://developers.openai.com/codex/learn/best-practices
---

# Codex Best Practices

> [!abstract] 概述
> OpenAI Codex 最佳实践指南，涵盖 Prompt 编写、任务规划、AGENTS.md 配置、MCP 集成、Skills 复用及自动化等核心主题。核心理念：**把 Codex 当作一个可以持续配置和改进的团队成员，而非一次性助手。**

![[Gemini_Generated_Image_mhc1akmhc1akmhc1.png]]




## 1. 提供清晰的 Context 和 Prompt

一个好的 Prompt 应包含四个要素：
![[Pasted image 20260325141342.png]]

| 要素 | 说明 |
|------|------|
| **Goal** | 你要改变或构建什么？ |
| **Context** | 哪些文件、文件夹、文档、示例或报错与任务相关？可以用 `@` 提及文件 |
| **Constraints** | 需要遵循哪些标准、架构、安全要求或约定？ |
| **Done when** | 任务完成的标志是什么？（测试通过、行为变化、Bug 不再复现等） |

> [!tip] Reasoning Level 选择
> - **Low**：快速、范围明确的任务
> - **Medium / High**：复杂变更或调试
> - **Extra High**：长链式、需要深度推理的 Agent 任务

## 2. 复杂任务先做规划

三种有效的规划方式：

1. **Plan Mode**：用 `/plan` 或 `Shift + Tab` 切换，让 Codex 先收集 Context、提出澄清问题，再执行
2. **让 Codex 采访你**：告诉它先质疑你的假设，把模糊想法变成具体方案
3. **PLANS.md 模板**：为长任务配置执行计划模板（参考 [Execution Plans Guide](https://developers.openai.com/cookbook/articles/codex_exec_plans)）

## 3. 用 AGENTS.md 让指导规则可复用

> [!info] AGENTS.md 是什么？
> 一个面向 Agent 的开放格式 README，自动加载到 Context 中，是编码团队规范和工作方式的最佳载体。

一个好的 `AGENTS.md` 应包含：

- 仓库结构和重要目录说明
- 项目运行方式
- 构建、测试和 Lint 命令
- 工程规范和 PR 期望
- 约束和「不要做」规则
- 「完成」的定义及验证方式

**层级结构：**
![[Gemini_Generated_Image_ql1yzbql1yzbql1y.png]]
- `~/.codex/AGENTS.md` → 个人全局默认
- 仓库根目录 `AGENTS.md` → 团队共享标准
- 子目录 `AGENTS.md` → 局部规则（**就近原则，更具体的优先**）

> [!warning] 实践建议
> - 保持简短精确，比长篇泛泛的规则更有用
> - 当 Codex 犯同样的错误两次时，让它做 Retrospective 并更新 `AGENTS.md`
> - 如果文件过大，保持主文件精简，引用独立的 Markdown 文件（如 `code_review.md`、`architecture.md`）



## 4. 配置 Codex 保持一致性

**配置层级：**

| 位置 | 用途 |
|------|------|
| `~/.codex/config.toml` | 个人默认偏好 |
| `.codex/config.toml` | 仓库级行为 |
| 命令行参数 | 一次性覆盖 |

**两个关键控制维度：**

- **Approval Mode**：决定 Codex 何时需要你的许可才能执行命令
- **Sandbox Mode**：决定 Codex 可以读写的目录和文件范围

> [!tip] 新手建议
> 先用默认权限，只在明确需要时才放宽。很多质量问题本质上是配置问题（错误的工作目录、缺少写权限、模型默认值不对等）。

## 5. 通过测试和 Review 提升可靠性

不要止步于让 Codex 做变更，还应让它：

- 为变更编写或更新测试
- 运行相关的测试套件
- 检查 Lint、格式化、类型检查
- 确认最终行为符合需求
- Review Diff 以排查 Bug、回归或风险模式

> [!example] 实用功能
> - **Diff 面板**：直接在 Codex App 中 Review 变更
> - **`/review` 命令**：支持基于 Base Branch 的 PR Review、未提交变更 Review、Commit Review、自定义 Review 指令
> - **GitHub 集成**：可配置 Codex 自动 Review 所有 PR（OpenAI 内部 100% PR 由 Codex Review）

## 6. 用 MCP 获取外部 Context

> [!info] MCP (Model Context Protocol)
> 一个开放标准，用于将 Codex 连接到外部工具和系统。支持 STDIO 和 Streamable HTTP（含 OAuth）。

**适用场景：**

- 需要的 Context 在仓库外
- 数据变化频繁
- 需要 Codex 使用工具而非依赖粘贴的指令
- 需要跨用户或项目的可重复集成

> [!warning] 注意
> 从 1–2 个能消除手动循环的工具开始，不要一开始就接入所有工具。

## 7. 将重复工作变成 Skills

当工作流变得可重复时，用 Skill 将指令、Context 和逻辑打包。
![[Gemini_Generated_Image_ipuer8ipuer8ipue.png]]
**Skill 设计原则：**

- 每个 Skill 专注一个任务
- 从 2–3 个具体用例开始
- 定义清晰的输入和输出
- 描述说明 Skill 做什么以及何时使用

**典型 Skill 场景：** 日志分析、Release Note 起草、PR Checklist Review、迁移规划、Telemetry 摘要、标准调试流程

**存放位置：**

- 个人：`$HOME/.agents/skills`
- 团队共享：仓库内 `.agents/skills`

## 8. 用 Automations 自动化稳定工作流

> [!important] 关键原则
> **Skills 定义方法，Automations 定义调度。** 如果工作流还需要大量人工引导，先变成 Skill；一旦可预测，再自动化。

**适合自动化的场景：**

- 总结近期 Commits
- 扫描潜在 Bug
- 起草 Release Notes
- 检查 CI 失败
- 生成 Standup 摘要
- 按计划运行分析工作流

## 9. 用 Session Controls 管理长任务

**实用命令：**

| 命令 | 用途 |
|------|------|
| `/resume` | 恢复已保存的对话 |
| `/fork` | 创建新线程，保留原始记录 |
| `/compact` | 压缩长对话的早期 Context |
| `/agent` | 在并行 Agent 间切换 |
| `/plan` | 切换 Plan Mode |
| `/review` | 代码审查 |
| `/status` | 查看当前 Session 状态 |

> [!tip] 线程管理
> - 每个独立工作单元使用一个线程
> - 仅在工作真正分叉时才 Fork
> - 用 Subagent 分担有界任务（探索、测试、分类等），保持主 Agent 聚焦核心问题

## 10. 常见错误

> [!danger] 避免以下错误
> - 在 Prompt 中堆砌持久规则，而不是放到 `AGENTS.md` 或 Skill 中
> - 没有告诉 Codex 如何运行构建和测试命令
> - 对多步骤复杂任务跳过规划
> - 在理解工作流之前就给 Codex 完全权限
> - 在同一文件上运行多个活跃线程，而不使用 Git Worktree
> - 在工作流不够稳定时就转为自动化
> - 逐步监视 Codex 而不是并行工作
> - 每个项目只用一个线程（而非每个任务一个线程），导致 Context 膨胀、结果变差

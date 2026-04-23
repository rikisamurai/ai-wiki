---
title: Hooks（钩子）
tags: [claude-code, hooks, deterministic]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 最佳实践]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
last-ingested: 2026-04-22
status: draft
---

Hooks 是 Claude Code 的**确定性扩展点**：在 PreToolUse / PostToolUse / SessionStart 等事件触发时执行你定义的脚本。它和 [[claude-code-memory|CLAUDE.md]] 的根本差别——**Hooks 是"必须每次都执行、零例外"，CLAUDE.md 是"建议性的提醒"**。

> [!compare] 确定性 vs 建议性
> | 维度 | Hooks | CLAUDE.md |
> |---|---|---|
> | **执行保证** | 100%，由代码触发 | 模型自由解释，可能忽略 |
> | **失败处理** | 可阻断工具调用 | 只能事后发现没遵守 |
> | **上下文成本** | 0（不进上下文） | 每次会话占用 token |
> | **适合内容** | lint / 格式化 / 路径白名单 | 代码风格说明 / 工作流偏好 |

**典型用例**

- 每次文件编辑后**自动**运行 ESLint / Prettier
- **阻止**对 `migrations/` 目录的写入（误操作防御）
- SessionStart 时拉取最新依赖版本到上下文
- PreToolUse 拦截高危 Bash（`rm -rf` / `git push --force`）

> [!important] 选择 Hooks 还是 CLAUDE.md：先问"能否容忍 Claude 偶尔不照做"
> 如果答案是"不能"——选 Hooks。例如"提交前必须跑 lint"——写 CLAUDE.md 里 Claude 大概率会做，但偶尔会跳，写成 PostToolUse hook 就 100% 保证。**两者不是替代关系，是分工**：[[claude-code-memory|CLAUDE.md]] 写"为什么"和"怎么写"，Hooks 写"必须发生"。

**与 [[harness-engineering|Harness Engineering]] 的关系**：Hooks 是 [[enforce-invariants|Enforce Invariants]] 原则在 Claude Code 这一层的载体——把不变量从"写在文档里希望 Claude 遵守"提升为"写进代码强制执行"。这与 git pre-commit hook、CI lint 是同一思路的不同层级。

> [!tip] Hooks 不要承担太多
> Hooks 跑在每次工具调用后，慢的 hook 会拖累整个会话节奏。把 lint 限定到改动文件而非全仓、把测试推到 commit 阶段而非 edit 阶段。重活留给 [[wiki/ai-coding/subagent-上下文隔离|subagent]]。

> [!important] CLAUDE.md / Skill / Hook 三层叠加
> 同一条规则三处布防，少任何一层都有漏洞：
> - **[[claude-code-memory|CLAUDE.md]]**：声明规则（"提交前必须通过测试"）——告诉 Claude 这条规则存在
> - **[[agent-skills|Skill]]**：告诉 Claude 操作顺序和修复方法（怎么跑测试、报错怎么读）
> - **Hook**：关键路径硬性校验，必要时阻断（commit 前自动跑测试，挂了不让 commit）
>
> 只写 CLAUDE.md 规则，Claude 经常当没看见——因为它有"别的优先事项要赶"。Hook 把"建议性"升级为"确定性"。这是 [[wiki/ai-coding/enforce-invariants|Enforce Invariants]] 在 Claude Code 这一层的具体落地。

---
title: Skills vs Automations（方法 vs 调度）
tags: [codex, skills, automation, workflow]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/codex/Codex Best Practices]]"
last-ingested: 2026-04-23
status: stable
---

Codex Best Practices 用一句话切清了 [[agent-skills|Skills]] 和自动化的边界：**Skills 定义方法（how to do it），Automations 定义调度（when to do it）**。这条原则同样适用于 Claude Code 的 Skills + [[hooks|Hooks]]——hooks 就是 Claude 的 automations。

> [!important] 升级路径：手动 → Skill → Automation
> 一个工作流从混沌走向稳定的成熟度阶梯：
>
> 1. **混沌期**：每次都靠人工 prompt，每次结果略有不同——不要急着做 Skill
> 2. **方法期**：动作稳定但仍需人来触发——把动作打包成 Skill
> 3. **调度期**：连触发时机都可预测——再升级为 Automation
>
> 颠倒顺序的代价：在第 2 阶段直接做自动化 → 自动跑出垃圾结果你都不知道；在第 1 阶段做 Skill → 频繁改、难维护。

> [!compare] 决策树
> | 工作流的状态 | 选择 |
> |---|---|
> | "我每次都得详细解释" | 写 Skill |
> | "Skill 已稳定，每次仍要我手动 invoke" | 升级 Automation |
> | "结果还不可预测" | **不要**自动化，先打磨 Skill 或人工做 |
> | "只做一次" | 都不需要——直接 prompt |

**Codex 的 Automation 典型场景**

- 总结近期 commits
- 扫描潜在 bug
- 起草 release notes
- 检查 CI 失败
- 生成 standup 摘要
- 按计划运行分析工作流

> [!example] Claude Code 里的等价物
> Claude Code 没有正式的 "Automations" 命名，但 **[[hooks|Hooks]] 就是 automations**——`PreToolUse` / `PostToolUse` / `Stop` 等事件触发的 shell 命令。同时 [[wiki/claude-code/claude-code|Claude Code]] 还能配合外部调度（cron / GitHub Actions）做时间驱动的 automation：
>
> ```bash
> # 每天早上自动跑安全扫描
> 0 9 * * * cd /repo && claude -p "/security-scan" --allowedTools Read,Bash
> ```
>
> 关键是不要把这种"已经稳定的动作"留在交互式会话里——会浪费上下文。

> [!warning] 反模式：早自动化
> Codex 列出的常见错误之一：**"工作流不够稳定就转为自动化"**。表面上是"我自动化了，效率高了"，实际上是把"输出质量随机"的工作流批量化生产噪声——从手动出错变成自动出错，错的次数还更多。
>
> 检验标准：**Skill 至少在 5 次不同输入下产出符合预期的结果**，再考虑自动化。

> [!tip] Skill 的 3 步设计
> 来自 Codex Best Practices 的 Skill 设计原则（与 [[skill-编写实践|Skill 编写实践]]互为印证）：
>
> 1. **每个 Skill 专注一个任务**——不要做"万能助手 Skill"
> 2. **从 2-3 个具体用例开始**——抽象之前先有具象
> 3. **定义清晰的输入和输出**——和 Unix pipe 哲学一致
> 4. **描述说明 Skill 做什么 + 何时使用**——这条决定 [[wiki/claude-code/auto-memory|检索时能不能选中]]

**关联**：[[agent-skills|Agent Skills 规范]] / [[skill-编写实践|Skill 编写实践]] / [[hooks|Hooks]]（Claude Code 的 automation 实现） / [[wiki/claude-code/codex|Codex]]

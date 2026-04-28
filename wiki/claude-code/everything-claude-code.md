---
title: Everything Claude Code
tags: [claude-code, harness, plugin]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/🛠️claude-code-tools]]"
last-ingested: 2026-04-23
status: draft
---

Everything Claude Code（简称 ECC）是 Anthropic Hackathon 获奖者发布的"完整 [[wiki/agent-engineering/philosophy/harness-engineering|Harness]]"——不是一堆配置的拼盘，而是把 [[claude-code-六层架构|六层架构]]里每一层都填满的开源参考实现：28 个 subagents、125+ skills、60 个 slash commands、多语言 rules、PM2 编排、AgentShield 安全扫描。50K+ stars 说明这套思路被认可。

> [!important] 它的存在证明了什么
> 你能不能"自己组装一套 Harness"是 [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]] 的成熟度试金石。ECC 把 [[wiki/agent-engineering/philosophy/harness-成熟度|三层成熟度]]的 L1/L2/L3 全部走通——可以当成参考样板研究每一层应该装什么、按什么节奏交互。它不是"装一下就能用"，更适合**对照自己的 setup 看缺了什么**。

> [!compare] ECC 各组件对应到六层架构
> | ECC 组件 | 对应六层架构的层 |
> |---|---|
> | 28 个 agents（planner / architect / TDD guide / security reviewer …） | [[claude-code-六层架构\|Subagents]] 层 |
> | 125+ skills（前后端、TDD、安全、多语言） | [[agent-skills\|Skills]] 层 |
> | 60 个 commands（`/plan` `/security-scan` `/multi-execute` …） | Tools 层（自定义 [[wiki/claude-code/claude-code\|slash command]]） |
> | 多语言 rules（按 `common/` + 语言目录） | [[claude-rules\|.claude/rules/]] 层 |
> | AgentShield（1282 测试 / 102 规则） | [[hooks\|Hooks]] 层 + Verifiers 层 |
> | PM2 多 Agent 编排 + multi-plan/multi-execute | [[wiki/agent-engineering/workflow/coordinator-模式\|Coordinator 模式]] 的具体实现 |

**关键设计决策**

- **跨平台**：同一套 skills/agents 在 Claude Code、Codex、Cursor、OpenCode 都能用——印证 [[agent-skills|Skills 规范]] 是平台无关的资产
- **持续学习**：自动从会话中提取模式生成 skills——让 [[wiki/claude-code/auto-memory|Auto Memory]] 升级成"团队共享的可执行经验"
- **Token 优化**：model routing（贵的大模型只在必要时用）+ strategic compact + memory persistence——印证 [[wiki/agent-engineering/context/context-window|上下文窗口]]是稀缺资源
- **Verification Loop**：checkpoint + 持续验证——是 [[wiki/agent-engineering/workflow/验证驱动|验证驱动]]的产品化

> [!warning] Rules 不能由插件分发
> ECC 的安装提到一个细节：**插件机制不能自动分发 [[claude-rules|.claude/rules/]] 文件**——必须 `git clone` 仓库再执行 `./install.sh <language>` 把 rules 拷贝到本地。这反过来说明：rules 是项目级 / 个人级配置，按设计就不该被外部插件随意覆盖。

> [!example] 怎么"借鉴"而不"复制"
> 直接全量装 ECC 的代价是：125+ skills 同时加载会显著拉高 Claude 的 [[wiki/agent-engineering/context/cache-命中率|cache miss]]，且大部分 skills 你不会用。建议姿势：
>
> 1. 读 ECC 的 `agents/` 和 `commands/` 目录，**借鉴 prompt 写法**而非完整安装
> 2. 选少量真正常用的 skills（如 `tdd-guide`）进自己的 `.claude/skills/`
> 3. 把 AgentShield 的安全规则单独抄进 [[hooks|hooks]]，不需要整套 PM2 体系

> [!tip] 配套读物
> ECC 作者发了两份指南——**Shorthand**（基础）和 **Longform**（Token 优化、memory persistence、eval、并行化）。Longform 与 [[wiki/agent-engineering/workflow/long-horizon-agent|Long Horizon Agent]] 高度相关，值得对照看。

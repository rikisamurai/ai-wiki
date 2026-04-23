---
title: Codex Plugin for Claude Code
tags: [claude-code, codex, plugin]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/🛠️claude-code-tools]]"
last-ingested: 2026-04-23
status: draft
---

OpenAI 官方发布的插件，把 Codex 接入 Claude Code 作为**第二审阅者和后台执行器**。它不是"用 Codex 替代 Claude"，而是 [[wiki/ai-coding/writer-reviewer-模式|Writer/Reviewer 模式]]的产品化——主写者用 Claude，关键节点请异系模型来挑刺，是一种廉价的"对抗性 review"。

> [!important] 为什么用"另一家的模型"做 reviewer
> 同一个模型给自己 review 等于"你自己检查自己的作文"——已知盲区会被一并继承。换 Codex 来 review，至少能撞出**模型选择本身的偏差**：Claude 写代码偏哪些假设、Codex 倾向哪些质疑。这是 Writer/Reviewer 模式比"同系双 Agent 编程"更进一步的地方——异系模型 > 同系不同会话 > 同会话自检。

> [!compare] 三个核心命令
> | 命令 | 用途 | 适合场景 |
> |---|---|---|
> | `/codex:review` | 普通只读 review，可加 `--base main` 比较 | 提交前请 Codex 看一眼 diff |
> | `/codex:adversarial-review` | **专门挑刺**：质疑设计、隐藏假设、边界条件 | 重要决策前压力测试方案 |
> | `/codex:rescue` | 把任务委派给 Codex subagent | 排障 / 修复 / 续跑卡住的任务 |

**核心实战流——后台 review，回来取结果**

```bash
/codex:review --background           # 派出去
/codex:status                         # 查进度
/codex:result                         # 取结论
```

> [!example] 对抗性 review 的提示词
> ```bash
> /codex:adversarial-review --background \
>   look for race conditions and question the chosen approach
> ```
> 这条命令的精髓在 `question the chosen approach`——明确告诉 Codex 不是来确认你做对了，是来挑战你的方向。Reviewer 默认会偏温和，必须强制它"持反对立场"才能挖出价值。

> [!tip] 委派排障，不是委派思考
> `/codex:rescue` 适合**已经定位但修不动**的 bug——比如"测试在某 commit 后开始挂了，找出原因并修复"。**不要**用它做"我不知道接下来该干什么"——那种问题需要主线程 Claude 维持上下文连贯，换会话只会丢信息。

**安装**（前置：ChatGPT 订阅或 OpenAI API key + Node 18.18+）

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

> [!warning] 代价：双倍 token
> 后台 Codex 会话有自己的 [[wiki/ai-coding/context-window|context window]]——你为同一份代码同时付 Claude 和 Codex 的 token。"对每条 PR 都跑一次 codex:review" 在小项目划算，在大型 monorepo 是显著开销。建议只在**进合并前**或**重大设计决策时**触发。

**关联**：[[wiki/aigc/coordinator-模式|Coordinator 模式]]（Codex 是另一个 worker） / [[wiki/ai-coding/writer-reviewer-模式|Writer/Reviewer 模式]] / [[wiki/ai-coding/subagent-上下文隔离|Subagent 上下文隔离]]（同样适用 - 委派 = 隔离）

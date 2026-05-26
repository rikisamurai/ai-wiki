---
title: caveman 超压缩通信模式
tags: [token-budget, prompt, context]
date: 2026-05-26
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Matt Pocock Skills - 人类满分工程师的自我蒸馏]]"
last-ingested: 2026-05-26
status: draft
---

`/caveman` 是 [[wiki/skills/matt-pocock-skills|Matt Pocock Skills]] 里的一个"原始人模式"指令——让 AI 用最少的词回复，丢弃所有客套话、过渡词、解释性废话，宣称可节省约 75% token。本质是给当前对话临时切换到"telegram 风格"，专为节约成本和加速反馈而设计。

> [!example] 风格对比
> **普通模式**：
> > "好的，我会帮您查看这段代码并找出问题所在。让我先读取一下相关的文件，然后我们一起分析其中可能存在的几个潜在问题点……"
>
> **caveman 模式**：
> > "读 src/x.ts。看到了。bug 在 23 行：未处理空数组。改成 `arr?.[0] ?? def`。"

## 它真正省的是什么

> [!important] 省的是 output token，不是 input
> input prompt 进了 [[wiki/agent-engineering/context/prefix-cache|prefix cache]] 之后，重复读的成本接近零；真正贵的是 output。caveman 模式压的是 output，所以它的优势在**长对话 / 高频回合**场景才显著——一次性提问感受不强。

## 与 [[wiki/agent-engineering/context/cache-命中率|cache 命中率]] 的关系

caveman 是**对话风格层**的优化，prefix cache 是**协议层**的优化，两者正交：
- prefix cache 让 input 的相同前缀只计费一次（每 [[wiki/agent-engineering/context/cache-keep-alive|cache TTL]] 一次）
- caveman 让每次 output 的 token 数下降到 1/4 左右

> [!compare] caveman 与"沉默 agent"风格的差异
> 一些 [[wiki/agent-engineering/workflow/agent-可读性|agent 可读性]]实践（如 Claude Code 主线对外少说话、多干活）走的是**减少自我评论**的路线；caveman 是**整体语言风格压缩**——前者保留信息密度、后者用电报体牺牲流畅度。**自动化流水线场景**用 caveman 不损失什么；**人机对话场景**用 caveman 会让协作感降级，谨慎切换。

## 何时不该用

- **教学 / 解释代码**：用户需要的就是"详细推理过程"，caveman 反而碍事
- **设计讨论**：思路演化路径本身有价值，省掉只剩结论会丢上下文
- **第一次定义任务**：[[wiki/agent-engineering/workflow/采访驱动-spec|采访阶段]]需要 AI 多问、人多答，caveman 压不出好需求

## 关联

- 同源框架：[[wiki/skills/matt-pocock-skills|Matt Pocock Skills]]
- 同类优化：[[wiki/agent-engineering/context/compact-vs-clear|/compact vs /clear]]——压缩历史而非压缩风格
- 反向参考：[[wiki/agent-engineering/workflow/agent-可读性|agent 可读性]]——什么时候需要 agent 多说话

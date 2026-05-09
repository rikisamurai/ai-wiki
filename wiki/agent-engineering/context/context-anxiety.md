---
title: Context Anxiety（上下文焦虑）
tags: [context, model-quirks, prompt-engineering]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: stable
---

[[cursor|Cursor]] 团队给某个模型的怪癖起的名字：**上下文窗口快填满时，模型开始拒绝执行任务、犹豫地说"任务看起来太大了"**。它跟 [[wiki/agent-engineering/context/context-rot|Context Rot]] 不同——后者是模型决策质量降级（仍在干活但变笨），前者是模型直接**罢工**。Cursor 的解法不是换模型，而是调 prompt 缓解。

## 表现与诊断

> [!example] 怎么辨认
> - 用户问一个具体任务，模型不开始执行
> - 模型回复诸如"这个任务规模较大、建议拆分""我建议先讨论方案"等
> - 把对话清空 / 走 [[compact-vs-clear|/clear]] 后同样模型同样任务能正常做
> - 在新窗口起步时不会出现
>
> 关键信号：**任务复杂度没变、上下文消耗变了**。如果换会话后能做，几乎一定是 context anxiety 而不是 capability 限制。

## 为什么会出现

> [!note] 训练数据中的"自我审慎"信号
> 一种解释：训练数据里"长上下文 + agent 任务"的样本里，agent 在面对超长 history 时常给出谨慎/拒绝的回答（人类标注偏好"不要硬上"）。模型把这个统计规律泛化到了**对话过长就该犹豫**——但实际上很多长对话只是 task 复杂、不该拒绝。
>
> 这是模型 alignment 训练在某些场景的副作用——**该谨慎和不该谨慎被一起学了**。

## Cursor 的缓解：prompt 调整

> [!tip] 用 prompt 反向激励
> Cursor 文章只说"通过调整 prompt，成功减轻了这种行为"——没披露具体 prompt。常见做法：
> - 明确告诉模型"长上下文是工程需要、不是任务复杂的信号"
> - 加 "继续执行"的 affirmative framing
> - 在系统 prompt 里塞 "**上下文长度不是衡量任务难度的依据**"
>
> 这是 [[per-model-harness]] 的典型应用——模型怪癖通过 harness 层缓解，而不是等模型迭代修复。

## 与 [[wiki/agent-engineering/context/context-rot|Context Rot]] 的差异

> [!compare] 同源不同表现
> | 维度 | [[wiki/agent-engineering/context/context-rot\|Context Rot]] | Context Anxiety |
> |---|---|---|
> | 触发 | 长上下文 + 累积错误 | 长上下文（即使没有错误） |
> | 表现 | 决策质量降级（仍在干活但变笨） | 拒绝/犹豫执行 |
> | 根因 | 上下文里噪声多 / 重要信号被埋 | 模型把"长上下文"误读成"应谨慎" |
> | 应对 | [[compact-vs-clear\|compact / clear]]、[[wiki/agent-engineering/context/会话管理动作\|会话管理]] | per-model prompt 调整 |
>
> 两者也可叠加——长会话同时触发 rot 和 anxiety。先 [[compact-vs-clear|compact]] 减 rot，再用 prompt 抗 anxiety。

## 与 [[wiki/agent-engineering/context/冻结快照模式|冻结快照模式]] 的协同

冻结快照可以缓解 anxiety 的二阶问题：你 fork 一个干净状态出去做新任务，绕开当前长 context 触发 anxiety 的窗口。但 fork 本身不能从根上修——只是给单次任务一条出路。

## 一个 anti-pattern：当真接受模型的 push back

> [!warning] 别让 anxiety 改变你的工程判断
> Anxiety 的危险在于它像有道理的建议——"这任务太大了，我们先拆分"听起来合理。但当任务实际并不大时，你被 push back 反而会浪费一次会话切换 + reload 上下文。
>
> 经验法则：**如果任务在新窗口能做，就是 anxiety；不要因为模型说"太大"就当真要拆分**。

## 关联

- 上游问题：[[per-model-harness]]——这是 model-specific 怪癖的代表
- 同族 context 现象：[[wiki/agent-engineering/context/context-rot|Context Rot]]、[[wiki/agent-engineering/context/cache-失效陷阱]]
- 缓解工具：[[wiki/agent-engineering/context/compact-vs-clear|Compact vs Clear]]、[[wiki/agent-engineering/context/会话管理动作]]、[[wiki/agent-engineering/context/冻结快照模式]]
- 检测信号：[[工具错误分类法]] 里 `UserAborted` 上升 + agent 拒绝执行的 transcript pattern
- 上游工具：[[cursor]]

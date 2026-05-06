---
title: Per-Model Harness（每模型定制框架）
tags: [philosophy, harness, model-specific]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
last-ingested: 2026-05-06
status: draft
---

[[harness-engineering|Harness Engineering]] 的精细化范式：**同一个 framework 抽象，在工具格式、提示词、错误处理上对每个模型/版本独立定制**。[[cursor|Cursor]] 的实践：OpenAI 模型用 patch 编辑、Anthropic 模型用 string-replace；prompt 也按 provider 甚至 model version 分别写。"框架抽象不依赖具体模型，但每个模型可深度定制"。

## 模型有"训练时偏好"

> [!important] 同一工具对不同模型代价不同
> Cursor 的关键观察：
> - **OpenAI 模型**经过训练习惯**基于 patch 的格式**编辑文件
> - **Anthropic 模型**经过训练习惯**字符串替换**
>
> 两类模型其实**都能用**两种工具——但**给它们不熟悉的那一种**：
> - 额外消耗 reasoning token（理解陌生格式）
> - 错误率显著上升
>
> 所以 harness 在每个模型槽位**配置它训练时用的工具格式**。这是省 token、降错率的"免费"优化。

## 提示词也要 per-model

> [!example] 风格差异需要不同 prompt 风格
> Cursor 总结：
> - **OpenAI 模型**：偏字面理解、更精确——指令要写**严格、显式**
> - **Claude**：偏直觉、对不精确指令容忍度高——指令可以**更高层次、更短**
>
> 把同一段 prompt 喂两个模型，效果差距可能比"换更强的模型"还大。

## Early Access 调优流程

> [!note] 拿到新模型后的几周
> Cursor 拿到新模型 Early Access 后的标准流程：
> 1. 从**最接近的现有模型**的 framework 出发拷贝一份
> 2. 跑离线 eval（[[cursorbench|CursorBench]] + 内部套件）找模型容易出错或困惑的地方
> 3. 团队成员实际使用 + 反馈
> 4. 据此调框架——改 prompt、换工具格式、加缓解 prompt
> 5. 反复迭代直到模型-框架组合可发布
>
> 这是 [[eval-driven-development|EDD]] 在模型升级场景的具体实例：评估先行、迭代收敛。

## 模型怪癖也通过 harness 缓解

> [!example] 上下文焦虑的范例
> Cursor 在某个模型上观察到：上下文窗口快填满时，模型开始**拒绝执行任务**，犹豫地说"任务太大了"——他们称为 [[context-anxiety|Context Anxiety]]。解法不是换模型，而是**调 prompt 缓解**——这是 per-model 调优的典型例子：模型有怪癖、harness 给护栏。

## 与"通用 prompt"的对照

> [!compare] One-prompt-fits-all vs Per-model
> | 维度 | 通用 prompt | Per-model harness |
> |---|---|---|
> | 维护成本 | 低（一份） | 高（N 个 provider × M 个版本） |
> | 性能上限 | 中等（必须迁就最弱模型） | 高（每个模型在自己最舒服的接口上跑） |
> | 模型升级成本 | 重测整套 | 只改受影响模型槽位 |
> | 适合 | 早期 / 演示 / 个人项目 | 生产化、规模化 |
>
> Cursor 选 per-model 是因为他们 multi-provider，对每个 provider 都要做到 SOTA。[[claude-code|Claude Code]] 主要走 Anthropic 自家模型，Per-model 复杂度低很多——它把精力投在 [[wiki/skills/agent-skills|Skills]] 和 [[claude-code-六层架构|六层架构]]上。

## 切换的代价

per-model harness 有个直接代价：[[mid-chat-model-switch|聊天中途切换模型]] 变得棘手。要切 prompt、切工具集、还要告诉新模型"前面是别的模型生成的对话"。具体见 [[mid-chat-model-switch]] 那页。

## 关联

- 范式上游：[[harness-engineering]]、[[cursor]]
- 调优过程：[[eval-driven-development]]、[[cursorbench]]
- 衍生工程问题：[[mid-chat-model-switch]]、[[context-anxiety]]
- per-model 维度的另一面：[[工具错误分类法|工具调用错误分类法]]——baseline 也要 per (tool, model)
- 跟 Skills 跨模型的对照：[[wiki/skills/agent-skills|Agent Skills 规范]]——skills 设计上跨模型可用，跟 per-model harness 是不同抽象层

---
title: Keep Rate（保留率）
tags: [evals, metric, in-product]
date: 2026-05-06
sources:
  - "[[sources/clippings/持续改进我们的智能体框架]]"
  - "[[sources/posts/aigc/ai-coding/tools/Git AI - 追踪 AI 生成代码的 Git 扩展]]"
last-ingested: 2026-05-08
status: draft
---

[[cursor|Cursor]] 用的 in-product 质量度量：**对 agent 提出的一组代码变更，跟踪固定时间间隔后还有多少比例留在用户代码库里**。比例高 = 用户接受了 AI 的改动；比例低 = 用户改回去了或 agent 自己反复修。它跟 [[agent-evals|automated eval]] 互补——后者评 synthetic task，Keep Rate 评真实用户的脚投票。

## 为什么这个指标有意义

> [!important] "成功" 不只是 "code passed test"
> 一段 AI 写的代码可能：
> - 通过单测（在 [[coding-agent-eval|coding eval]] 里算 pass）
> - 但用户两小时后把它改回原样——因为风格不符 / 命名不行 / 引入了反模式
>
> Keep Rate 抓的就是后半段。它不要求事先定义"什么是好代码"——**用户的留存行为本身就是判定**，比 LLM rubric 还干净。

## 在 Cursor 评估栈里的位置

> [!example] Keep Rate 解决什么 benchmark 解决不了的事
> | 度量 | 抓什么 |
> |---|---|
> | [[cursorbench\|CursorBench]] | 标准化 task 上的 pass 率（趋势仪表盘） |
> | 内部 eval 套件 | 私有/敏感场景的 pass 率 |
> | **Keep Rate** | **真实用户用脚投票留下了多少 AI 代码** |
> | A/B test 的 latency / token / cache hit | 工程效率指标 |
> | [[语义满意度信号]] | LLM 读用户后续回复推断满意度 |
>
> Keep Rate + 语义满意度信号是 Cursor 在 A/B 实验里对"质量"这件模糊事的两个具体抓手。

## 适用与边界

> [!warning] 不要单独看
> Keep Rate 单独看会被几类信号污染：
> - 用户接受了但**之后再改**——你得选合理的时间窗口
> - 用户接受了但**根本没用**——保留 ≠ 价值
> - 用户拒绝是因为**任务本身错了**——不是 AI 写得差
>
> 必须配合：
> - 多个时间窗（5min / 1d / 1w 多看几张）
> - **iteration count**：用户为完成任务跟 agent 来回了几轮
> - **rollback rate**：保留后又被删/改的比例

## 类似度量在其他工具里

> [!compare] in-product 质量度量族
> | 工具 | 度量 | 抓什么 |
> |---|---|---|
> | Cursor | **Keep Rate** | 改动留存 |
> | GitHub Copilot | acceptance rate | 候选被接受比例 |
> | Claude Code / Codex | thumbs up / down | 用户显式反馈 |
> | gstack | telemetry（opt-in） | skill 成功率、duration |
>
> Keep Rate 比 acceptance rate 更"延后"——后者只看接的瞬间，前者看一段时间后还在不在。延后版抓的是**真正的留存价值**，瞬时版可能被一时心动带偏。

## 与 [[capability-vs-regression-eval|regression eval]] 的关系

Keep Rate 适合做**生产侧 regression 信号**——一旦它在某个 cohort 上突然下跌，几乎一定是某次 harness/模型更新出了问题。比 [[wiki/agent-engineering/workflow/eval-方法矩阵|production monitoring]] 单看 latency/error rate 更接近"agent 真实质量"。

## 与 commit 级 Attribution 的关系

> [!tip] Keep Rate 跌了，用 attribution 找凶手
> Keep Rate 是聚合数字——告诉你"AI 改动的留存率掉了"。要查具体是什么原因，需要把行级 attribution 接上来：[[wiki/claude-code/git-ai|Git AI]] 在 commit 上记录"哪行是哪个 agent / model / prompt 写的"，反查丢失的那部分留存属于谁。这是 Keep Rate 的下钻能力。详见 [[wiki/agent-engineering/workflow/ai-代码-attribution|Attribution 自报 vs 检测]]。

## 关联

- 工具栈：[[cursor]]
- 评估上游：[[agent-evals]]、[[eval-方法矩阵]]
- 同族度量：[[语义满意度信号]]、[[cursorbench]]、[[采纳率]]
- 事后归因互补：[[wiki/agent-engineering/workflow/ai-代码-attribution|AI 代码 Attribution]]、[[wiki/claude-code/git-ai|Git AI]]
- 与 regression：[[capability-vs-regression-eval]]

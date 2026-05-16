---
title: Agent Trace 与可观测性
tags: [observability, trace, agent-ops]
date: 2026-05-16
sources:
  - "[[sources/clippings/你不知道的 Agent：原理、架构与工程实践]]"
last-ingested: 2026-05-16
status: draft
---

Trace 是 Agent 调试的前提：**没有完整记录，失败案例就没法稳定复现**。传统 APM 只监控延迟和错误率，接口层看起来正常，但问题可能出在模型某一轮做出了错误决策——只有回看完整 Trace 才能定位。

## Trace 必须记录什么

```
每次 Agent 运行：
├── 完整 Prompt，含系统提示
├── 多轮交互的完整 messages[]
├── 每次工具调用 + 参数 + 返回值
├── 推理链（如有 thinking 模式）
├── 最终输出
└── token 消耗 + 延迟
```

规模上来后还应具备**语义检索能力**：能查询"哪些 Trace 里 Agent 混淆了两种工具"，而不只是精确字符串匹配。靠人工全量审查是跟不上的，自动化是前提。

## 两层可观测性

**第一层 — 人工抽样标注**：基于规则采样错误案例、长对话、用户负反馈，由人工判断执行质量和失败原因。主要用来摸清失败模式，并给第二层提供校准数据。

**第二层 — LLM 自动评估**：对更大范围的 Trace 做全量覆盖，以第一层标注作为校准依据。

只跑第二层，评分标准容易漂移；只靠第一层，规模上覆盖不了真实流量。**两层必须一起用**。

## 在线评测采样策略

全量评测成本高，完全随机采样容易错过关键 Trace。推荐对 10%–20% 的 Trace 运行在线评测，按规则路由：

| 场景 | 采样率 | 原因 |
|---|---|---|
| 用户明确负反馈 | 100% | 已知问题点 |
| token 超阈值 | 优先 | 可能在绕圈子 |
| 时间窗口随机 | 每天固定时段 | 覆盖正常流量 |
| 模型/Prompt 变更后 | 头 48 小时全量 | 确认无退化 |

## 事件流架构

Agent Loop 在三个节点发出事件，Trace 同步落盘后分发给各下游，**主循环不需要为任何下游改代码**：

```
on tool_start: emit { type, tool_name, input, timestamp }
on tool_end:   emit { type, tool_name, result, duration }
on turn_end:   emit { type, turn_output }

agent.on("event") -> write_to_logs
agent.on("event") -> update_ui
agent.on("event") -> send_to_eval_framework
```

## 先查环境，再动 Agent

> [!warning] 评测噪声陷阱
> 看到评测分数下降，先检查**基础设施错误率**，而不是立刻修改 Agent。资源限制导致进程被杀、评分器本身有 bug、环境状态在测试间共享——这些问题在表现上与模型退化一模一样。先修评测系统，基于失真信号改 Agent 可能把本来正常的部分改坏。

## 相关页面

- [[workflow/agent-evals|Agent Evals]] — 评测体系的搭建方法
- [[workflow/读-transcript|读 Transcript]] — 通过逐步审阅轨迹发现问题
- [[agent-loop|Agent Loop]] — Trace 以 Loop 的 messages\[\] 为基础
- [[workflow/eval-方法矩阵|Eval 方法矩阵]] — 评测方法选择的决策框架

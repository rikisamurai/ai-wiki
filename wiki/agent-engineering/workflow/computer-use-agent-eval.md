---
title: Computer Use Agent Eval
tags: [evals, computer-use, webarena]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: draft
---

Computer use agent 用**和人类一样的接口**操作软件——截图、鼠标、键盘——而不是 API。这意味着它能驱动任何 GUI 应用（设计工具、遗留企业软件），但也意味着评估必须在**真实或沙箱环境**里跑，并通过环境/数据库/文件系统的状态变化来判定成功。WebArena 测浏览器、OSWorld 测整个操作系统。

## 评估必须看后端状态

> [!warning] 看 UI 不够
> 一个常见错误是只检查 UI 终态——例如看到"订单已下"页面就算过。但 agent 可能：
> - 走到了那个页面，但订单实际没进数据库
> - 走到了页面，但订错了商品/数量
>
> WebArena 因此**同时**做 URL/page state 检查 + 后端状态检查（数据库里是否真有这条订单）。OSWorld 检查得更广：文件系统、应用配置、数据库、UI 元素属性。

## WebArena / OSWorld

> [!compare] 浏览器 vs 整个 OS
> | 维度 | [WebArena](https://arxiv.org/abs/2307.13854) | [OSWorld](https://os-world.github.io/) |
> |---|---|---|
> | 范围 | 浏览器内任务 | 完整操作系统控制 |
> | 检查项 | URL、page state、后端状态 | 文件系统状态、应用配置、数据库内容、UI 元素属性 |
> | 沙箱 | docker 化的 web app | 完整 VM |

## DOM vs 截图：一个被低估的取舍

> [!important] token 效率 vs 延迟
> 浏览器 agent 必须在 DOM 解析和截图之间选：
> - **DOM 交互**：执行快、但消耗 token 多
> - **截图交互**：慢、但 token 高效
>
> 例子（Claude for Chrome 的实测）：
> - "总结一下 Wikipedia"——DOM 提取文本更高效
> - "在 Amazon 找一款新笔记本电脑壳"——截图更高效（整页 DOM 太大）
>
> Claude for Chrome 团队专门做了一组 eval **检查 agent 是否在每个上下文里选对了工具**——这种"meta 决策评估"是 computer use 特有的一类。

## grader 设计要点

| grader 类型 | 用途 |
|---|---|
| **state_check**（数据库/文件系统） | 主 grader——验证 outcome 真的发生了 |
| **screenshot diff** / page DOM 校验 | 辅助验证 UI 状态 |
| **tool_calls** | 但**不要规定鼠标点击顺序**，参见 [[eval-grader-三类|不评路径只评产物]] |
| **transcript metrics** | n_turns、token 消耗、completion latency |

## 与其他 agent 的方法学共享

- 与 [[conversational-agent-eval|conversational agent]] 一样，可用 LLM 模拟用户进行扩展交互
- 与 [[research-agent-eval|research agent]] 一样，需要警惕只看 UI 不看后端的"似是而非的成功"——本质是 [[plausible-code|plausible code]] 在 UI 自动化领域的对应

## 关联

- 总览：[[agent-evals]]
- 检索域：[[wiki/retrieval/browser/cdp|CDP]]、[[wiki/retrieval/browser/cdp-能力边界|CDP 能力边界]]——跟 computer use 不同的另一条浏览器自动化路径
- 同类不同 agent：[[coding-agent-eval]]、[[conversational-agent-eval]]、[[research-agent-eval]]
- 度量：浏览器/OS 任务通常 [[pass-at-k-vs-pass-power-k|pass^k]] 更重要——一次失败可能误买、误删

---
title: OPC（One Person Company）
tags: [opc, ai-coding, org-design]
date: 2026-04-22
sources:
  - "[[sources/inbox/我的 Vibe Coding 项目]]"
  - "[[sources/inbox/为什么你的\"AI 优先\"战略可能大错特错？]]"
last-ingested: 2026-04-22
status: stable
---

# OPC（One Person Company）

> [!note] TL;DR
> "**一人公司**"——一个人 + 一群 Agent，做出过去需要十几人团队才能交付的多产品矩阵。它不是科幻，而是 idoubicc 这类开发者已经在走的路：3 个月用 [[vibe-coding|Vibe Coding]] 同步推进 10+ 个产品（WorkAny / ClawHost / OpenClaw / CodeAny ...）。但它的代价同样真实——**护城河消失、注意力稀缺、商业能力变成新瓶颈**，详见 [[vibe-coding-的代价]]。

## 实证形态

idoubicc 的一份"3 个月作品清单"：

| 项目 | 定位 |
|---|---|
| WorkAny | 通用云端 Agent |
| ClawHost | Claude Code 托管平台 |
| ChatClaw / WeClaw | 聊天端 Agent 入口 |
| CoRich / FastClaw | 各类垂直 Agent |
| AnyClaw / ClawRouter | API 网关 / 路由 |
| Clawork / ClawBaby | 业务工具 |
| Open Agent SDK | 自研 Agent 运行时（4 语言版本） |
| CodeAny / CCOnline | Claude Code 复刻 / 云托管 |

> "这些项目全部由 Claude Code 完成，我负责提需求、测试、再提需求，**未参与过代码编写工作**。"

## 架构师 + Agent = 100 人产能

OPC 的可行性建立在 [[架构师-操作员二分]] 的极端形态上：

- 架构师 = 1 人（你自己）
- 操作员 = 0 人（用户 + 你的 LLM 测试自己当）
- 工人 = N 个 Agent

CREAO 的预言（25 人架构师 → 100 人产能）在 OPC 这里压缩到 **1 人架构师 → 多产品并发**。

## 工作姿势

```
路上灵感来了
   │ 手机 Discord 发给 OpenClaw
   ↓
[ OpenClaw 调用 Claude Code 实现 ]
   │ 后台跑
   ↓
回家打开电脑验收
   │ 不满意 → 再发消息让它改
   ↓
上线
```

**人不再是写代码的瓶颈，而是"提需求 + 验收"的瓶颈**——这正好印证了 [[review-带宽瓶颈]]。

## 为什么现在才可能

OPC 早就是创业理想，过去做不到的原因是"实现"成本——需要工程师、设计师、运维。AI Coding 把实现成本压到接近零之后，瓶颈完全转移：

| 过去稀缺 | 现在稀缺 |
|---|---|
| 写代码的工程师 | 提需求的产品力 |
| DevOps / 运维 | 注意力 / 持续性 |
| 测试 QA | 商业落地能力 / 流量 |

## 暗面

> [!warning] 不要把 OPC 浪漫化
> idoubicc 的反思（详见 [[vibe-coding-的代价]]）：
> - 同时开 10 个项目 → 没一个做得特别好
> - "测试资源极度缺乏" → AI 写得快，人验不过来
> - "用 AI 复刻一个项目变得极度容易，我不明白这个时代产品的护城河在哪里"
> - "我时常感到迷茫，不知道做这些所谓'产品'的意义在哪里"

OPC 把"可以做"扩到接近无限，但"该做什么 / 做多深"反而成了更难的问题。

## 关联

- 组织前提：[[架构师-操作员二分]]——OPC 是这套二分法的极端
- 工作姿势：[[vibe-coding]] / [[harness-engineering]]
- 风险与反思：[[vibe-coding-的代价]]
- 经济学层：实现成本归零 → 价值在哪里重新分配

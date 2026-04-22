---
title: Vibe Coding
tags: [vibe-coding, anti-pattern, ai-coding]
date: 2026-04-22
sources:
  - "[[sources/inbox/为什么你的\"AI 优先\"战略可能大错特错？]]"
  - "[[sources/inbox/我的 Vibe Coding 项目]]"
last-ingested: 2026-04-22
status: stable
---

# Vibe Coding（凭感觉编程）

> [!note] TL;DR
> Vibe Coding 是当下最常见的 AI 编程姿势——打开 Cursor、不断调提示词直到代码能跑通、提交、重复。**它适合做原型验证，做不了生产系统**。一个真正用于生产的系统必须稳定、可靠、安全；当 AI 写代码时，你需要构建的是兜底系统，那些 prompts 都是用完即弃的。

## 操作方式

```
1. 打开 Cursor / Claude Code / Copilot
2. 写一段 prompt 描述想要的功能
3. 跑一下，看效果
4. 不对劲？再调 prompt，让 AI 改
5. 能跑了，提交
6. 下一个功能，重复
```

整个过程的"质量信号"是单一的：**能跑就行**。看到结果合心意就放过，看不顺眼就再让 AI 改一改。

## 为什么只能做原型

它的全部前提是"反馈来自肉眼"——你看一眼输出，觉得对就过。这个前提在原型期成立，在生产期完全失效：

- **稳定性**：原型崩了你重启，生产崩了用户骂街
- **可靠性**：原型偶尔出错你笑笑，生产出错就要赔钱
- **安全性**：原型没人攻击，生产每天被探测
- **演进性**：原型不需要明天再读这段代码，生产代码会被几十个 PR 反复触碰

要解决这些，靠的不是更聪明的 prompt，而是 [[harness-engineering|Harness Engineering]] 那套兜底基础设施：自动化测试、CI/CD、A/B 验证、监控告警、回滚机制。

## 谁是它的合理用户

参见 [[review-带宽瓶颈]] 的判断："如果你是 Vibe Coding 的目标用户（业务不严苛、用户即测试者），那'先 accept 再说'是合理策略"。具体场景：

- 个人脚本、一次性数据处理
- 早期想法验证（验证完不上线，或者上线后用户量极小）
- 内部工具，崩了影响范围极小
- 学习/教学场景

## 真正要构建的是系统，不是 prompts

> [!warning] 核心误区
> Vibe Coding 把 prompt 当成产物。但 prompt 的复用价值很低，模型一升级、需求一变、上下文一动，prompt 就废了。生产工程要构建的是**承载 AI 工作的系统**——测试支架、流水线、监控、回滚——这些才是会被反复使用、长期演进的资产。

这恰好是 [[harness-engineering|Harness Engineering]] 的核心论点。

## 与 AI First 的关系

很多团队混淆了 Vibe Coding 和 [[ai-first-vs-ai-assisted|AI First]]——以为"AI 能写出代码就是 AI First"，结果做出来的是**没有兜底的 Vibe Coding 流水线**。这种状态下功能越上越多、bug 也越积越多，[[ai-first-工程前提]] 里的五件事一项都没做。

## 实战代价

它能跑通不代表没成本。一个 OPC 创业者三个月用 Vibe Coding 做了 13 个产品，复盘出 4 个真实代价（注意力 / 验收带宽 / 护城河 / 意义感）——详见 [[vibe-coding-的代价]]。

## 与其他概念的关联

- 反面：[[harness-engineering]] / [[ai-first-vs-ai-assisted]]
- 适用判断：[[review-带宽瓶颈]]——靠人 review 兜底就别搞 vibe
- 风险点：[[plausible-code]]——AI 生成的代码"看起来对"≠ 真的对
- 极端形态：[[opc-一人公司]] / [[vibe-coding-的代价]]

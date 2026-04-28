---
title: Agent 等待时间（Human Wait）
tags: [metric, harness-engineering, productivity]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/从Spec Coding到Harness：AI Coding的两次范式转变与实践总结]]"
last-ingested: 2026-04-22
status: stable
---

衡量 AI Coding 效率的真正指标，不是 Token 消耗量、也不是 AI 代码生成占比，而是 **Agent 因等待人类反馈而浪费了多少时间**（`human wait`）。目标是把它降为 0——让 Agent 24 小时不间断地在"开发-测试-修复"的闭环里自主工作。

> [!warning] 容易误用的指标
> "AI 写了多少代码"鼓励数量而非质量；"Token 消耗"鼓励压缩而非效果。两者都让人忘了真正的瓶颈在哪。Agent 等待人 = 闲置算力 + 串行延迟，是 [[harness-engineering|Harness Engineering]] 想消灭的最大浪费。

**怎么才能降为 0**：把过去依赖人类的环节工程化为 Agent 可自驱的反馈源——

- 测试用例 + CI 替代人工跑通验证
- Lint + 静态检查替代人工 Code Review 的"硬规则"部分
- 监控告警 + 日志可读性替代人工排障
- 自动部署到泳道替代人工部署

每消除一个"必须等人"的环节，Agent 自主迭代的时长就增加一段。这正是 [[self-healing-loop|自愈循环]]的工程目标，也是 [[review-带宽瓶颈|Review 带宽瓶颈]]的对偶视角——后者关心人能消化多少，前者关心 Agent 等了多久。

相关：[[harness-engineering]]、[[约束悖论]]

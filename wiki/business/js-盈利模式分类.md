---
title: JS 库的 5 种盈利模式
tags: [frontend, business-model, oss-economics]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析]]"
last-ingested: 2026-04-22
status: stable
---

JavaScript 开源库的商业化路径在 himself65 的市场分析里被归纳为 5 类。只有"部署收费"和"人头收费"两种具备规模化潜力，其余三种本质上是**生存模式**，不是**增长模式**。

> [!note] 五种模式速览
> | 模式 | 代表 | 规模化潜力 | 核心逻辑 |
> | --- | --- | --- | --- |
> | 部署收费 | [[wiki/frontend/web-platform/vercel|Vercel]]、Netlify、Deno Deploy | ✅ | 框架捕获心智 → 平台变现 |
> | 人头收费 | AG Grid、MUI、Kendo UI | ⚠️（被 Vibe Coding 通缩） | [[wiki/business/per-seat-licensing|按席位授权]] |
> | 付费咨询 | NestJS、Fastify | ❌（线性增长） | 维护者工时变现 |
> | 广告变现 | Vue.js、Babel.js、Webpack | ❌（天花板 ~$12K/月） | GitHub Sponsors / Open Collective |
> | 被收购 | npm、Turborepo、[[wiki/frontend/web-platform/bun\|Bun]] | 一次性事件 | 生态卡位价值 > 自身商业价值 |

**部署收费——唯一被 AI 加速放大的模式**："框架 → 平台 → 生态"三段绑死的飞轮模型，详见 [[wiki/frontend/web-platform/vercel|Vercel]]。这条路径在 AI 时代被进一步放大：v0、Bolt.new 等 AI 代码生成工具几乎全部输出 JS/TS，部署平台是天然的变现出口。

**人头收费——面临结构性通缩**：AG Grid（$999/开发者/年）、MUI Pro、Kendo UI 都走 [[wiki/business/per-seat-licensing|Open Core + 按席位授权]] 路线。但 [[wiki/agent-engineering/philosophy/vibe-coding-对-saas-的通缩|Vibe Coding 让"开发者人数"这个计费单位的含义变了]]——一个开发者靠 AI 干三个人的活，企业续约时席位自然缩减。

**付费咨询——天花板在 $100-200 万/年**：线性增长，不可规模化。一个顶级维护者一年最多服务 10-20 家企业客户，组个 3-5 人小团队天花板 $200 万/年。AI 双向影响：常规咨询被 ChatGPT 替代，深度架构咨询反而更值钱，整体规模稳定。

**广告变现——维持，不增长**：Vue.js 是这种模式的天花板：稳定 $12-15K/月，跟使用量（npm 周下载几百万、GitHub stars 20 万+）完全不成正比。每个活跃用户每月贡献不到 $0.01。结构性问题：捐助者付钱因为"感激"而不是"需求"，热度退潮收入立刻下滑（Webpack 被 Vite 取代后被迫加入 OpenJS 基金会就是案例）。

## 被收购：估值看战略卡位

npm 卖给 GitHub、Turborepo 卖给 Vercel、Bun 卖给 Anthropic，估值逻辑都是相同四点：

1. **用户基数与生态位**：是不是不可替代的"基础设施"
2. **技术资产**：能否产生乘数效应（[[wiki/frontend/web-platform/bun|Bun]] 的 JS 运行时之于 Claude Code）
3. **人才**：JS 核心维护者全球不超过几百人
4. **战略卡位**：不让对手拿到，往往比资产本身的商业价值更重要

> [!compare] 总市场规模锚定
> - **TAM**（人数 × ARPU）：$10-80 亿
> - **SAM**（DevOps 市场 × JS 占比 15-25%）：$16-33 亿
> - **SOM**（头部公司可追踪收入加总）：$5-8 亿
>
> SOM/SAM 仅 20-30%，意味着大量 JS 开发者支出仍在流向 AWS、GitHub Actions、Datadog 这些通用平台，JS-native 工具公司还有抢份额空间。

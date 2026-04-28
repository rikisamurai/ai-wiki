---
title: Vercel
tags: [frontend, deployment, business-model]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析]]"
last-ingested: 2026-04-22
status: stable
---

Vercel（原名 ZEIT，2015）是把"前端框架→部署平台→AI 生成"打成一条飞轮的代表公司。靠 Next.js 捕获开发者心智，再把流量导回部署变现，2025 年 ARR ~$2 亿，F 轮估值 $93 亿。

> [!note] 飞轮三段
> 1. **框架** 给开发者 DX：Next.js、Turbopack、Server Components、即时预览
> 2. **平台** 做深度优化：只在自家 hosting 上跑得最顺
> 3. **生态** 反哺框架：shadcn/ui、AI SDK、v0 把 Next.js 变成 AI 生成的默认输出

这三段绑死的策略叫"[[wiki/business/js-盈利模式分类|框架 → 平台 → 生态]]"，也是 Vercel 与同期对手分叉的核心原因。

> [!compare] Vercel vs Netlify（2021 同水位 → 2025 拉开 4 倍）
> | | Vercel | Netlify |
> | --- | --- | --- |
> | 2021 ARR | $25.5M | $22.9M |
> | 2025 ARR | ~$200M（+82% YoY） | ~$46M（三年 ~2x） |
> | 估值 | $9.3B（F 轮） | $2B（2021 后无新轮次） |
> | 核心绑定 | Next.js | 无自有框架，押 JamStack |
>
> Netlify 业务做的事和 Vercel 几乎一样，但没自己的框架就吃不到生态复利，AI 叙事也讲不通。

## 三个不可忽视的对手

- **Cloudflare**：从 CDN 边缘网络反向叠加 Workers/Pages/R2。价格碾压（Workers $5/月 vs Vercel Pro $20/用户/月），但 V8 Isolate 不兼容完整 Node.js，DX 是短板。结论：杀不死 Vercel，但持续压低价格天花板。
- **VoidZero（Vite+）**：Evan You 的新公司复刻 Vercel 老路，但切入更底层的打包工具层。如果 Vite 把各家 meta-framework 的底层全替换掉，覆盖面会比绑死 Next.js 的 Vercel 更大。
- **Bolt.new / Lovable / Replit / Same**：AI 代码生成赛道，[[wiki/frontend/web-platform/webcontainers|WebContainers]] 让浏览器内跑完整 Node.js，输出几乎全是 JS/TS。Vercel 用 v0 + 一键部署 + Next.js + [[wiki/frontend/ui-libraries/shadcn-ui|shadcn/ui]] 的闭环卡住了赛道，护城河不在 AI 生成本身。

## 估值跳变靠的是 AI 叙事

2021–2024 年 SaaS 市场对"AI 原生 vs AI 贴牌"打分极其严格。Twilio/Fastly 加 AI 功能但市场视为补丁，估值砍 75%；Vercel 因 v0 从零设计为 AI 产品，被算 AI 原生，E/F 轮估值翻番。Vercel 的飞轮是 [[wiki/agent-engineering/philosophy/ai-first-vs-ai-assisted|"AI 叙事 = 第二增长曲线"]] 的最佳实证。

**风险点**：

- Next.js 在开发者中口碑下滑（频繁 breaking change、过度服务端化）
- VoidZero 真把 Vite+ 跑通后，Vercel 的"必须用 Next.js 才能享受 DX"叙事会被解构
- v0 这类生成工具一旦被 Anthropic/OpenAI 自家产品整合，可能失去独立存在意义

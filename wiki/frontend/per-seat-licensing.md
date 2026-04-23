---
title: Per-Seat Licensing（按席位授权）
tags: [frontend, business-model, pricing]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析]]"
last-ingested: 2026-04-22
status: stable
---

按开发者人数收费的商业化模式，常与 Open Core 策略捆绑：基础库 MIT 协议免费引流，企业级功能（数据网格、日期选择器、SSO、SLA）按 seat 收费。这是 JS 生态除[[wiki/frontend/vercel|部署收费]]之外第二大可规模化的[[wiki/frontend/js-盈利模式分类|盈利模式]]，但正被 [[wiki/ai-coding/vibe-coding-对-saas-的通缩|Vibe Coding 通缩]] 结构性挤压。

> [!example] 头部代表
> | 厂商 | 价格区间 | 融资状态 |
> | --- | --- | --- |
> | AG Grid | $999-$1,498/开发者/年 | Bootstrapped，~60 人，90% Fortune 500 |
> | MUI X | Pro/Premium 分档 | A 轮 |
> | Kendo UI（Telerik/Progress） | $799-$2,098/开发者 | 上市公司子产品 |
> | Syncfusion | <$100 万营收公司免费 | 私有 |

## Open Core 的两个关键约定

1. **免费层不能阉割得太狠**：开发者会绕路用 [[wiki/frontend/headless-ui|TanStack Table]] 这类纯开源替代方案。AI 生成代码时尤其偏好 MIT 库（训练数据更多）。
2. **付费层卖"AI 替代不了的能力"**：合规审计、WCAG 无障碍认证、官方 SLA、SSO 集成——这些在企业采购流程里是硬性要求。

## 三大压力源

- **AI 默认开源偏好**：ChatGPT/Claude 生成 UI 代码时默认用 [[wiki/frontend/shadcn-ui|shadcn/ui]]、Radix UI、TanStack Table，商业组件库的"默认被选中率"下降
- **[[wiki/frontend/headless-ui|Headless 趋势]]加速**：纯逻辑库 + AI 自动生成样式层，比配置一个商业组件库简单
- **Ghost Seat 问题**：10 人前端团队靠 AI 提效后只需要 6 个人，企业续约缩席位，没法靠提价对冲

## 转型方向（不是换定价模型那么简单）

> [!note] 出路在产品价值定位的重构
> 1. **功能分层加深**：押注合规、SLA、SSO 这类企业刚需
> 2. **从"组件"转向"平台"**：把组件 + 报表导出 + 权限管理捆一起卖，提高替换成本
> 3. **AI 本身成护城河**：内置"AI 驱动的列配置/数据分析"，把 "AI 生成我的替代品" 翻成 "AI 增强我的产品"

AG Grid 这类 bootstrapped 公司没有 VC 增长压力，反而比 VC-backed 对手更从容地完成转型。

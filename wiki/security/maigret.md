---
title: Maigret
tags: [osint, username-search]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

Maigret 是用户名查人的专精工具，覆盖 3000+ 平台，核心差异是**递归追踪**：在 A 平台发现目标的另一个马甲后，自动拿这个新用户名继续搜，顺着线索一路挖到底。

> [!example] 能力
> - 输入：username（可链式扩展）
> - 覆盖：3000+ 平台（远多于 [[wiki/security/blackbird|Blackbird]] 的 600+）
> - 核心：递归——自动用新发现的马甲再发起搜索
> - 开箱即用，`pip install maigret`，**不需要 API Key**
> - 约 33000 GitHub Star（`soxoj/maigret`）

> [!compare] Blackbird vs Maigret
> - **Blackbird**：平台少、出全貌快、带 AI 画像，适合第一棒
> - **Maigret**：平台多、递归深挖、无画像，适合第二棒
>
> 典型用法是 Blackbird 出全貌 → Maigret 顺马甲深挖，完整链路见 [[wiki/security/osint-工具链工作流|OSINT 工具链工作流]]。

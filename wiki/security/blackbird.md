---
title: Blackbird
tags: [osint, username-search]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

Blackbird 是一款用户名 / 邮箱反查工具，把一个昵称或邮箱在 600+ 平台上批量扫一遍，命中哪些平台有对应账号，并能免费调 AI 生成人物画像、一键导出 PDF。是入门 [[wiki/security/osint|OSINT]] 的首选工具。

> [!example] 能力
> - 输入：单个 username 或 email
> - 覆盖：600+ 平台（社交、论坛、交友等）
> - 输出：命中账号列表 + AI 人物画像 + PDF 报告
> - 开箱即用，**不需要 API Key**
> - 约 6300 GitHub Star（`p1ngul1n0/blackbird`）

定位是"快速出全貌"的第一棒——平台覆盖广但不做递归追踪。要顺着发现的马甲继续往下挖，接力 [[wiki/security/maigret|Maigret]]。两者在取证链里的分工见 [[wiki/security/osint-工具链工作流|OSINT 工具链工作流]]。

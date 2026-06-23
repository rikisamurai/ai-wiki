---
title: theHarvester
tags: [osint, recon]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

theHarvester 是查公司专用的 [[wiki/security/osint|OSINT]] 采集器：给一个域名，自动从谷歌、必应、LinkedIn、DNS 记录等 40+ 数据源里，把这家公司的员工邮箱、子域名、IP、URL 批量扒出来。

> [!example] 能力
> - 输入：单个域名
> - 数据源：40+（搜索引擎、LinkedIn、DNS 等）
> - 输出：员工邮箱列表（含邮箱命名规律，如 firstname.lastname@company.com）、子域名、IP、URL
> - 基础功能免费；部分数据源（谷歌、Bing 等）需 API Key
> - 约 16500 GitHub Star（`laramies/theHarvester`）

它是企业侧取证 / 攻击面审计的第一棒——采集面向公开的邮箱与子域名清单，再把结果交给 [[wiki/security/spiderfoot|SpiderFoot]] 深挖、交给 [[wiki/security/shodan|Shodan]] 查设备暴露。防御侧怎么用见 [[wiki/security/数字痕迹自查|数字痕迹自查]]。

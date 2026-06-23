---
title: SpiderFoot
tags: [osint, automation]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

SpiderFoot 是 [[wiki/security/osint|OSINT]] 里的"重炮"——手机号、邮箱、域名、IP 全吃，200+ 模块同时出动自动采集，能查数据泄露、暗网挂牌、子域名，并产出可视化关系图谱。

> [!example] 能力
> - 输入：手机号 / 邮箱 / 域名 / IP（几乎任意实体）
> - 模块：200+ 个数据源并行
> - 特色：数据泄露查询、暗网检索、子域名枚举、实体关系图谱
> - 开箱即用，**不需要 API Key**（部分模块可选接 Key 增强）
> - 约 18000 GitHub Star（`smicallef/spiderfoot`）

SpiderFoot 的角色是"关联深挖"——常作为取证链的最后一棒，把前面工具的产物（[[wiki/security/theharvester|theHarvester]] 采集的域名、[[wiki/security/shodan|Shodan]] 发现的 IP）喂进来做交叉关联。链路全貌见 [[wiki/security/osint-工具链工作流|OSINT 工具链工作流]]。

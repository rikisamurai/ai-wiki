---
title: Shodan
tags: [osint, attack-surface]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

Shodan 被称为"设备版谷歌"——它持续全网扫描并索引暴露在公网上的设备：摄像头、路由器、服务器、数据库、工业控制系统（ICS）。官方 `shodan-python` 库让你用代码自动化查询这个数据库。

> [!example] 能力
> - 索引对象：公网可达的设备与服务（端口、Banner、版本、地理位置）
> - 典型查询：暴露的数据库、后台管理界面、默认口令的 NAS/摄像头/打印机、ICS
> - 接入：注册免费账号拿 API Key，免费额度日常够用；`pip install shodan`
> - 约 2800 GitHub Star（`achillean/shodan-python`）

Shodan 是 IP / 设备维度取证的对口工具——把 [[wiki/security/theharvester|theHarvester]] 采到的 IP 段扔进去，就能看出目标把哪些服务直接开在公网，从而评估其安全水位。这正是 [[wiki/security/数字痕迹自查|攻击面自查]] 的核心手段之一，完整链路见 [[wiki/security/osint-工具链工作流|OSINT 工具链工作流]]。

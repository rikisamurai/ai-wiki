---
title: OSINT（开源情报）
tags: [osint, security, reconnaissance]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

OSINT（Open Source Intelligence，开源情报）指仅从**公开可获取的信息源**收集、关联、分析目标情报的方法论——不入侵、不接触目标系统，只把散落在互联网各处的公开痕迹拼成完整画像。

> [!note] 定义
> "开源"指 **open source intelligence**（公开来源情报），与开源软件无关。核心假设：一个人或一家公司在网上留下的公开痕迹，远比他们以为的多——用户名、邮箱、域名、IP、暴露在公网的设备，只要存在过就大概率能被检索回来。

OSINT 取证对象按**输入类型**分类，每类有对口工具：

- **用户名 / 邮箱** → [[wiki/security/blackbird|Blackbird]]（快速全貌）+ [[wiki/security/maigret|Maigret]]（递归深挖）
- **域名** → [[wiki/security/theharvester|theHarvester]]（邮箱/子域名批量采集）
- **IP / 设备** → [[wiki/security/shodan|Shodan]]（公网暴露面）
- **综合关联** → [[wiki/security/spiderfoot|SpiderFoot]]（200+ 模块自动编排）

它们如何串成一条取证链，见 [[wiki/security/osint-工具链工作流|OSINT 工具链工作流]]。

> [!warning] 合法与伦理边界
> OSINT 技术本身中立，但用途有红线。正当场景是**对自己或获得授权的目标**：自查数字痕迹（[[wiki/security/数字痕迹自查|数字痕迹自查]]）、企业资产暴露面审计、授权渗透测试、对公开商业信息的尽调。未经同意地追踪、定位、画像私人（俗称"开盒"）在多数司法辖区涉嫌侵犯隐私、违反个人信息保护法规，本页只讨论防御与授权用途。

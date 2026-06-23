---
title: OSINT 工具链工作流
tags: [osint, workflow]
date: 2026-06-23
sources:
  - "[[sources/clippings/网警同款开盒思路，查人查公司查设备，五个免费开源工具]]"
last-ingested: 2026-06-23
status: draft
---

[[wiki/security/osint|OSINT]] 取证不是单工具作战，而是**按输入类型路由 + 先快后深**的流水线：先用平台覆盖最广的工具出全貌，再用最深的工具顺着线索往下挖、交叉验证。

> [!example] 按输入类型路由
> - **用户名** → [[wiki/security/blackbird|Blackbird]]（快速全貌）→ [[wiki/security/maigret|Maigret]]（递归深挖）
> - **邮箱** → Blackbird（账号 + AI 画像）→ [[wiki/security/spiderfoot|SpiderFoot]]（泄露 + 暗网）
> - **域名** → [[wiki/security/theharvester|theHarvester]]（邮箱/子域名批量采集）→ SpiderFoot（深挖）
> - **IP** → [[wiki/security/shodan|Shodan]]（设备与服务暴露）→ SpiderFoot（关联情报）
> - **信息充足** → 全部上，交叉验证

> [!note] 唯一原则
> **先用最快的出全貌，再用最深的往下挖。** 这与 agent 检索里"广覆盖召回 → 精排深挖"的两段式思路同构，可对照 [[wiki/retrieval/rag/hybrid-retrieval|混合检索]]。

工作流的正当落地是防御侧——对自己或授权目标跑一遍，见 [[wiki/security/数字痕迹自查|数字痕迹自查]]。

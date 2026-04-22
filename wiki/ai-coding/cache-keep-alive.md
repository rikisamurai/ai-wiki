---
title: Cache Keep-Alive
tags: [cache-keep-alive, cost-optimization, claude-code]
date: 2026-04-22
sources:
  - "[[sources/inbox/搞懂缓存机制，从Gemma4到Claude Code省80%Token]]"
last-ingested: 2026-04-22
status: stable
---

# Cache Keep-Alive

> [!note] TL;DR
> [[prefix-cache|Prefix Cache]] 的 TTL 在**每次读取时刷新**——意味着只要在过期前匹配前缀发一次请求，缓存就能无限续命。这条机制衍生出一种省钱姿势：用脚本每 55 分钟（1 小时 TTL 内）往 Claude Code 发一句无关紧要的 ping，把缓存"拽住"，避免午饭/会议期间 ~20K 的系统提示词被冲。

## 原理

```
TTL 1 小时
    ├─ 0:00  发请求       → 写缓存（贵 25%）
    ├─ 0:30  发请求       → 命中（0.1×）→ TTL 重置回 1h
    ├─ 1:25  发请求       → 命中（0.1×）→ TTL 又重置 1h
    └─ ... 持续命中，永不过期
```

刷新机制是被动的——**没人请求**才会让 TTL 自然走完。所以"续命"本质就是"假装一直有人在工作"。

## 为什么这件事值得做

Pro/Max 用户的 TTL 默认 1 小时。常见冲缓存场景：

| 行为 | 是否冲缓存 |
|---|---|
| 午饭吃 1.5 小时 | ✅ 冲 |
| 开 1 个跨午饭的长会 | ✅ 冲 |
| 下午茶聊 30 分钟 | 不冲 |
| 上线一上午集中干活 | 不冲 |

冲一次缓存的代价 = ~20K tokens 全价 Prefill。每天冲 3-4 次，**一周净亏一份套餐额度**。

## 实操方案

> [!example] tmux / iTerm AppleScript 自动 ping
> 每 55 分钟往 Claude Code 终端自动发一条 prompt：
> 
> ```markdown
> 我断线了么？如果没断你只要简单说ok。
> ```
> 
> Claude 会回个 "ok"。这条请求消耗极小（输入几十 token + 输出 1 token），但**让整个 20K+ 的系统前缀重新生效**。

## 适用边界

> [!warning] 这是 Pro/Max 套餐的玩法
> - **API 计费用户**：每次 ping 也要花钱，没必要
> - **Free / 默认 5 分钟 TTL 用户**：每 4 分钟 ping 一次太频繁，节奏被打乱
> - **本来就高频对话的人**：自然 keep-alive，不用脚本

适合的画像：**Max 套餐 + 长会议/外出多 + 一天有几个完整工作时段**。

## 跟其他保护缓存动作的关系

Cache Keep-Alive 是 [[cache-失效陷阱|失效陷阱]] 防御的最后一公里——前面所有"别改 CLAUDE.md / 别加减 MCP / 别切模型"管的是**主动行为**导致的失效，而 keep-alive 管的是**被动等待**导致的失效。

| 失效成因 | 防御手段 |
|---|---|
| 改了静态前缀 | [[稳定前缀-动态后缀]] 设计法则 |
| 切了模型 | 工作日内单模型 |
| /compact 了历史 | 推迟到对话 >100K 再用 |
| **TTL 走完了** | **Cache Keep-Alive** |

## 关联

- 上层概念：[[prefix-cache]]——TTL 是 prefix cache 的内置属性
- 兄弟动作：[[cache-失效陷阱]] / [[稳定前缀-动态后缀]]
- 经济账：[[cache-命中率]]——keep-alive 是把命中率从被动"运气"变成主动"维持"

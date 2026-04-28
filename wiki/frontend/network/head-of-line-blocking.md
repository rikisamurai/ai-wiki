---
title: 队头阻塞（Head-of-Line Blocking）
tags: [networking, protocol, performance]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/HTTP3 入门指南]]"
last-ingested: 2026-04-22
status: draft
---

队头阻塞是指多路复用通道里，靠前的数据丢失或延迟会拖累后面所有数据的现象。它在 HTTP 协议演进里出现过两次：HTTP/1.1 Pipeline 的应用层队头阻塞，以及 HTTP/2 over TCP 的传输层队头阻塞。

> [!note] HTTP/1.1 应用层队头阻塞
> Pipeline 允许在一个 TCP 连接上连续发请求，但响应必须按发送顺序返回。前一个慢响应会卡住所有后续响应。这就是 Pipeline 几乎没在生产环境普及的根本原因。

> [!warning] HTTP/2 传输层队头阻塞
> [[wiki/frontend/network/http-3|HTTP/2]] 在应用层做了多路复用，但底层仍是 TCP。TCP 保证字节按序到达——一个包丢失，**所有流**都得等它重传完才能继续，多路复用反而在丢包场景下变成劣势。

> [!tip] HTTP/3 的解法
> [[wiki/frontend/network/quic|QUIC]] 把多路复用下沉到传输层。每条 Stream 有独立的丢包检测和重传机制，一条流丢包不影响其他流，应用层和传输层的多路复用第一次真正统一。

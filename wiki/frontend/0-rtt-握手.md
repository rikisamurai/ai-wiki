---
title: 0-RTT 握手
tags: [networking, performance, protocol]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/HTTP3 入门指南]]"
last-ingested: 2026-04-22
status: stable
---

0-RTT 是 [[wiki/frontend/quic|QUIC]] 在重连场景下的一种能力：客户端可以在握手的同时发送应用数据，无需等待任何往返。配合首次连接的 1-RTT 握手，[[wiki/frontend/http-3|HTTP/3]] 把传输建立延迟压到了协议物理下限。

> [!compare] 握手延迟对比
> | 场景 | TCP + TLS 1.3 | QUIC |
> | --- | --- | --- |
> | 首次连接 | 2-3 RTT（TCP 三次握手 + TLS 握手分层） | 1 RTT（握手与 TLS 合并） |
> | 重连同一服务器 | 1-2 RTT | 0 RTT（带数据握手） |

> [!tip] 0-RTT 的真实价值
> 移动端用户跨基站切换、跨洋请求等高延迟场景，握手往返本身就是首屏耗时的大头。0-RTT 把"协议建链"这一段从用户感知中抹掉，是 HTTP/3 对 [[wiki/frontend/connection-migration|连接迁移]] 之外的另一个移动端杀手锏。

> [!warning] 重放风险
> 0-RTT 数据可能被中间人捕获后重放。规范要求服务端只对**幂等**请求接受 0-RTT 数据，写操作仍需走完整握手。

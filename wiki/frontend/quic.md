---
title: QUIC
tags: [networking, protocol, transport]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/HTTP3 入门指南]]"
last-ingested: 2026-04-22
status: draft
---

QUIC（Quick UDP Internet Connections）是基于 UDP 的可靠传输协议，[[wiki/frontend/http-3|HTTP/3]] 的传输层基础。它在 UDP 之上自行实现了流控、拥塞控制、重传，并把 TLS 1.3 内嵌进握手，避免了 TCP+TLS 分层带来的多次往返。

> [!note] QUIC 的关键改进
> - **传输层多路复用**：原生支持多条独立 Stream，每条流有独立的丢包检测和重传，避免 [[wiki/frontend/head-of-line-blocking|TCP 队头阻塞]]
> - **快速握手**：QUIC 握手与 TLS 握手合并为 1 RTT，重连支持 [[wiki/frontend/0-rtt-握手|0-RTT]]
> - **强制加密**：没有明文模式，TLS 1.3 必选
> - **连接迁移**：通过 Connection ID 标识连接，不依赖 IP 四元组，[[wiki/frontend/connection-migration|网络切换无需重建]]

> [!warning] 中间设备兼容性
> 部分企业防火墙、NAT 设备会拦截或限速 UDP 流量，导致 QUIC 不可用。客户端通常会回退到 HTTP/2 over TCP。

**RFC 索引**：QUIC 协议本体见 RFC 9000，HTTP/3 映射见 RFC 9114，QPACK 头部压缩见 RFC 9204。

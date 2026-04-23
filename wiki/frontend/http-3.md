---
title: HTTP/3
tags: [networking, http, protocol]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/HTTP3 入门指南]]"
last-ingested: 2026-04-22
status: stable
---

HTTP/3 是基于 [[wiki/frontend/quic|QUIC]] 协议的下一代 HTTP 标准，把传输层从 TCP 换成 UDP，从根本上解决了 HTTP/2 的 [[wiki/frontend/head-of-line-blocking|队头阻塞]] 问题，同时带来更快的握手和 [[wiki/frontend/connection-migration|连接迁移]] 能力。

> [!compare] HTTP/2 vs HTTP/3
> | 维度 | HTTP/2 | HTTP/3 |
> | --- | --- | --- |
> | 传输层 | TCP | QUIC（基于 UDP） |
> | 握手延迟 | 2-3 RTT | 1 RTT 首次 / [[wiki/frontend/0-rtt-握手\|0-RTT]] 重连 |
> | 队头阻塞 | TCP 层存在 | 流级别独立，无阻塞 |
> | 连接迁移 | 不支持 | 支持，基于 Connection ID |
> | 头部压缩 | HPACK | QPACK（适配无序传输） |
> | 加密 | 可选 TLS | 强制内置 TLS 1.3 |

> [!example] 协议栈对比
> ```
> HTTP/2 协议栈          HTTP/3 协议栈
> ┌──────────┐          ┌──────────┐
> │  HTTP/2  │          │  HTTP/3  │
> ├──────────┤          ├──────────┤
> │   TLS    │          │   QUIC   │ ← 内置 TLS 1.3
> ├──────────┤          ├──────────┤
> │   TCP    │          │   UDP    │
> └──────────┘          └──────────┘
> ```

**浏览器与 CDN 支持**：Chrome 87+ / Firefox 88+ / Safari 14+ 默认启用；Cloudflare、Google Cloud CDN 默认开启，AWS CloudFront 需手动开启，Nginx 1.25.0+ 实验支持，Caddy 与 LiteSpeed 原生支持。

> [!tip] 检测方法
> 浏览器 DevTools → Network → Protocol 列显示 `h3` 即为 HTTP/3。命令行可用 `curl -I --http3 https://example.com`。

> [!info] Alt-Svc 升级机制
> 服务端通过 `Alt-Svc: h3=":443"; ma=86400` 响应头告知浏览器支持 HTTP/3。首次访问仍走 HTTP/2，后续请求才会升级到 HTTP/3。

---
title: HTTP/3 入门指南
tags:
  - networking
  - http
  - quic
  - protocol
date: 2026-03-13
---

# HTTP/3 入门指南

> [!abstract] 概览
> HTTP/3 是基于 ==QUIC 协议==的下一代 HTTP 标准，用 UDP 替代了 TCP，从根本上解决了 HTTP/2 的 TCP 层队头阻塞问题，同时带来更快的连接建立和连接迁移能力。

## HTTP 协议演进简史

### HTTP/1.0 → HTTP/1.1

- HTTP/1.0 每次请求都需要新建 TCP 连接，开销巨大
- HTTP/1.1 引入 **Keep-Alive**（连接复用）和 **Pipeline**（管道化请求）
- 但 Pipeline 实际很少使用，因为响应必须按序返回，仍存在队头阻塞

### HTTP/1.1 → HTTP/2

- **多路复用**（Multiplexing）：一个 TCP 连接上并行传输多个请求/响应
- **HPACK 头部压缩**：大幅减少重复 header 的传输开销
- **服务端推送**（Server Push）：服务器可主动推送资源
- **二进制分帧**：用二进制帧替代文本协议，解析更高效

### HTTP/2 的痛点

HTTP/2 虽然在应用层实现了多路复用，但底层仍然依赖 TCP：

> [!warning] TCP 层队头阻塞（Head-of-Line Blocking）
> TCP 保证字节按序到达。当一个 TCP 包丢失时，==所有流==都必须等待该包重传完成，即使丢失的数据只属于其中一个流。这意味着 HTTP/2 的多路复用优势在丢包场景下反而变成了劣势。

此外，TCP + TLS 的握手需要多次往返（RTT），在高延迟网络下连接建立很慢。

这些问题催生了 HTTP/3。

## HTTP/3 核心特性

### QUIC：基于 UDP 的传输协议

HTTP/3 不再使用 TCP，而是基于 **QUIC**（Quick UDP Internet Connections）协议。QUIC 在 UDP 之上实现了可靠传输、流控、拥塞控制等原本由 TCP 提供的功能，但做了关键改进：

```
HTTP/2 协议栈          HTTP/3 协议栈
┌──────────┐          ┌──────────┐
│  HTTP/2  │          │  HTTP/3  │
├──────────┤          ├──────────┤
│   TLS    │          │   QUIC   │ ← 内置 TLS 1.3
├──────────┤          ├──────────┤
│   TCP    │          │   UDP    │
├──────────┤          ├──────────┤
│    IP    │          │    IP    │
└──────────┘          └──────────┘
```

### 0-RTT / 1-RTT 握手

- **TCP + TLS 1.3**：需要 2-3 个 RTT 才能开始传输数据
- **QUIC 首次连接**：==1 RTT== 即可完成握手并开始传输（QUIC 握手与 TLS 握手合并）
- **QUIC 重连**：支持 ==0-RTT==，客户端可在握手的同时发送数据，极大降低延迟

> [!tip] 0-RTT 的意义
> 对于移动端用户、高延迟网络（如跨洋连接），0-RTT 可以显著提升首屏加载速度。

### 无队头阻塞的多路复用

QUIC 在传输层原生支持多条独立的流（Stream）：

- 每条流有独立的丢包检测和重传机制
- 一条流丢包==不会阻塞==其他流的数据传输
- 真正实现了应用层和传输层的多路复用统一

### 连接迁移

TCP 连接由四元组（源 IP、源端口、目标 IP、目标端口）标识，网络切换时连接必须重建。

QUIC 使用 **Connection ID** 标识连接：

- 从 Wi-Fi 切换到 4G 时，IP 地址变了，但 Connection ID 不变
- 连接==无缝迁移==，无需重新握手
- 对移动端体验提升尤为明显

### 内置 TLS 1.3

- QUIC 强制加密，==没有明文传输==的选项
- TLS 1.3 直接集成到 QUIC 握手中，减少了往返次数
- 相比 TCP + TLS 的分层设计，安全性更高且延迟更低

## HTTP/2 vs HTTP/3 对比

| 维度 | HTTP/2 | HTTP/3 |
| --- | --- | --- |
| **传输层** | TCP | QUIC（基于 UDP） |
| **握手延迟** | 2-3 RTT（TCP + TLS） | 1 RTT（首次）/ 0 RTT（重连） |
| **队头阻塞** | TCP 层存在 | 流级别独立，无队头阻塞 |
| **连接迁移** | 不支持，网络切换需重建连接 | 支持，基于 Connection ID |
| **头部压缩** | HPACK | QPACK（适配无序传输） |
| **加密** | 可选（TLS） | 强制（内置 TLS 1.3） |
| **中间设备兼容性** | 好（TCP 广泛支持） | 部分防火墙/NAT 可能阻止 UDP |

## 实践指南

### 浏览器支持现状

主流浏览器均已支持 HTTP/3：

- **Chrome**：自 87 版本起默认启用
- **Firefox**：自 88 版本起默认启用
- **Safari**：自 14 版本起支持（macOS Big Sur / iOS 14）
- **Edge**：基于 Chromium，同 Chrome

> [!info] 检测方法
> 打开浏览器开发者工具 → Network 面板 → 查看请求的 Protocol 列，显示 `h3` 即为 HTTP/3。

### 服务器 / CDN 支持

| 平台 | 支持情况 |
| --- | --- |
| **Cloudflare** | 默认启用 |
| **AWS CloudFront** | 支持，需手动开启 |
| **Google Cloud CDN** | 默认启用 |
| **Nginx** | 1.25.0+ 实验性支持（需编译 quic 模块） |
| **Caddy** | 原生支持 |
| **LiteSpeed** | 原生支持 |

### 如何检测网站是否使用 HTTP/3

1. **浏览器 DevTools**：Network 面板查看 Protocol 列
2. **curl 命令**：
   ```bash
   curl -I --http3 https://example.com
   ```
3. **在线工具**：访问 [http3check.net](https://http3check.net) 输入域名检测

### 简要开启指引（Nginx 示例）

确保 Nginx 版本 ≥ 1.25.0 且编译时启用了 QUIC 支持：

```nginx
server {
    # 同时监听 TCP (HTTP/2) 和 UDP (HTTP/3)
    listen 443 ssl;
    listen 443 quic;

    ssl_certificate     /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 告知浏览器支持 HTTP/3
    add_header Alt-Svc 'h3=":443"; ma=86400';
}
```

> [!tip] Alt-Svc 头
> 浏览器通过 `Alt-Svc` 响应头发现 HTTP/3 支持。首次访问仍会使用 HTTP/2，后续请求才会升级到 HTTP/3。

## 参考资料

- [RFC 9000 - QUIC: A UDP-Based Multiplexed and Secure Transport](https://www.rfc-editor.org/rfc/rfc9000)
- [RFC 9114 - HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [RFC 9204 - QPACK: Field Compression for HTTP/3](https://www.rfc-editor.org/rfc/rfc9204)
- [HTTP/3 explained (Daniel Stenberg)](https://http3-explained.haxx.se/)
- [Can I use: HTTP/3](https://caniuse.com/http3)

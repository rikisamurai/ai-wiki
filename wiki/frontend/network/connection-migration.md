---
title: 连接迁移（Connection Migration）
tags: [networking, mobile, protocol]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/HTTP3 入门指南]]"
last-ingested: 2026-04-22
status: stable
---

连接迁移指 [[wiki/frontend/network/quic|QUIC]] 通过 Connection ID 标识连接、不依赖 IP 四元组的能力——网络从 Wi-Fi 切到 4G、IP 地址变化时，连接无需重建即可继续使用。这是 [[wiki/frontend/network/http-3|HTTP/3]] 对移动端体验的关键升级之一。

> [!compare] TCP 与 QUIC 的连接标识
> | | TCP | QUIC |
> | --- | --- | --- |
> | 标识方式 | 四元组（源 IP、源端口、目标 IP、目标端口） | Connection ID（与 IP 解耦） |
> | 网络切换 | 必须重建连接，重新握手 | 连接 ID 不变，无缝迁移 |
> | 配合 [[wiki/frontend/network/0-rtt-握手\|0-RTT]] | 不可用 | 可在迁移后立即继续传输 |

> [!example] 典型场景
> 用户在地铁上看视频，列车出站后从地铁 Wi-Fi 切到 4G。TCP 连接会断开重连，视频缓冲跳一下；QUIC 连接保持活跃，体验无感。

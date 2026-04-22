---
title: MCP（Model Context Protocol）
tags: [claude, protocol, agent]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
last-ingested: 2026-04-22
status: draft
---

MCP（Model Context Protocol）是 Anthropic 推出的开放协议，让 LLM 客户端通过统一接口接入外部工具、数据源、服务。相当于 Agent 世界的"USB-C"——一次实现 server，所有支持 MCP 的客户端（Claude Code、[[wiki/obsidian/claudian|Claudian]]、Cursor、Zed 等）都能用。

> [!note] 三种传输
> | 传输 | 适用 | 部署方式 |
> | --- | --- | --- |
> | **stdio** | 本地工具，进程间 pipe | 客户端启动子进程 |
> | **SSE** | 远程长连接，服务端推送 | 长跑 HTTP 服务 |
> | **HTTP** | 简单请求/响应 | 普通 REST 端点 |

> [!example] 典型 MCP server
> - **filesystem**：读写指定目录
> - **github**：调 GitHub API（issue / PR / search）
> - **postgres**：执行 SQL 查询
> - **playwright**：浏览器自动化
> - **slack**：发消息、读频道

> [!compare] MCP vs 传统插件
> | 传统插件 | MCP |
> | --- | --- |
> | 每个客户端各自实现 | 一次实现，多客户端复用 |
> | 紧耦合宿主 API | 协议抽象，客户端无关 |
> | 工具描述写死 | server 自描述能力 |

> [!tip] 与 [[wiki/aigc/permission-modes|权限模式]] 配合
> MCP 工具调用同样会被 YOLO/Safe/Plan 拦截。把高风险的 MCP server（如 shell、数据库写）配 Safe，只读 server 配 YOLO，是一种实用的精细化授权。

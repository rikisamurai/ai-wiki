---
title: MCP（Model Context Protocol）
tags: [claude, protocol, agent]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/Claudian - Obsidian × Claude Code]]"
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 深度使用指南 - HiTw93]]"
  - "[[sources/posts/aigc/ai-coding/codex/Codex Best Practices]]"
last-ingested: 2026-04-23
status: stable
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

> [!warning] MCP 工具定义是上下文层的"隐形杀手"
> 一个典型 MCP Server 含 20-30 个工具定义，每个 ~200 tokens。**接 5 个 server，固定开销就达 ~25,000 tokens（占 200K 上下文的 12.5%）**。所有 MCP 工具 schema 在每次请求开头被全量发送——这部分被 [[wiki/ai-coding/prefix-cache|Prefix Cache]] 缓存，但**占用窗口的额度**。
>
> **优化策略**：
> - 用 `/mcp` 查看当前 server 的 token 成本，砍掉只是"装着以防万一"的 server
> - 大型 MCP server（如 GitHub 全工具集）考虑 **defer_loading**：先发 stub，模型按需通过 ToolSearch 加载完整 schema
> - 会话中途**不要**临时禁用某 MCP——工具集变了 = 缓存断（参见 [[wiki/ai-coding/cache-失效陷阱|cache 失效陷阱]]）

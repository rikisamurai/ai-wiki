---
title: agent-browser
tags: [agent-browser, browser-automation, ai-agent]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/browser-use/blog/OpenCLI：把任何网站变成 AI Agent 的命令行工具]]"
last-ingested: 2026-04-23
status: stub
---

agent-browser 是 Browser Agent 三大流派里的"中间路线"——不像 [[browser-use|Browser-Use]] 把原始截图喂给 LLM，也不像 [[opencli|OpenCLI]] 把每个网站封成专用命令，而是**在浏览器层做针对 Agent 的优化**：去除 UI 干扰、提供 Agent 友好的 selector、Token 高效的页面表征。

> [!compare] 三流派定位
> | 流派 | 代表 | LLM 输入抽象层级 |
> |---|---|---|
> | Browser-Use 派 | [[browser-use\|browser-use]] | 最原始（截图 + DOM） |
> | **专用 Agent 派** | **agent-browser** | **中等（精简 DOM + 浏览器原语）** |
> | CLI 派 | [[opencli\|OpenCLI]] | 最抽象（结构化命令） |
>
> 选型：通用 + 控制力 → agent-browser；通用 + 灵活 → Browser-Use；高频 + 确定 → OpenCLI。

> [!note] 待补充
> 本页为最小存根，后续 36/41 / 37/41 的横向评测会补全：浏览器原语 CLI 设计、Token 效率对比、与 Cursor / Codex 的集成路径。

**关联**：[[browser-use|Browser-Use]] / [[opencli|OpenCLI]] / [[cdp|CDP]] / [[cdp-能力边界|CDP 能力边界]]

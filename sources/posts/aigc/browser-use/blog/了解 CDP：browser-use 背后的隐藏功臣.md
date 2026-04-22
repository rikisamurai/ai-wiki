---
title: 了解 CDP：browser-use 背后的隐藏功臣
tags:
  - browser-use
  - cdp
  - ai-coding
date: 2026-03-23
---

# 了解 CDP：browser-use 背后的隐藏功臣

> [!info] 文章来源
> 原文：[了解 CDP：browser-use 背后的隐藏功臣](https://supercodepower.com/chrome-devtools-protocol/)

## 协议格式

CDP（Chrome DevTools Protocol）是 Chrome 浏览器对外暴露的控制接口，基于 **JSON-RPC 2.0** 定制，运行在 **WebSocket** 之上，采用 CS 架构：

```
Client ↔ CDP Protocol ↔ Chromium
```

所有消息均为 JSON 格式，包含 `id`、`method`、`params` 等字段。

Chrome Devtools Frontend 就是前端开发者天天按 F12 唤起的调试面板，而 Puppeteer 和 Playwright 是非常有名的浏览器自动化操作工具，如今的 agent browser tool（例如 [playwright-mcp](https://github.com/microsoft/playwright-mcp)，[browser-use](https://github.com/browser-use/browser-use) 和 [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)）也是基于它们构建的。可以说每个开发者都在使用 CDP，但因它的定位比较底层，大家常常又意识不到他的存在。


CDP 有自己的[官方文档站](https://chromedevtools.github.io/devtools-protocol/)和相关的 [Github 地址](https://github.com/ChromeDevTools/devtools-protocol)，秉承了 Google 开源项目的一贯风格，简洁，克制，就是没什么可读性。文档和项目都是根据源码变动自动生成的，所以只能用来做 API 的查询，这也导致如果没有相关的领域知识，直接阅读相关文档或 [deepwiki](https://deepwiki.com/ChromeDevTools/devtools-protocol) 是拿不到什么有建设性内容的。

## Domain 整体分类

CDP 将功能按 **Domain** 划分，分为两大类：

![[Pasted image 20260323212707.png]]


- **Browser Protocol**：Page、DOM、CSS、Network、Input、Target 等，控制浏览器行为
- **JavaScript Protocol**：Runtime、Debugger、HeapProfiler、Profiler 等，控制 JS 执行环境



## Domain 内部通信

每个 Domain 的使用遵循三步流程：

1. **enable**：激活 Domain，开始监听事件
2. **methods / events**：发送命令、接收推送事件
3. **disable**：关闭 Domain，停止监听

以 Chrome DevTools 的 Console 面板为例：打开面板时发送 `Console.enable`，面板内的日志输出对应 `Console.messageAdded` 事件，关闭面板时发送 `Console.disable`。

![[asset/cdp-domain.png]]



## Target：特殊的 Domain

Target 是一个较为抽象的概述，它指的是浏览器中的**可交互实体**：

- 我创建了一个**浏览器**，那么它本身就是一个 type 为「browser」的 Target
- 浏览器里有一个**标签页**，那么这个页面本身就是一个 type 为「page」的 Target
- 这个页面里要做一些耗时计算创建了一个 **Worker**，那么它就是一个 type 为「worker」的 Target


目前从 [chromium 源码](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/devtools_agent_host_impl.cc?ss=chromium&q=f:devtools%20-f:out%20%22::kTypeTab%5B%5D%22)上可以看出，Target 的 type 有以下几种：

- browser，browser_ui，webview
- tab，page，iframe
- worker，shared_worker，service_worker
- worklet，shared_storage_worklet，auction_worklet
- assistive_technology，other

从上面的 target type 可以看出，Target 整体是属于一个 scope 比较大的实体，基本上是以**进程/** **线程****作为隔离单位**分割的，每个 type 下可能包含多个 CDP domain，比如说 page 下就有 Runtime，Network，Storage，Log 等 domain，其他类型同理。



> [!tip] Session 机制
> 与普通 Domain 不同，Target 通过 **Session** 进行通信。每个 Target 对应一个独立的 Session，支持一对多连接——同一个 Target 可以被多个 Client 同时连接控制。

![[asset/cdp-session.png]]



## 编码建议

> [!warning] AI 工具在 CDP 领域表现一般
> CDP 文档复杂且细节多，当前 AI 编码工具对 CDP 的理解有限，容易生成错误代码。

推荐实践：

- **小步快跑，随时验证**：每完成一小步就在真实浏览器中验证，避免错误积累
- **学习 Puppeteer 源码**：Puppeteer 是对 CDP 的高质量封装，阅读其源码是理解 CDP 用法的最佳途径

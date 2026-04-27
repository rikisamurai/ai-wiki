---
title: Bun
tags: [frontend, runtime, ai-infra]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析]]"
last-ingested: 2026-04-22
status: draft
---

Bun（88.8k stars）是 Jarred Sumner 2021 年发起的 Node.js 全栈替代品，把 JS 运行时、打包工具、测试框架、包管理器合成一个单体。底层用 JavaScriptCore（不是 V8），Zig 写的，启动速度和执行性能大幅领先 Node.js。2025 年 12 月被 Anthropic 收购，价格未公开，承诺继续以 MIT 协议开源运营。跟同样定位"JS 运行时新形态"的 [[wiki/frontend/webcontainers|WebContainers]] 路线互补——bun 是 native 端的高性能基座，WebContainers 是浏览器内沙箱基座。

> [!note] 技术选型的反共识
> | 维度 | Node.js | Bun |
> | --- | --- | --- |
> | JS 引擎 | V8 | JavaScriptCore（Safari 用的） |
> | 实现语言 | C++ | Zig |
> | 包管理 | npm/yarn/pnpm（外挂） | 内置 bun install |
> | 打包/测试 | webpack/vitest（外挂） | 内置 |
> | 启动速度 | 慢 | 大幅领先 |

## 为什么 Anthropic 要收购 Bun

收购公告同一天，Anthropic 宣布 Claude Code 达到 $10 亿年化收入（5 月公开发布到 12 月只用了 6 个月）。CPO Mike Krieger 把 Bun 定位为"AI 驱动的软件工程的关键基础设施"。逻辑链：

1. Claude Code 的 native installer 早就基于 Bun 构建
2. 一个高性能、可嵌入的 JS 运行时，是构建 Agent、代码执行沙箱、工具调用环境的理想基座
3. 把核心依赖收进自家，避免上游技术决策被第三方左右

这是典型的 [[wiki/frontend/js-盈利模式分类|"技术资产 → AI 基础设施"]] 收购逻辑，不是为了 Bun 在 Web 运行时市场的份额。

## 跟 Deno 的命运对比

Deno 也是 Node.js 替代品（Ryan Dahl，Node 原作者主导），但走"安全 + URL 导入 + 内置 TypeScript"路线。结果是 Deno 始终撬不动 Node.js 的存量市场，最后转做 Deno Deploy（部署平台）。Bun 收益更多——在被 Anthropic 收购前，月下载量超过 700 万，Midjourney、Lovable 等公司都在生产环境用了。

> [!compare] JS 运行时三家
> | | Node.js | Deno | Bun |
> | --- | --- | --- | --- |
> | 治理 | OpenJS Foundation | Deno Land Inc | Anthropic（自 2025-12） |
> | 主要叙事 | 事实标准 | 安全 + TS | 性能 + 一体化 |
> | 商业化 | N/A | Deno Deploy | 已被收购 |

**启示**：JS 运行时市场的护城河不在技术优雅，而在 npm 包生态兼容性。Bun 通过深度兼容 Node.js API + npm 包，绕过了 Deno 早期"重新发明生态"的陷阱。但即便如此，单靠运行时仍然撬不动 Node.js，最终走向[[wiki/frontend/js-盈利模式分类|被收购]] 这种 JS 项目的常见退出路径——成为 AI 公司战略版图里不可或缺的一块。

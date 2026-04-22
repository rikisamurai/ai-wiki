---
title: Headless UI
tags: [frontend, ui-library, ai-friendly]
date: 2026-04-22
sources:
  - "[[sources/posts/frontend/JavaScript/Blog/JavaScript 市场分析]]"
last-ingested: 2026-04-22
status: draft
---

Headless UI 指**只提供逻辑、不绑定样式**的组件库范式。代表是 TanStack Table（27.9k stars，MIT 协议）、Radix UI Primitives、cmdk 等。这种范式天然适配 AI 代码生成时代——AI 写一个 styled wrapper 比配置一个商业 [[wiki/frontend/per-seat-licensing|按席位授权]] 组件库简单太多。

> [!note] 三类组件库范式
> | 范式 | 代表 | 提供 | 适合 |
> | --- | --- | --- | --- |
> | 完整 styled | Material UI、Ant Design | 逻辑 + 样式 + 主题 | 快速搭管理后台 |
> | Headless | TanStack Table、Radix Primitives | 仅逻辑/可访问性 | 自定义设计语言 |
> | Recipe | [[wiki/frontend/shadcn-ui\|shadcn/ui]] | 逻辑组合 + 可复制粘贴样式源码 | AI 生成 + 项目级定制 |

## 为什么 AI 时代是 Headless 的红利期

- **训练数据偏好**：MIT 协议、活跃度高的 headless 库在 LLM 训练数据里出现频率更高，生成时被默认选中
- **样式生成成本崩塌**：Tailwind CSS + AI 让"写样式"几乎零成本，headless 不再是"还得自己写 CSS"的负担
- **可访问性外包**：Radix Primitives 把 ARIA、键盘导航、焦点管理这些难做对的东西封装好了，AI 不用关心
- **替换成本低**：Headless 库换皮容易，企业不会被锁死，长期成本可控

**与商业组件库的此消彼长**：商业组件库（[[wiki/frontend/per-seat-licensing|AG Grid 一类]]）面临的不是增长放缓，而是 AI 代码生成把"配置一个商业组件"和"让 AI 写一个 headless 替代"的成本曲线翻了过来。Tailwind Labs 2026 年 1 月裁员 75% 是这个趋势的注脚之一——即使是 State of JS 2025 最受欢迎的 CSS 框架，也躲不过商业模式的天花板。

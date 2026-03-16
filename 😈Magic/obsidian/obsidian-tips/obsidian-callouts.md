---
title: Obsidian Callout 使用指南
tags:
  - obsidian
  - callout
  - markdown
date: 2026-03-16
---




# Obsidian Callout 使用指南

Callout 是 Obsidian 提供的高亮信息块，用于在笔记中突出显示重要内容。它基于 Markdown 引用语法扩展而来。

## 基本语法

使用 `> [!type]` 创建一个 Callout：

> [!note]
> 这是一个基本的 note callout。

````markdown
> [!note]
> 这是一个基本的 note callout。
````


You can insert a default `[!note]` callout using the `Insert callout` [command](https://help.obsidian.md/plugins/command-palette)

## 自定义标题

在类型后面添加文字即可自定义标题：

> [!tip] 小技巧
> 可以在类型后面直接写标题文字。

````markdown
> [!tip] 小技巧
> 可以在类型后面直接写标题文字。
````

如果只写标题不写内容，Callout 会只显示标题行：

````markdown
> [!info] 仅标题，无正文
````

## 可折叠 Callout

在类型后加 `-` 表示默认折叠，加 `+` 表示默认展开：

> [!faq]- 点击展开（默认折叠）
> 这段内容默认是隐藏的，点击标题可以展开。

> [!faq]+ 点击折叠（默认展开）
> 这段内容默认是可见的，但可以折叠。

````markdown
> [!faq]- 点击展开（默认折叠）
> 这段内容默认是隐藏的，点击标题可以展开。

> [!faq]+ 点击折叠（默认展开）
> 这段内容默认是可见的，但可以折叠。
````

## 嵌套 Callout

Callout 可以嵌套使用：

> [!question] 外层 Callout
> > [!note] 内层 Callout
> > 嵌套的内容写在这里。

````markdown
> [!question] 外层 Callout
> > [!note] 内层 Callout
> > 嵌套的内容写在这里。
````

## 内置类型

Obsidian 提供 13 种内置 Callout 类型，每种都有独特的颜色和图标：

| 类型 | 别名 | 颜色 / 图标 |
|------|------|------------|
| `note` | — | 🔵 蓝色 / 铅笔 |
| `abstract` | `summary`, `tldr` | 🟢 青色 / 剪贴板 |
| `info` | — | 🔵 蓝色 / 信息 |
| `todo` | — | 🔵 蓝色 / 复选框 |
| `tip` | `hint`, `important` | 🟦 青色 / 火焰 |
| `success` | `check`, `done` | 🟢 绿色 / 对勾 |
| `question` | `help`, `faq` | 🟡 黄色 / 问号 |
| `warning` | `caution`, `attention` | 🟠 橙色 / 警告 |
| `failure` | `fail`, `missing` | 🔴 红色 / ✕ |
| `danger` | `error` | 🔴 红色 / 闪电 |
| `bug` | — | 🔴 红色 / 虫子 |
| `example` | — | 🟣 紫色 / 列表 |
| `quote` | `cite` | ⚪ 灰色 / 引号 |

> [!tip] 别名用法
> 别名和原类型效果完全相同，比如 `> [!faq]` 等同于 `> [!question]`。

### 示例一览

> [!note]
> 用于一般性的备注信息。

> [!abstract]
> 用于摘要或 TL;DR，快速概括要点。

> [!info]
> 提供补充说明或背景信息。

> [!todo]
> 记录待办事项或行动清单。

> [!tip]
> 分享实用的小技巧或最佳实践。

> [!success]
> 表示操作成功或任务完成。

> [!question]
> 提出问题或标记需要进一步思考的内容。

> [!warning]
> 提醒注意潜在风险或需要谨慎处理的事项。

> [!failure]
> 标记失败的操作或已知的缺陷。

> [!danger]
> 强调严重错误或危险操作，务必注意！

> [!bug]
> 记录已发现的 Bug 或异常行为。

> [!example]
> 提供具体的使用示例或代码演示。

> [!quote]
> 引用他人的话语或经典语句。

## 自定义 Callout

可以通过 CSS 片段自定义新的 Callout 类型。在 Obsidian 设置中打开 **外观 → CSS 代码片段**，创建一个 `.css` 文件：

```css
.callout[data-callout="custom-type"] {
  --callout-color: 255, 0, 0;
  --callout-icon: lucide-alert-circle;
}
```

- `--callout-color`：RGB 颜色值（不带 `rgb()` 包裹）
- `--callout-icon`：使用 [Lucide](https://lucide.dev/) 图标名称

保存后即可在笔记中使用：

````markdown
> [!custom-type] 自定义 Callout
> 这是一个自定义类型的 callout。
````

## 参考

- [Obsidian 官方文档 - Callouts](https://help.obsidian.md/callouts)


![](https://twitter.com/obsdmd/status/1580548874246443010)
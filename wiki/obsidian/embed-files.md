---
title: 嵌入文件（Embed）
tags: [obsidian, linking, transclusion]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/linking-notes-and-files/🔗 内部链接（Internal Links）]]"
last-ingested: 2026-04-22
status: draft
---

嵌入是 [[wiki/obsidian/wikilink|Wikilink]] 的"实时投影"变体——链接前加 `!`，目标内容会在当前笔记里**渲染**而不是跳转。源文件改了，嵌入处自动同步。这是 Obsidian 实现 transclusion（文本透嵌）的核心机制。

> [!example] 不同目标类型
> ```markdown
> ![[文件名]]              # 嵌入整篇笔记
> ![[文件名#标题]]          # 嵌入某个 header 的章节
> ![[文件名#^id]]          # 嵌入某个块（详见 [[wiki/obsidian/block-reference|块引用]]）
> ![[图片.png]]            # 嵌入图片
> ![[音频.mp3]]            # 嵌入音频播放器
> ![[视频.mp4]]            # 嵌入视频播放器
> ![[PDF.pdf#page=5]]     # 嵌入 PDF 第 5 页
> ![[xxx.base#view-id]]   # 嵌入 [[wiki/obsidian/obsidian-bases|Bases]] 视图
> ```

> [!compare] 嵌入 vs 复制粘贴
> | | 嵌入 | 复制粘贴 |
> | --- | --- | --- |
> | 数据 | 一份原件，多处投影 | 多份独立副本 |
> | 维护 | 改源同步 | 每处都要改 |
> | Diff 可见性 | 源文件 diff 即可 | 多文件 diff 噪音大 |
> | 适用 | 跨笔记复用 | 一次性引用历史快照 |

> [!tip] 嵌入是 [[wiki/obsidian/moc-索引笔记|MOC]] 的引擎
> MOC 页面里的"主题速览"通常就是用嵌入拼出来的：每个子主题嵌一个块或一段笔记，主页面只负责编排顺序和加导言。配合 [[wiki/obsidian/dataview|Dataview]] 自动列表能做到 90% 的内容是动态的。

> [!warning] 嵌入循环
> 如果 A 嵌入 B，B 又嵌入 A，Obsidian 会检测并停止递归——但仍要避免，会让笔记结构难以追踪。

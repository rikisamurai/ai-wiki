---
title: JSON Canvas
tags: [obsidian, canvas, format]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
last-ingested: 2026-04-22
status: draft
---

JSON Canvas（jsoncanvas.org）是 Obsidian 推出的开放规范，把"无限画布"用纯 JSON 描述：节点（文本/文件/链接/分组）、边（带方向的连线）、坐标和样式。`.canvas` 文件能在 Obsidian 内可视化编辑，也能被任何工具按规范读写。

> [!note] 为什么是 JSON 不是私有格式
> Kepano 把 Canvas 设计成开放规范，意图很明显：让 Agent、第三方工具、未来的协作者都能用同一份格式。`.canvas` 本质是 JSON，diff 友好、Git 可读、LLM 可生成。

> [!example] 节点类型
> | 类型 | 用途 |
> | --- | --- |
> | text | 自由文本块 |
> | file | 嵌入 vault 内笔记 |
> | link | 嵌入外部 URL |
> | group | 把多个节点框成一组 |

> [!compare] JSON Canvas vs Excalidraw
> | | JSON Canvas | Excalidraw |
> | --- | --- | --- |
> | 定位 | 结构化思维板（节点 + 边） | 自由手绘 / 图表 |
> | 数据 | 节点是笔记/文本/链接 | 形状是几何图元 |
> | 适合 | 知识地图、流程梳理 | 草图、白板、流程图 |

> [!tip] 配合 [[wiki/obsidian/obsidian-skills|json-canvas skill]]
> 让 LLM 直接生成 `.canvas` 文件——比如把一段长文档的章节关系画成画布，或者把一个想法拆成节点放到画布上等用户拖动整理。这是从"线性笔记"扩展到"二维画布"的思维工具。

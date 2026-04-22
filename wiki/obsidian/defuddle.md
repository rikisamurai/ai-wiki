---
title: Defuddle
tags: [obsidian, scraping, markdown]
date: 2026-04-22
sources:
  - "[[sources/posts/obsidian/obsidian/obsidian-claude/skills]]"
last-ingested: 2026-04-22
status: draft
---

Defuddle 是 Kepano 维护的命令行工具（github.com/kepano/defuddle-cli），用来把网页清洗成干净 Markdown——剥掉导航、广告、cookie 横幅、相关推荐等"网页噪音"，只留正文。常被 Agent 用来抓网页内容时省 token。

> [!compare] Defuddle vs [[wiki/obsidian/obsidian-web-clipper|Web Clipper]]
> | | Defuddle | Web Clipper |
> | --- | --- | --- |
> | 形态 | CLI / npm 包 | 浏览器扩展 |
> | 触发 | Agent / 脚本调用 | 用户手动点击 |
> | 用途 | 程序化批量抓取 | 即兴剪藏入 [[wiki/obsidian/inbox-工作流\|inbox]] |
> | 输出 | 干净 Markdown 字符串 | 完整 frontmatter + 模板化笔记 |

> [!example] Agent 用法
> [[wiki/obsidian/obsidian-skills|defuddle skill]] 让 Claude Code 在收到"读这个网页"指令时自动调 Defuddle 而不是直接 fetch HTML——LLM 看到的是干净正文，省下 70%+ 的 token，提取也更准。

> [!tip] 与 [[wiki/aigc/agent-skills|Agent Skills]] 的设计哲学一致
> Defuddle 本身只是个 CLI，但它通过 obsidian-skills 包装成 skill 后，被任何 Agent 客户端都能"自动调"。这是"工具 + skill 描述"的标准化打包模式——比直接让 Agent 学会调命令行更可靠。

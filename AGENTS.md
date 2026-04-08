# Repository Guidelines

## 项目定位

这是一个以 Obsidian 为核心的中文知识库，主要沉淀 AI Coding、AIGC、Obsidian 和前端相关内容。仓库重点是文档的可读性、可链接性和可持续整理，不是应用构建或发布。

## 目录结构

- `00_inbox/`：收件箱，存放待整理的剪藏、草稿和临时素材。
- `😈Magic/`：方法类、工具类、Obsidian 使用技巧。
- `🚀AIGC/`：AI Coding、browser-use、RAG 等专题内容。
- `🌇FrontEnd/`：前端相关笔记与文章。
- `asset/` 子目录：存放与当前专题或文章相关的图片资源。
- `.agents/skills/`：与代理工作流相关的技能说明和少量代码。

新增文档时，优先放到最贴近主题的目录；不要把已完成文章长期留在 `00_inbox/`。

## 文档编写规范

- 笔记内容尽量使用**中文**撰写，但英文专有名词不要使用中文（比如写“Agent”，而不是写“代理”)
- 使用 Obsidian Flavored Markdown（wikilinks、callouts、frontmatter 等）
- 内部链接使用 `[[wikilink]]`，外部链接使用标准 Markdown 语法
- 新建笔记必须包含 YAML frontmatter，格式参考：
  ```yaml
  ---
  title: 笔记标题
  tags:
    - tag1
    - tag2
  date: YYYY-MM-DD
  ---
  ```
- 新增的 tag 必须符合 kebab-case, 且一篇文章最多 3 个 tags
- 善用 Obsidian callouts（`> [!type]`）组织内容


## 提交规范

提交信息沿用现有风格，优先使用 `docs:`、`feat:`、`chore:` 开头，主题简短明确，例如 `docs: 新增 browser-use 对比文章`。PR 或合并说明应写清楚改动目录、文档目的，以及是否涉及图片、链接修复或结构调整。


## 与用户沟通

- 使用中文交流
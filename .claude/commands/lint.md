---
description: 扫 wiki/ 输出健康报告，不自动修
---

# /lint

扫 `wiki/` 全部 markdown 文件，**只报告，不自动改**。

## 你必须输出的检查项

### 1. 孤儿页面
- 定义：在 `wiki/` 下存在，但没有任何其他 wiki 页面 wikilink 到它，且不在 `index.md` 里
- 报告：列出文件路径，建议候选动作（移到 `wiki/_orphans/` 或在 index.md 补链）

### 2. 出链不足
- 定义：wiki 页面正文中 wikilink 数 < 2
- 报告：列出文件路径 + 当前 wikilink 数

### 3. 过时页面
- 定义：frontmatter `last-ingested` 早于 90 天前（用 `date -v-90d +%Y-%m-%d` 拿基准）
- 报告：列出文件路径 + last-ingested 日期

### 4. 概念重复
- 定义：标题或 H1 在多个文件高度相似（启发式：包含相同 ≥4 字关键词）
- 报告：列出候选合并组

### 5. 断链
- 定义：`index.md` 或 wiki 页面里的 wikilink 指向不存在的文件
- 报告：源文件 + 断链目标

### 6. status 异常
- frontmatter 缺 status，或 status 不在 {draft, stable, stale} 内

## 输出格式

把上面 6 类各自一节，用 markdown 输出到对话。每节末尾给"建议下一步"（一条 prompt 用户复制就能继续）。

## 退出条件

- 全部 6 类检查跑完
- 报告里至少包含每类的"零项"或"具体清单"
- append 到 log.md：`## [...] lint | weekly check` + 简要数字汇总

## 禁止

- 不自动修任何文件（除了 log.md）
- 不删任何 wiki 页面（即便是孤儿，移动也要等用户确认）

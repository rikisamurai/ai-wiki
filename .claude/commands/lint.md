---
description: 扫 wiki/ 输出健康报告，不自动修
---

# /lint

扫 `wiki/` 全部 markdown 文件，**默认只报告**；唯一例外是 §3 status 流转——按规则自动改 frontmatter，跑完汇报变更。

## 你必须输出的检查项

### 1. 孤儿页面
- 定义：在 `wiki/` 下存在，但没有任何其他 wiki 页面 wikilink 到它，且不在 `index.md` 里
- 报告：列出文件路径，建议候选动作（移到 `wiki/_orphans/` 或在 index.md 补链）

### 2. 出链不足
- 定义：wiki 页面正文中 wikilink 数 < 2
- 报告：列出文件路径 + 当前 wikilink 数

### 3. status 流转

status 三态是 `draft → stable → stale`。**lint 直接改 frontmatter，不需要用户确认**，跑完后报告"改了哪些"。

**3a. 自动升级 draft → stable**
- 触发：`status: draft` 且被 ≥3 个 wiki 页 wikilink 引用（高入度 = 已被网络承认为枢纽概念）
- 动作：把 frontmatter `status: draft` 改成 `status: stable`
- 报告：变更清单（文件路径 + 入度）

**3b. 自动降级到 stale**
- 触发：`last-ingested` 早于 180 天前（`date -v-180d +%Y-%m-%d`）且 `status != stale`
- 动作：把 frontmatter status 改成 `status: stale`
- 报告：变更清单（文件路径 + last-ingested 日期）

**3c. status 字段异常**（仅报告，不自动修）
- frontmatter 缺 status，或 status 不在 {draft, stable, stale} 内
- 报告：文件路径 + 当前异常值；由用户决定改成什么

### 4. 概念重复
- 定义：标题或 H1 在多个文件高度相似（启发式：包含相同 ≥4 字关键词）
- 报告：列出候选合并组

### 5. 断链
- 定义：`index.md` 或 wiki 页面里的 wikilink 指向不存在的文件
- 报告：源文件 + 断链目标

## 输出格式

把上面 5 类各自一节，用 markdown 输出到对话。每节末尾给"建议下一步"（一条 prompt 用户复制就能继续）。

## 退出条件

- 全部 5 类检查跑完
- 报告里至少包含每类的"零项"或"具体清单"
- append 到 log.md：`## [...] lint | weekly check` + 简要数字汇总

## 禁止

- 不自动修任何文件，**例外**：`log.md` 和被 §3a / §3b 触发的 `status` 字段
- 不删任何 wiki 页面（即便是孤儿，移动也要等用户确认）
- 不动 §3c 报告的异常 status（不知道改成啥，留给用户）

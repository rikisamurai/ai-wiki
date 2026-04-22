---
description: 把 sources/ 下一份原料抽取成 wiki/ 多个互链页面
argument-hint: <source-path>
---

# /ingest

输入：`$ARGUMENTS`（sources/ 下的某个文件路径或 wikilink）

## 你必须严格遵守的步骤

1. **读 source**：用 Read 工具读取 `$ARGUMENTS` 指向的文件全文。如果 source 是 wikilink 形式（`[[xxx]]`），先在 `sources/` 下定位实际路径。

2. **识别概念**：识别其中 5-15 个值得独立成页的概念、工具、事件、人物。每个概念应满足：
   - 能被一句话定义
   - 大概率会在未来其他 source 中再次出现
   - 不是 source 的一次性论点

3. **检查重复**：对每个概念，先用 Grep 在 `wiki/` 全域搜近义页面（含别名、英文/中文对照）。
   - 已有 → 走"追加补充"分支
   - 没有 → 走"新建"分支

4. **写页面**（每页都满足）：
   - 路径：`wiki/<domain>/<kebab-case-标题>.md`，domain 在 ai-coding / aigc / frontend / obsidian 里选
   - frontmatter 含：title / tags（≤3 kebab-case）/ date / sources（**全路径 wikilink 列表**，形如 `"[[sources/clippings/xxx]]"`）/ last-ingested / status: draft
   - 首段是 TL;DR（1-3 句，不带 "TL;DR:" 前缀）
   - 至少 2 个 wikilink 出链到其他 wiki 页面
   - 用 Obsidian callouts 区分定义 / 示例 / 对比

5. **回填 frontmatter**：在每个被影响的 wiki 页面的 `sources:` 列表里加上这条 source（用全路径 wikilink，如 `"[[sources/clippings/xxx]]"`，便于 /lint 反查）。

6. **更新 index.md**：在对应 `## <domain>` 标题下追加 wikilink 行（按字母序插入，不重复）。

7. **append 到 log.md**：

   ```
   ## [YYYY-MM-DD HH:MM] ingest | <source 标题>
   - 新建：[[wiki/.../page-a]]、[[wiki/.../page-b]]
   - 更新：[[wiki/.../page-c]]
   - source: $ARGUMENTS
   ```

## 退出条件

完成时必须满足：
- 所有新建/更新的 wiki 页面都有 ≥2 个 wikilink 出链
- 这条 source 至少在 1 个 wiki 页面的 frontmatter `sources:` 里出现
- index.md 和 log.md 都已更新
- **不修改 source 本身**

## 禁止

- 不修改 `sources/` 下任何文件
- 不写超过 15 个概念页（控制单次 ingest 规模）
- 不在 wiki 页面里放原 source 的大段引用（精华提炼，不是搬运）

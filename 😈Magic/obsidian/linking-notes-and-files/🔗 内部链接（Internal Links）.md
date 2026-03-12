# Obsidian 内部链接（Internal Links）

> 官方文档：[Internal links](https://help.obsidian.md/links)


---

通过内部链接将笔记相互关联，可以构建出一个知识网络。Obsidian 支持在重命名文件时自动更新所有内部链接（可在 **设置 → 文件与链接 → 自动更新内部链接** 中控制）。

---

## 支持的链接格式

Obsidian 支持两种链接格式：


| 格式               | 示例                                         |
| ---------------- | ------------------------------------------ |
| **Wikilink**（默认） | `[[三大运动定律]]` 或 `[[三大运动定律.md]]`             |
| **Markdown**     | `[三大运动定律](三大运动定律)` 或 `[三大运动定律](三大运动定律.md)` |

两种格式效果相同。Obsidian 默认使用更简洁的 Wikilink 格式。如果需要与其他工具互通，可在 **设置 → 文件与链接** 中关闭 **使用 \[\[Wikilinks\]\]**。

> [!note] Markdown 格式注意事项
> 使用 Markdown 格式时需要对链接目标进行 URL 编码，例如空格需写为 `%20`。

> [!warning] 无效字符
> 链接中不应包含以下字符：`# | ^ : %% [[ ]]`

---

## 链接到文件

在编辑模式下创建链接的方式：

1. 输入 `[[`，然后从弹出列表中选择目标文件
2. 先选中文本，再输入 `[[`
3. 打开命令面板，选择「添加内部链接」

链接 Markdown 以外的文件类型时需要包含扩展名，例如 `[[Figure 1.png]]`。

> [!tip]
> 在内部链接前加 `!` 可以嵌入链接内容，例如 `![[文件名]]`。详见 [[Embed Files]]。

---


## 链接到标题

### 链接到当前笔记中的标题

输入 `[[#` 即可看到当前笔记中所有标题的列表。

```markdown
[[#预览链接文件]]
```



### 链接到其他笔记中的标题

在链接目标后加 `#` 和标题文本：

```markdown
[[About Obsidian#Links are first-class citizens]]
```

### 链接到子标题

可以使用多个 `#` 来定位嵌套标题：

```markdown
[[帮助与支持#问题与建议#报告 Bug]]
```

### 跨库搜索标题

使用 `[[##` 语法可以在整个库中搜索标题：

```markdown
[[## team]]    <!-- 搜索所有包含 "team" 的标题 -->
```

---

## 链接到块

"块"是笔记中的一个内容单元，可以是段落、引用、列表项等。

### 基本语法

在链接目标后加 `#^` 和块标识符：

```markdown
[[2023-01-01#^37066d]]
```

输入 `^` 时 Obsidian 会弹出建议列表，无需手动查找标识符。

### 为不同类型的块添加 ID

**普通段落** — 在行末加空格、`^` 和标识符：

```markdown
这是一段需要被引用的文字。 ^my-block-id
```

**结构化块**（列表、引用、callout、表格）— 标识符需另起一行，前后各留一个空行：

```markdown
> 这是一段引用内容。

^block-id-here

后续段落。
```

**列表中的特定行** — 标识符可直接放在列表项上：

```markdown
- 第一项 ^item-1
- 第二项
```


### 跨库搜索块

使用 `[[^^block]]` 语法可以搜索整个库中的块。


[[block-link-demo#^37066d]]

[[block-link-demo#^37066f]]

[[block-link-demo#^063f9a]]

[[block-link-demo#^37006f]]


### 自定义块 ID

块 ID 只能包含**拉丁字母、数字和连字符**（`-`）：

```markdown
"你不会升到目标的高度，只会落到系统的水平。" — James Clear ^quote-of-the-day
```

然后通过 `[[2023-01-01#^quote-of-the-day]]` 引用。

> [!warning] 互操作性
> 块引用是 Obsidian 特有功能，不属于标准 Markdown 规范。包含块引用的链接在 Obsidian 之外无法使用。

---

## 修改链接显示文本

默认情况下链接按原样显示。可以自定义显示文本：

**Wikilink 格式** — 用竖线 `|` 分隔：

```markdown
[[示例文件|自定义名称]]
[[示例文件#详情|章节名称]]
```

[[🧱Cross Walls]]

**Markdown 格式** — 用标准语法：

```markdown
[自定义名称](示例文件.md)
[章节名称](示例文件.md#详情)
```

> [!tip] 显示文本 vs 别名
> - **显示文本**：在特定位置自定义链接外观
> - **别名（Alias）**：在 YAML frontmatter 中设置可复用的替代名称，全库通用

---

## 预览链接文件

需先启用 **Page preview** 插件。

- **阅读模式**：悬停在链接上即可预览
- **编辑模式**：按住 `Ctrl`（macOS 为 `Cmd`）并悬停在链接上预览

---

## 相关文档

- [Internal links — Obsidian Help](https://help.obsidian.md/links)
- [Embed files — Obsidian Help](https://help.obsidian.md/Linking+notes+and+files/Embed+files)
- [Aliases — Obsidian Help](https://help.obsidian.md/Linking+notes+and+files/Aliases)

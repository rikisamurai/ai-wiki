# Obsidian 块引用使用案例



> 官方文档：[Linking to blocks](https://help.obsidian.md/Linking+notes+and+files/Internal+links#Link+to+a+block+in+a+note)

---

## 什么是块引用？

Obsidian 中"块"（Block）是任意一段独立内容——一个段落、一个列表项、一个标题、一张表格等。块引用允许你精确链接或嵌入某个块，而不是整篇笔记。

---

## 基础用法

### 1. 创建块 ID

在段落末尾手动添加 `^自定义id`：

```markdown
这是我想被引用的段落内容。 ^my-block-id
```

也可以在输入 `[[^^` 后，Obsidian 会弹出搜索框让你选择已有内容，自动生成随机 ID（如 `^abc123`）。

### 2. 链接到块（跳转）

```markdown
[[文件名#^my-block-id]]
[[文件名#^my-block-id|自定义显示文字]]
```

点击后会直接跳转到目标文件的对应块位置。

### 3. 嵌入块（transclusion）

```markdown
![[文件名#^my-block-id]]
```

目标块的内容会直接渲染显示在当前笔记中，源文件更新后此处自动同步。

---

## 典型使用场景

### 场景一：每日笔记引用重要结论

你在 `2026-03-12 日记` 中记录了一个重要决策：

```markdown
今天和团队讨论后，决定使用 PostgreSQL 而非 MongoDB。 ^db-decision
```

之后在项目笔记中直接嵌入，无需复制粘贴：

```markdown
## 技术选型依据

![[2026-03-12 日记#^db-decision]]
```

---

### 场景二：读书笔记中引用金句

在 `《原则》读书笔记` 中标记一段话：

```markdown
痛苦 + 反思 = 进步。 ^dalio-pain
```

在你的「个人成长 MOC」中嵌入这句话，形成跨笔记的知识联系：

```markdown
![[《原则》读书笔记#^dalio-pain]]
```

---

### 场景三：避免重复维护同一信息

在 `技术规范.md` 里定义接口版本说明：

```markdown
当前 API 版本为 v3，所有请求需携带 `X-API-Version: 3` header。 ^api-version
```

在多个相关笔记中嵌入这一块，只需维护一处：

```markdown
![[技术规范#^api-version]]
```

---

### 场景四：MOC（内容地图）聚合碎片知识

在你的 `AI 学习 MOC` 中，从不同笔记中嵌入关键段落，形成综合视图：

```markdown
## 核心概念速览

### Transformer 原理
![[深度学习笔记#^transformer-core]]

### Prompt 工程要点
![[Prompt 技巧#^prompt-tips]]

### RAG 架构说明
![[RAG 实践#^rag-overview]]
```

---

### 场景五：任务追踪跨文件引用

在 `项目计划.md` 中创建任务块：

```markdown
- [ ] 完成用户认证模块重构 ^task-auth
```

在每日笔记中嵌入，直接在日记里勾选，源文件状态同步更新：

```markdown
![[项目计划#^task-auth]]
```

---

## 注意事项

- 块 ID 只能包含字母、数字和连字符（`-`），不支持中文或空格
- 嵌入的块内容是实时同步的，修改源文件后嵌入处自动更新
- 块引用在 Obsidian 图谱中会显示为笔记间的连接关系
- 若源文件被删除，块引用链接会变为断链

---

## 相关文档

- [Internal links — Obsidian Help](https://help.obsidian.md/Linking+notes+and+files/Internal+links)
- [Embed files — Obsidian Help](https://help.obsidian.md/Linking+notes+and+files/Embed+files)



This is a paragraph  ^2026-03-12


[[#^2026-03-12]]


[[^]]
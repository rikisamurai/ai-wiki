


# Obsidian 使用技巧总结

## 📝 双向链接与知识图谱

### 基础链接
- `[[文件名]]` - 创建内部链接
- `[[文件名|显示文本]]` - 创建带自定义显示文本的链接
- `[[文件名#标题]]` - 链接到文件中的特定标题
- `[[文件名#^块引用]]` - 链接到特定段落块

### 块引用
- 在段落末尾添加 `^block-id` 创建块ID
- 使用 `![[文件名#^block-id]]` 嵌入特定块
- 快捷键：输入 `[[^^` 然后选择要引用的块

### 反向链接
- 侧边栏的"反向链接"面板显示所有指向当前笔记的链接
- 未链接提及：显示提到当前笔记名称但未创建链接的位置

### 知识图谱
- `Ctrl/Cmd + G` - 打开全局知识图谱
- 右键点击节点可以快速导航
- 使用过滤器和分组功能优化图谱显示
- 本地图谱：显示当前笔记的关联网络

## ⌨️ 快捷键与命令

### 核心快捷键
- `Ctrl/Cmd + P` - 命令面板（最重要的快捷键）
- `Ctrl/Cmd + O` - 快速切换文件
- `Ctrl/Cmd + N` - 新建笔记
- `Ctrl/Cmd + E` - 切换编辑/预览模式
- `Ctrl/Cmd + ,` - 打开设置
- `Ctrl/Cmd + F` - 当前文件内搜索
- `Ctrl/Cmd + Shift + F` - 全局搜索

### 编辑快捷键
- `Ctrl/Cmd + B` - 加粗
- `Ctrl/Cmd + I` - 斜体
- `Ctrl/Cmd + K` - 插入链接
- `Ctrl/Cmd + [` / `]` - 减少/增加缩进
- `Ctrl/Cmd + D` - 删除当前行
- `Alt + ↑/↓` - 上下移动行

### 导航快捷键
- `Ctrl/Cmd + Click` - 在新标签页打开链接
- `Ctrl/Cmd + Alt + ←/→` - 前进/后退导航历史
- `Ctrl/Cmd + Shift + E` - 打开文件管理器
- `Ctrl/Cmd + Shift + L` - 打开图谱视图

### 自定义快捷键
- 设置 → 快捷键，可以为任何命令自定义快捷键
- 搜索功能名称快速找到对应命令
- 建议为常用插件功能设置快捷键

## 📋 模板与日记

### 模板功能
1. **设置模板文件夹**
   - 设置 → 核心插件 → 模板
   - 指定模板文件夹位置（如 `Templates/`）

2. **创建模板**
   ```markdown
   ---
   title: {{title}}
   date: {{date}}
   tags: []
   ---

   # {{title}}

   ## 概述

   ## 详细内容

   ## 相关链接
   ```

3. **模板变量**
   - `{{title}}` - 笔记标题
   - `{{date}}` - 当前日期
   - `{{time}}` - 当前时间

4. **使用模板**
   - `Ctrl/Cmd + P` → 搜索"插入模板"
   - 或设置快捷键快速调用

### 日记功能
1. **启用日记**
   - 设置 → 核心插件 → 日记
   - 配置日记存储位置和日期格式

2. **日记模板**
   ```markdown
   # {{date:YYYY-MM-DD dddd}}

   ## 📌 今日计划
   - [ ]

   ## 📝 笔记

   ## 🎯 完成事项
   - [x]

   ## 💭 反思总结
   ```

3. **快速打开**
   - `Ctrl/Cmd + P` → "打开今天的日记"
   - 设置快捷键一键打开

### Templater 插件（高级）
- 支持JavaScript表达式
- 动态内容生成
- 更强大的变量系统
- 条件逻辑和循环

## 🔌 常用插件推荐

### 效率提升类
1. **Templater** - 高级模板系统
2. **Quick Switcher++** - 增强的文件切换器
3. **Commander** - 自定义界面按钮和菜单
4. **Hotkeys++** - 额外的快捷键功能
5. **QuickAdd** - 快速捕获和宏命令

### 编辑增强类
1. **Advanced Tables** - 表格编辑增强
2. **Editor Syntax Highlight** - 代码高亮
3. **Paste URL into Selection** - 智能粘贴链接
4. **Footnote Shortcut** - 脚注快速插入
5. **Multi-Column Markdown** - 多列布局

### 知识管理类
1. **Dataview** - 数据库查询和动态列表
2. **Excalidraw** - 手绘图表和思维导图
3. **Canvas** - 可视化画布（核心插件）
4. **Tag Wrangler** - 标签管理
5. **Folder Note** - 文件夹笔记

### 外观美化类
1. **Minimal Theme Settings** - 主题自定义
2. **Style Settings** - 样式调整
3. **Icon Folder** - 文件夹图标
4. **Iconize** - 文件图标美化
5. **Banners** - 笔记横幅图片

### 发布与同步类
1. **Obsidian Git** - Git版本控制
2. **Remotely Save** - 云端同步（S3/WebDAV等）
3. **Digital Garden** - 发布笔记到网页
4. **Obsidian Publish** - 官方发布服务（付费）

### 任务管理类
1. **Tasks** - 高级任务管理
2. **Kanban** - 看板视图
3. **Calendar** - 日历视图
4. **Tracker** - 习惯追踪

## 📐 Markdown 高级语法

### 基础语法
```markdown
# 一级标题
## 二级标题
### 三级标题

**粗体** 或 __粗体__
*斜体* 或 _斜体_
~~删除线~~
==高亮==

- 无序列表
- 项目2
  - 子项目

1. 有序列表
2. 项目2

- [ ] 待办事项
- [x] 已完成事项

> 引用文本
>> 嵌套引用

`行内代码`

​```语言
代码块
​```

[链接文本](URL)
![图片描述](图片路径)
```

### Obsidian 扩展语法

#### Callouts（提示框）
```markdown
> [!note] 笔记
> 这是笔记内容

> [!tip] 提示
> 这是提示内容

> [!warning] 警告
> 这是警告内容

> [!danger] 危险
> 这是危险警告

> [!info] 信息
> 这是信息内容

> [!question] 问题
> 这是问题内容

> [!todo] 待办
> 这是待办事项

> [!example] 示例
> 这是示例内容

> [!quote] 引用
> 这是引用内容
```

可折叠的 Callout：
```markdown
> [!note]- 点击展开
> 折叠的内容

> [!tip]+ 默认展开
> 可以折叠的内容
```

#### 嵌入内容
```markdown
![[文件名]] - 嵌入整个笔记
![[文件名#标题]] - 嵌入特定章节
![[图片.png]] - 嵌入图片
![[音频.mp3]] - 嵌入音频
![[视频.mp4]] - 嵌入视频
![[PDF.pdf#page=5]] - 嵌入PDF特定页
```

#### 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 内容 | 内容 | 内容 |
| 内容 | 内容 | 内容 |

左对齐 | 居中 | 右对齐
:--- | :---: | ---:
内容 | 内容 | 内容
```

#### 数学公式（MathJax）
```markdown
行内公式：$E = mc^2$

独立公式：
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

#### Mermaid 图表
```markdown
​```mermaid
graph TD
    A[开始] --> B{判断}
    B -->|是| C[执行]
    B -->|否| D[结束]
    C --> D
​```

​```mermaid
sequenceDiagram
    用户->>服务器: 发送请求
    服务器->>数据库: 查询数据
    数据库->>服务器: 返回结果
    服务器->>用户: 响应
​```
```

### 前置元数据（YAML Frontmatter）
```markdown
---
title: 笔记标题
date: 2024-01-01
tags: [标签1, 标签2]
author: 作者名
status: 进行中
priority: 高
---
```

## 🚀 工作流优化建议

### 笔记组织策略

#### 1. PARA 方法
- **P**rojects（项目）- 短期目标
- **A**reas（领域）- 长期责任
- **R**esources（资源）- 参考资料
- **A**rchives（归档）- 完成的项目

#### 2. Zettelkasten（卡片盒）
- 原子化笔记：每条笔记只包含一个想法
- 使用唯一ID标识笔记
- 通过链接建立知识网络
- 创建索引笔记（MOC）

#### 3. 混合方法
- 结合文件夹和标签
- 使用 MOC（Maps of Content）作为导航中心
- Dataview 查询动态聚合内容

### 标签使用技巧
```markdown
# 使用层级标签
#项目/工作/客户A
#项目/个人/学习

# 使用状态标签
#status/进行中
#status/已完成
#status/待定

# 使用内容类型标签
#类型/文献笔记
#类型/永久笔记
#类型/每日笔记
```

### Dataview 查询示例

#### 任务汇总
```dataview
TASK
WHERE !completed
GROUP BY file.folder
```

#### 最近修改的笔记
```dataview
TABLE file.mtime as "修改时间"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

#### 按标签分组
```dataview
LIST
FROM #项目
WHERE status = "进行中"
GROUP BY file.folder
```

### 工作流最佳实践

1. **每日工作流**
   - 早晨：打开日记，规划今日任务
   - 工作中：随时记录想法和笔记
   - 晚上：回顾总结，整理笔记链接

2. **笔记处理流程**
   - 快速捕获 → 收集箱
   - 定期整理 → 分类归档
   - 深度加工 → 建立链接
   - 定期回顾 → 更新维护

3. **知识积累策略**
   - 输入：阅读、学习时做文献笔记
   - 处理：提炼关键概念，创建永久笔记
   - 输出：通过链接形成知识体系
   - 创作：基于笔记网络创作内容

4. **搜索技巧**
   - 使用全局搜索：`Ctrl/Cmd + Shift + F`
   - 搜索语法：
     - `"精确短语"` - 精确匹配
     - `file:文件名` - 搜索特定文件
     - `tag:#标签` - 搜索标签
     - `path:路径` - 搜索特定路径
     - `-排除词` - 排除关键词
     - `(词1 OR 词2)` - 或逻辑

5. **定期维护**
   - 清理孤立笔记（没有链接的笔记）
   - 重命名和重组文件夹结构
   - 更新和完善 MOC
   - 删除或归档过时内容

## 💡 进阶技巧

### 1. 工作区（Workspace）
- 保存不同的布局配置
- 快速切换工作模式
- 命令：管理工作区布局

### 2. 快速切换器增强
- 使用别名快速找到笔记
- 在 YAML 中添加：`aliases: [别名1, 别名2]`

### 3. 使用 CSS Snippets 自定义样式
- 设置 → 外观 → CSS 代码片段
- 在 `.obsidian/snippets/` 文件夹创建 `.css` 文件

### 4. 使用正则表达式搜索和替换
- `Ctrl/Cmd + H` 打开替换
- 点击正则表达式按钮启用

### 5. 利用 URI 链接
```markdown
obsidian://open?vault=库名&file=文件路径
obsidian://search?vault=库名&query=搜索词
```

### 6. 批处理技巧
- 使用 Dataview + Templater 批量处理笔记
- QuickAdd 宏实现复杂操作自动化

### 7. 移动端同步
- 官方 Obsidian Sync（付费）
- iCloud / Dropbox / OneDrive
- Git + Working Copy（iOS）
- Remotely Save 插件

## 🎯 实用建议

1. **从简单开始**：不要一开始就配置太复杂，先熟悉基础功能
2. **渐进式完善**：随着使用慢慢添加插件和工作流
3. **定期备份**：使用 Git 或云端同步保护笔记
4. **保持一致**：制定命名规范和组织规则并坚持执行
5. **工具为人服务**：不要为了工具而工具，专注于内容本身
6. **定期回顾**：每周/月回顾笔记系统，优化工作流

## 📚 学习资源

- [Obsidian 官方文档](https://help.obsidian.md/)
- [Obsidian 中文论坛](https://forum-zh.obsidian.md/)
- [Obsidian Hub](https://publish.obsidian.md/hub/)
- YouTube: Linking Your Thinking 频道
- 《卡片笔记写作法》（Sönke Ahrens 著）

---

**最后更新**：{{date}}
**持续完善中...**

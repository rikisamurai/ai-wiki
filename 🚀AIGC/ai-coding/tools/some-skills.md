---
tags:
  - ai-coding
  - claude-code
  - skills
---


https://agentskills.io/home
A simple, open format for giving agents new capabilities and expertise.
Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently.


skills 商店，可以寻找想要的 skills
https://skills.sh/


# Claude Code Skills 收集


## claude-health

> [!info] 基本信息
> - **作者**：tw93
> - **仓库**：[tw93/claude-health](https://github.com/tw93/claude-health)
> - **协议**：MIT

一个用于系统性审查 Claude Code 项目配置健康状况的 skill。基于**六层框架**来诊断配置：

> `CLAUDE.md → rules → skills → hooks → subagents → verifiers`

运行后会自动检测项目复杂度（Simple / Standard / Complex），并行跑两个诊断 agent，最终输出一份==按优先级排序的修复报告==。

### 检查内容

| 层级 | 检查项 |
|------|--------|
| **CLAUDE.md** | 信噪比、是否缺少 Verification/Compact Instructions、散文冗余 |
| **rules/** | 语言相关规则放置是否正确、覆盖缺口 |
| **skills/** | 描述 token 数、触发清晰度、自动调用策略 |
| **skill 安全性** | Prompt 注入、数据泄露、危险命令、硬编码凭证等 |
| **hooks** | Pattern 字段、文件类型覆盖、过期条目 |
| **MCP** | Server 数量、token 开销估算、上下文压力检测 |
| **Prompt Cache** | 动态时间戳、工具重排、会话中途切模型等破坏缓存的行为 |
| **三层防御** | 关键规则是否同时被 CLAUDE.md + Skill + Hook 覆盖 |

### 输出结果

结果分三个优先级：

- 🔴 **Critical**：立即修复（规则违反、危险权限、缓存破坏、MCP 开销 >12.5%、安全问题）
- 🟡 **Structural**：尽快修复（内容错放、缺少 hooks、单层关键规则）
- 🟢 **Incremental**：锦上添花（上下文卫生、HANDOFF.md 采用、skill 调优）

### 安装与使用

```bash
# 推荐用 npx skills 安装
npx skills add tw93/claude-health

# 或 Claude Plugin 方式
claude plugin marketplace add tw93/claude-health
claude plugin install health
```

在 Claude Code 会话中运行 `/health` 即可启动检查。

> [!tip] 参考资料
> 背后的理论来自 tw93 的博客文章 [《Claude Code 六层框架》](https://tw93.fun/en/2026-03-12/claude.html)，适合想要系统性优化 Claude Code 配置的用户。


## xiaohongshu-cli

> [!info] 基本信息
> - **作者**：jackwener
> - **仓库**：[jackwener/xiaohongshu-cli](https://github.com/jackwener/xiaohongshu-cli)
> - **版本**：0.6.4

小红书命令行工具，让 Claude Code 可以直接搜索、阅读、互动小红书内容，无需打开浏览器或 App。通过浏览器 cookie 自动提取或二维码扫码完成认证。

### 功能一览

| 类别 | 命令示例 | 说明 |
|------|---------|------|
| **搜索** | `xhs search "美食"` | 搜索笔记，支持排序和类型筛选 |
| **阅读** | `xhs read <id/url>` | 阅读笔记内容 |
| **评论** | `xhs comments <id/url>` | 查看评论，支持 `--all` 全量拉取 |
| **推荐流** | `xhs feed` | 浏览推荐内容 |
| **热门** | `xhs hot -c food` | 按分类浏览热门（food/travel/fitness 等） |
| **点赞/收藏** | `xhs like` / `xhs favorite` | 互动操作 |
| **评论/回复** | `xhs comment` / `xhs reply` | 发表评论或回复 |
| **关注** | `xhs follow` / `xhs unfollow` | 关注或取关用户 |
| **发布** | `xhs post --title "..." --body "..."` | 发布笔记，支持图片 |
| **账号** | `xhs login` / `xhs status` / `xhs whoami` | 认证与账号管理 |

### 安装与使用

```bash
# 安装（需要 Python 3.10+）
uv tool install xiaohongshu-cli

# 认证（二选一）
xhs login                  # 从浏览器自动提取 cookie
xhs login --qrcode         # 二维码扫码登录
```

在 Claude Code 中直接与小红书交互即可触发该 skill。

> [!warning] 注意事项
> - 内置请求限速（~1-1.5s 间隔），不要并行请求以保护账号安全
> - 不支持视频下载、私信、直播、关注列表
> - 同一时间只支持单账号


## baoyu-skills

> [!info] 基本信息
> - **作者**：宝玉 (JimLiu)
> - **仓库**：[JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)

宝玉分享的 Claude Code Skills 合集，涵盖内容生成、AI 图片生成和实用工具三大类，旨在提升日常工作效率。所有 skill 支持通过 `EXTEND.md` 文件进行自定义配置。

### 内容生成类 Skills

| Skill | 说明 |
|-------|------|
| **baoyu-xhs-images** | 小红书信息图生成器，将内容拆分为 1-10 张卡通风格图片，支持 **Style × Layout** 二维系统（9 种视觉风格 + 6 种布局） |
| **baoyu-infographic** | 专业信息图生成，提供 20 种布局类型和 17 种视觉风格，自动推荐最佳组合 |
| **baoyu-cover-image** | 文章封面图生成，采用 **Type × Palette × Rendering × Text × Mood** 五维系统，9 种配色 × 6 种渲染风格 |
| **baoyu-slide-deck** | 幻灯片生成，从内容创建大纲并逐页生成图片，支持 16 种预设风格，最终自动合并为 `.pptx` 和 `.pdf` |
| **baoyu-comic** | 知识漫画创作，支持 Art Style × Tone 组合（5 种画风 + 7 种基调），含 ohmsha、wuxia、shoujo 等预设 |
| **baoyu-article-illustrator** | 智能文章配图，分析文章结构后在合适位置插入插图，支持 Type × Style 二维选择 |

### 内容发布类 Skills

| Skill | 说明 |
|-------|------|
| **baoyu-post-to-x** | 发布内容到 X (Twitter)，支持普通推文和 X Articles 长文，使用 Chrome CDP 绕过反自动化 |
| **baoyu-post-to-wechat** | 发布到微信公众号，支持贴图模式和文章模式，可通过 API 或浏览器发布，支持多账号 |
| **baoyu-post-to-weibo** | 发布到微博，支持文字/图片/视频普通微博和头条文章 |

### AI 生成后端类 Skills

| Skill | 说明 |
|-------|------|
| **baoyu-image-gen** | 基于 AI SDK 的图片生成，统一封装了 OpenAI、Azure OpenAI、Google、OpenRouter、DashScope（通义万相）、即梦、豆包 Seedream、Replicate 等多个 provider，支持文生图、参考图和多种尺寸 |
| **baoyu-danger-gemini-web** | 通过 Gemini Web 界面生成文本和图片（使用浏览器自动化） |

### 工具类 Skills

| Skill | 说明 |
|-------|------|
| **baoyu-youtube-transcript** | 下载 YouTube 视频字幕/转录，支持多语言、翻译、章节分段和说话人识别，带本地缓存 |
| **baoyu-url-to-markdown** | 通过 Chrome CDP 抓取任意 URL 并转为干净的 Markdown，支持登录页面的等待模式 |
| **baoyu-danger-x-to-markdown** | 将 X (Twitter) 推文/线程/Articles 转为 Markdown，支持媒体下载 |
| **baoyu-compress-image** | 图片压缩，在保持质量的同时减小文件体积 |
| **baoyu-format-markdown** | Markdown 格式化，自动添加 frontmatter、标题、摘要，规范化排版 |
| **baoyu-markdown-to-html** | Markdown 转 HTML，支持微信公众号主题、代码高亮和底部引用 |
| **baoyu-translate** | 文档翻译，提供 quick / normal / refined 三种模式，支持自定义术语表、受众和风格，长文档自动分块并行翻译 |

### 安装与使用

```bash
# 推荐方式
npx skills add jimliu/baoyu-skills

# 或通过 Claude Code Plugin
/plugin marketplace add JimLiu/baoyu-skills
```

> [!tip] 环境配置
> 部分 skill（如 baoyu-image-gen）需要配置 API Key。可在 `~/.baoyu-skills/.env`（用户级）或 `<项目>/.baoyu-skills/.env`（项目级）中设置环境变量。支持 OpenAI、Google、DashScope、即梦、豆包等多个 provider 的 Key 配置。


## architecture-diagram-generator

> [!info] 基本信息
> - **作者**：Cocoon AI
> - **仓库**：[Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)
> - **协议**：MIT

一个 Claude Skill，用自然语言描述系统架构，自动生成精美的暗色主题架构图。输出为自包含的 HTML 文件，可直接在浏览器打开，无需任何额外依赖。

### 核心特性

- **文字 → 架构图**：用自然语言描述组件和连接关系，自动生成 SVG 架构图
- **自包含输出**：单个 HTML 文件，内嵌 CSS + 内联 SVG，任何浏览器直接打开
- **语义化配色**：自动为不同组件类型分配颜色
- **可迭代**：生成后可通过对话继续修改布局、组件、样式

### 示例效果

**Web Application (React + Node.js + PostgreSQL)**

![[🚀AIGC/ai-coding/tools/asset/arch-diagram-web-app.png]]

**AWS Serverless (Lambda + API Gateway + DynamoDB)**

![[🚀AIGC/ai-coding/tools/asset/arch-diagram-aws-serverless.png]]

**Microservices (Kubernetes + API Gateway)**

![[🚀AIGC/ai-coding/tools/asset/arch-diagram-microservices.png]]

### 配色方案

| 组件类型 | 颜色 | 适用 |
|---------|------|------|
| Frontend | Cyan | 客户端、UI |
| Backend | Emerald | 服务端、API |
| Database | Violet | 数据库、存储、AI/ML |
| Cloud/AWS | Amber | 云服务、基础设施 |
| Security | Rose | 认证、安全 |

### 使用方式

1. 下载 `architecture-diagram.zip`，在 Claude.ai → Settings → Capabilities → Skills 中上传启用
2. 描述你的架构（手写 / 让 AI 分析代码库 / 请求典型架构模板）
3. 让 Claude 使用该 Skill 生成图表

描述架构模板
```
Analyze this codebase and describe the architecture. Include all major
components, how they connect, what technologies they use, and any cloud
services or integrations. Format as a list for an architecture diagram.
```


```
Use your architecture diagram skill to create an architecture diagram from this description:
[你的架构描述]
```

### 安装

```bash
# Claude Code CLI
unzip architecture-diagram.zip -d ~/.claude/skills/

# 或项目级
unzip architecture-diagram.zip -d ./.claude/skills/
```

> [!warning] 注意事项
> - 需要 Claude Pro / Max / Team / Enterprise 订阅
> - 输出为静态 HTML/SVG，不支持交互式编辑
> - 字体依赖 Google Fonts（JetBrains Mono），离线环境可能降级





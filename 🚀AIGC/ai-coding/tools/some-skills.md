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

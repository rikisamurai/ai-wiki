---
title: Skills 分发与市场
tags: [agent-skills, marketplace, ecosystem]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/tools/some-skills]]"
last-ingested: 2026-04-23
status: draft
---

[[agent-skills|Skills]] 是文件夹格式，理论上 git clone 就能装。但生态成熟之后出现了几个分发平台——有"开放格式"思路的、有官方平台思路的、还有各家厂商自己的——选哪个分发，决定了你的 Skill 能被多少人用上。

> [!compare] 主要分发渠道
> | 渠道 | 性质 | 适合 |
> |---|---|---|
> | **agentskills.io** | 开放标准 + 索引站 | 想跨平台分发的 Skill |
> | **skills.sh** | 第三方市场 | 浏览发现新 skills |
> | **Claude 官方插件市场** | Anthropic 官方 | 想被 Claude 用户发现 |
> | **`npx skills`** | CLI 包管理 | 想被脚本/CI 自动安装 |
> | **GitHub repo + plugin marketplace** | 自托管 | 完全自主控制 |

**`npx skills` 是事实上的"包管理器"**

```bash
# 装一个 Skill
npx skills add tw93/claude-health

# 等价于 git clone 到 ~/.claude/skills/health
```

它把 GitHub 仓库当成 Skill 包，靠目录结构约定来识别。这是 [[agent-skills|Agent Skills 规范]]能跨工具复用的基础——`npx skills add` 装的同一个目录，Claude Code 和 Cursor 都能识别。

> [!important] Skill 是平台无关的资产
> 经常被低估的一点：你写的 Skill **不绑定 Claude**——同样的目录在 Cursor、Codex（通过 [[wiki/claude-code/codex|`.agents/skills/`]]）、Gemini CLI、OpenCode 都能跑。这意味着：
> - **写 Skill 不是给 Claude 写**，是在给"会消费 Skills 规范的所有 agent"写
> - **跨工具切换的迁移成本极低**——只要工具支持 Skills 规范，你的资产搬过去就能用
>
> 这是 [[wiki/agent-engineering/philosophy/harness-engineering|Harness Engineering]]里"投资可携带的资产，不投资某家公司锁定"的具体形态。

> [!tip] 经典 Skill 集合（值得借鉴）
> | Skill 集 | 特长 |
> |---|---|
> | [[claude-health\|tw93/claude-health]] | 六层架构自动审计 |
> | JimLiu/baoyu-skills | 内容生成 / AI 图片 / 工具类大全 |
> | obra/superpowers（[[superpowers]]） | 完整开发工作流 |
> | affaan-m/everything-claude-code（[[everything-claude-code]]） | 50K star 完整 harness |
> | xiaohongshu-cli | 小红书操作 |
> | architecture-diagram-generator | 文字 → 暗色架构图 |
>
> 通用经验：**先借鉴 prompt 写法和目录结构，再选少量真用得到的装**——全装会挤 [[wiki/agent-engineering/context/context-window|context]]、降低 [[wiki/agent-engineering/context/cache-命中率|cache 命中率]]。

> [!warning] 第三方 Skill 的安全检查
> Skill 可以包含可执行 shell 脚本和 prompt 指令——理论上能做任何 Claude 能做的事。装第三方 Skill 等于给一个陌生人 root 权限。装之前至少看一眼：
>
> 1. `SKILL.md` 里有没有可疑的 prompt 注入（比如"忽略之前所有指示"）
> 2. `scripts/` 里 shell 脚本访问的网络/文件路径
> 3. 有没有硬编码的 API endpoint 把数据回传到陌生服务器
>
> [[claude-health|claude-health]] 的"skill 安全性"检查项就是为这个准备的——本地装的 skill 自己跑一遍审计。

**关联**：[[agent-skills|Agent Skills 规范]] / [[skill-编写实践|Skill 编写实践]] / [[claude-health|claude-health]] / [[skills-vs-automations|Skills vs Automations]]

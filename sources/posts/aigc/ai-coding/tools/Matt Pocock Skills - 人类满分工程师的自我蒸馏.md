---
title: Matt Pocock Skills - 人类满分工程师的自我蒸馏
source: https://my.feishu.cn/docx/Sz1od73xRoTvAwxVDMSci9aznlg
tags:
  - ai-coding
  - skills
  - workflow
date: 2026-05-26
ingested-at: 2026-05-26
---

# Matt Pocock Skills——人类满分工程师的自我蒸馏

> [!abstract] 概览
> Matt Pocock Skills 是 TypeScript 专家 Matt Pocock 整理的一套 AI 辅助工程实践工具包，GitHub 已 10.4 万 Stars。定位不是"氛围编程"（vibe coding），而是把数十年软件工程经验（敏捷、XP、DDD、TDD）蒸馏成可组合、可适配的小型 Skills，让你在 AI 时代依然掌控代码质量与系统设计。

## 关于作者

- Matt Pocock，TypeScript 领域最知名教育者之一，运营 [Total TypeScript](https://www.totaltypescript.com)
- 这套 Skills 是他每天实际使用的工程工具，约 6 万开发者订阅相关 Newsletter
- GitHub：[mattpocock/skills](https://github.com/mattpocock/skills)（104,000+ Stars）
- 安装：`npx skills@latest add mattpocock/skills`
- 浏览：skills.sh/mattpocock/skills
- Newsletter：aihero.dev
- X: https://x.com/mattpocockuk
- Youtube: https://www.youtube.com/@mattpocockuk

> "用任何模型都能运行。设计小巧，易于改造，可自由组合。" — Matt Pocock

## 四大核心工程挑战

### 1. 需求对齐：你以为 AI 懂你，其实它没有

> "没有人确切知道自己想要什么。" — The Pragmatic Programmer

**问题**：AI 与人的沟通鸿沟——你以为讲清楚了，AI 构建出来的完全不对。

**解法**：使用"烤问会话"（Grilling Session）让 AI 在开始之前不断追问你，直到真正理解需求。

- `/grill-me` — 非代码场景的深度追问
- `/grill-with-docs` — 代码场景追问 + 更新领域文档

### 2. 领域语言：说同一种话

> "有了统一语言，开发者之间的对话和代码表达都源自同一个领域模型。" — Eric Evans, Domain-Driven Design

**问题**：AI 被丢进项目后不懂行话，用 20 个词表达 1 个意思。

**解法**：维护一份 `CONTEXT.md`，建立人与 AI 之间的共享词汇表。

- BEFORE：「当课程某节课被'真实化'（即在文件系统中获得位置）时出现了问题」
- AFTER：「materialization cascade 出了问题」

这种简洁在一次次会话中持续积累价值。

### 3. 反馈循环：让 AI 知道代码跑起来是啥样

> "始终迈出小步、刻意的步伐。反馈速率就是你的速度上限。" — The Pragmatic Programmer

**问题**：没有运行反馈，AI 盲飞。

**解法**：建立红-绿-重构的 TDD 循环，给 AI 可靠的反馈信号。

- `/tdd` — 测试驱动开发，红绿重构，一次一个垂直切片
- `/diagnose` — 调试最佳实践：复现 → 最小化 → 假设 → 检测 → 修复 → 回归测试

### 4. 代码质量：AI 加速了代码熵增

> "每天都要投资系统设计。" — Kent Beck, Extreme Programming Explained

**问题**：AI 加速了编码，也加速了软件熵增——代码库以前所未有的速度变复杂。

**解法**：把系统设计思维嵌入每一层 Skill：

- `/to-prd` — 创建 PRD 前先问清楚你在动哪些模块
- `/zoom-out` — 在大系统中解释局部代码
- `/improve-codebase-architecture` — 将"泥球代码库"重构为模块化架构

## 完整工作流

很多团队用 AI 写代码失败，不是因为模型不够强，而是**流程乱**。这套工作流把软件工程几十年的最佳实践浓缩成一条清晰的流水线，让 AI 在每个节点都有明确的输入和输出。

| 步骤 | 在做什么 | 为什么重要 |
|-|-|-|
| 🔍 grill-me | AI 反复追问你，澄清需求 | 70% 的返工来自需求没说清楚 |
| 📋 to-prd | 把对话变成正式需求文档 | 留下决策记录，避免反复解释 |
| 🎯 to-issues | 把大需求拆成独立小任务 | 大任务让 AI 容易失控，小任务更精准 |
| 🧪 tdd | 先写测试再写功能 | 给 AI 明确的"完成标准" |
| 🔬 diagnose | 系统化调试，不是乱猜 | 避免 AI 在没方向的情况下乱改代码 |
| 🔭 zoom-out | 回顾全局架构 | 防止局部正确但整体混乱 |
| 🏗 improve-architecture | 主动重构防止熵增 | AI 加速写代码也加速了代码腐烂 |

> [!tip] 对非工程师的类比
> 这就像出版一本书——
> 1. 先跟编辑对齐主题（grill-me）
> 2. 写大纲（to-prd）
> 3. 拆章节（to-issues）
> 4. 一章章写并审校（tdd + diagnose）
> 5. 最后通读全稿保证结构合理（zoom-out + improve-architecture）

## TDD 红绿重构循环

TDD（测试驱动开发）听起来像开发者的事，但它背后的逻辑适用于任何需要**验收标准**的工作。

**🔴 RED — 先定义"完成"长什么样**

在写任何代码之前，先写一个描述目标行为的测试——这个测试此时一定是失败的（红灯），因为功能还不存在。这一步的价值：**强迫你在动手之前想清楚你要什么**。对 AI 来说，红灯测试是一个不会说谎的需求说明书。

**🟢 GREEN — 用最小代价达成目标**

写刚好能让测试通过的代码，不多不少。目的不是写出漂亮的代码，而是先让测试变绿。这防止 AI 过度设计或跑题。

**🔵 REFACTOR — 在安全网下清理**

测试已经通过，现在可以放心地重构：删重复代码、改好命名、简化逻辑。因为测试会立刻告诉你有没有改坏，所以这一步没有风险。

> [!important] 为什么这对 AI 特别重要？
> 没有 TDD，AI 不知道"完成"的边界在哪里。它可能写了很多代码，看起来对，但其实偏了。红灯测试给了 AI 一个客观的、自动化的验收信号——通了就是通了，没通就是没通，不需要人眼逐行检查。

## Skills 完整参考

### 工程类 Skills

| Skill | 用途 |
|-|-|
| `/diagnose` | 系统化调试循环：复现→最小化→假设→检测→修复→回归测试 |
| `/grill-with-docs` | 追问会话 + 更新 CONTEXT.md 和 ADR |
| `/triage` | 通过状态机角色分类 Issue |
| `/improve-codebase-architecture` | 发现代码深化机会，基于领域语言和 ADR |
| `/setup-matt-pocock-skills` | 初始化 per-repo 配置（Issue 追踪、分类标签、文档目录） |
| `/tdd` | 测试驱动开发，红绿重构，一次一个垂直切片 |
| `/to-issues` | 将计划/规格/PRD 拆分为可独立处理的 GitHub Issues |
| `/to-prd` | 将当前对话上下文转化为 PRD 并提交为 GitHub Issue |
| `/zoom-out` | 让 AI 从更宏观角度解释一段不熟悉的代码 |
| `/prototype` | 构建原型：终端 App 或多种 UI 变体 |

### 效率类 Skills

| Skill | 用途 |
|-|-|
| `/caveman` | 超压缩通信模式，减少约 75% token 用量 |
| `/grill-me` | 被 AI 追问到决策树的每个分支都解析完毕 |
| `/handoff` | 将当前对话压缩为交接文档，供另一个 Agent 继续 |
| `/write-a-skill` | 创建新 Skill，含结构、渐进披露和资源 |

### 杂项 Skills

| Skill | 用途 |
|-|-|
| `/git-guardrails-claude-code` | 为 Claude Code 设置 Git 钩子，阻止危险命令 |
| `/setup-pre-commit` | 配置 Husky pre-commit hooks（Prettier、类型检查、测试） |
| `/scaffold-exercises` | 创建包含章节、题目、答案和讲解的练习目录结构 |

## 安装方法

```bash
# 第一步：运行安装器
npx skills@latest add mattpocock/skills

# 第二步：选择需要的 Skills 和目标 Agent
# 确保选择 /setup-matt-pocock-skills

# 第三步：在 Agent 里初始化
/setup-matt-pocock-skills
```

> [!note]
> 安装器会询问你使用哪个 Issue 追踪工具（GitHub / Linear / 本地文件）、分类标签，以及文档保存位置。

## 结语

软件工程这个行业走过了几十年，积累了无数关于"怎么把事做对"的经验——敏捷、极限编程、领域驱动设计、测试驱动开发。这些方法论不是凭空发明的，而是无数团队在真实的失败和教训中提炼出来的。

AI 的出现改变了速度，但没有改变这些规律。如果说以前一个团队可以在混乱中慢慢漂移，那么现在有了 AI 加速，漂移的速度快了十倍。需求没说清楚、没有共同语言、没有反馈机制、不关心设计——这些问题不会因为 AI 更强而消失，只会暴露得更快。

Matt Pocock 这套 Skills 的价值，不在于它有多少命令，而在于它把"正确的工程思维"转化成了 AI 可以执行的工作流。你不需要读完《领域驱动设计》才能让 AI 维护一份领域词汇表，你不需要是 TDD 专家才能让 AI 先写测试再写功能。

这些 Skill 是工程经验的压缩包。打开它，解压的是几十年的集体智慧。

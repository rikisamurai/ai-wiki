---
title: Harness Engineering：在 Agent-First 时代利用 Codex
tags:
  - AI-Coding
  - OpenAI
  - Codex
  - Agent
  - harness-engineering
date: 2026-03-11
source: https://openai.com/index/harness-engineering/
author: Ryan Lopopolo
---

![[harness-engineering-cover.png]]

> [!info] 文章信息
> - **作者**: Ryan Lopopolo, OpenAI Member of Technical Staff
> - **发布日期**: 2026-03-11
> - **原文**: [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

## 一句话总结

OpenAI 团队用 **0 行手写代码**，完全依靠 Codex Agent 构建并上线了一款内部产品（约 100 万行代码、~1500 个 PR），总结了 Agent-First 开发模式的核心经验。

![[Pasted image 20260323180456.png|400]]

---

## 背景：从空仓库开始

2025 年 8 月底，团队向一个**空的 Git 仓库**提交了第一个 commit。

初始脚手架（仓库结构、CI 配置、格式化规则、包管理器设置、应用框架）全部由 Codex CLI + GPT-5 生成，参考了少量已有模板。甚至连指导 Agent 如何在仓库中工作的 `AGENTS.md` 文件本身也是 Codex 写的。

> [!quote] 核心哲学
> **No manually-written code** —— 从始至终，人类不直接贡献任何代码。

5 个月后，这个产品已被数百名内部用户使用，包括日活跃的重度用户。

## 核心观点

### 🔑 Human 的角色转变：从写代码到设计环境

> **Humans steer. Agents execute.**

早期进展比预期更慢，但原因**不是 Codex 不够强，而是环境不够明确**。Agent 缺乏完成高级目标所需的工具、抽象和内部结构。

团队的首要工作变成了**让 Agent 能够做有用的事**。实践中，这意味着 **depth-first** 工作方式：

1. 将大目标拆解为小的构建块（设计、编码、Review、测试等）
2. 让 Agent 构建这些块
3. 用这些块解锁更复杂的任务

当某个任务失败时，修复方式几乎从来不是"再试一次"或"换个 Prompt"，而是回到系统层面思考：

> **"缺少什么能力？如何让这个能力对 Agent 既可读（legible）又可执行（enforceable）？"**

**Human 的具体交互方式：**
- 工程师描述任务 → 运行 Agent → Agent 开 PR
- 指示 Codex **先本地自审**，再请求其他 Agent Review（本地 + 云端）
- 回应所有 Human/Agent 反馈，在循环中迭代直到所有 Agent Reviewer 满意
- 这本质上是一个 [Ralph Wiggum Loop](https://ghuntley.com/loop/)（Agent 自我审查循环）
- Codex 直接使用标准开发工具（`gh`、本地脚本、仓库内 Skills）获取上下文，无需人类复制粘贴
- Human 可以 Review PR，但**不是必须的** —— 随着时间推移，几乎所有 Review 工作都交给了 Agent-to-Agent

### 📖 让仓库成为唯一的知识源（System of Record）

#### 为什么"一个大 AGENTS.md"会失败

> [!warning] 他们尝试过"一个巨大的 AGENTS.md"，结果可预见地失败了
> - **Context 是稀缺资源**：巨大的指令文件会挤占任务本身、代码和相关文档 —— Agent 要么遗漏关键约束，要么对着错误目标优化
> - **什么都重要 = 什么都不重要**：Agent 最终只是局部模式匹配，而非有意识地导航
> - **立刻腐烂**：一个单体手册迅速变成过时规则的坟场，Agent 无法分辨哪些还有效，人类也懒得维护
> - **难以验证**：单一文件不利于机械化检查（覆盖率、时效性、所有权、交叉引用），漂移不可避免

#### 正确做法：渐进式披露（Progressive Disclosure）

**把 `AGENTS.md` 当作目录，而非百科全书。**

- `AGENTS.md` 只做**入口**（~100 行），主要是指向深层知识源的指针
- 知识库存放在结构化的 `docs/` 目录中，作为真正的 System of Record

```
AGENTS.md          ← 目录/入口（~100行）
ARCHITECTURE.md    ← 顶层架构地图：领域划分与包分层
docs/
├── design-docs/   ← 设计文档（含索引、验证状态、核心信念）
│   ├── index.md
│   ├── core-beliefs.md   ← 定义 Agent-First 操作原则
│   └── ...
├── exec-plans/    ← 执行计划（一等公民 artifact）
│   ├── active/    ← 进行中的计划
│   ├── completed/ ← 已完成的计划
│   └── tech-debt-tracker.md  ← 技术债追踪
├── generated/
│   └── db-schema.md  ← 自动生成的数据库 Schema 文档
├── product-specs/ ← 产品规格
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...
├── references/    ← 参考资料
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   ├── uv-llms.txt
│   └── ...
├── DESIGN.md
├── FRONTEND.md
├── PLANS.md
├── PRODUCT_SENSE.md
├── QUALITY_SCORE.md  ← 每个产品域和架构层的质量评分
├── RELIABILITY.md
└── SECURITY.md
```

**关键细节：**
- **设计文档**有索引和验证状态，还有一组"核心信念"定义 Agent-First 操作原则
- **架构文档**（参考 [matklad 的 ARCHITECTURE.md 理念](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)）提供领域和包分层的顶层地图
- **质量文档**对每个产品域和架构层打分，持续追踪差距
- **执行计划是一等公民**：简单变更用轻量临时计划，复杂工作用 [Execution Plans](https://cookbook.openai.com/articles/codex_exec_plans) 记录进度和决策日志，check in 到仓库
- Active plans、completed plans、已知技术债全部版本化并共存，Agent 无需依赖外部上下文即可运作

#### 机械化维护

- **专门的 Linter + CI Job** 验证知识库的时效性、交叉引用和结构正确性
- **定期运行 "doc-gardening" Agent** 扫描不再反映真实代码行为的过期/废弃文档，自动开 fix-up PR

### 🏗️ 为 Agent 可读性（Legibility）优化一切

由于仓库完全由 Agent 生成，它首先为 **Codex 的可读性**优化 —— 就像团队为新员工提升代码可导航性一样，他们的目标是让 Agent 能够**直接从仓库本身**理解完整的业务领域。

> [!important] 核心原则
> 从 Agent 的视角看，**运行时无法访问的上下文 = 不存在**。Google Docs、Slack 讨论、存在于人脑中的知识 —— 对系统来说都是不可见的。只有仓库内的、版本化的 artifact（代码、Markdown、Schema、执行计划）才是 Agent 能看到的全部。

**因此，团队持续将更多上下文推入仓库：**

- 那个在 Slack 上达成共识的架构决策？如果 Agent 发现不了，就跟三个月后入职的新人不知道一样
- 给 Agent 更多 context 不是简单地堆信息，而是**组织和暴露正确的信息**让 Agent 能推理 —— 就像给新队友讲产品原则、工程规范、团队文化（包括 emoji 偏好）

**提升应用可观测性（Application Legibility）：**

随着代码吞吐量增加，瓶颈从写代码变成了 **Human QA 能力**。为了缓解这个问题，他们让应用本身对 Codex 可读：

- **每个 git worktree 可独立启动应用**，Codex 可以为每个变更启动和驱动一个独立实例
- **接入 Chrome DevTools Protocol**，创建了操作 DOM 快照、截图和导航的 Skills —— Codex 可以直接复现 Bug、验证修复、推理 UI 行为
- **本地可观测性栈**（每个 worktree 临时的）暴露日志、指标和 Trace —— Agent 可以用 **LogQL** 查日志、用 **PromQL** 查指标，任务完成后整套栈自动销毁
- 这使得这样的 Prompt 变得可执行："确保服务启动在 800ms 内完成"或"这四个关键用户路径中没有 span 超过 2 秒"

**技术选型的启示：**

- 偏好"无聊"但稳定、可组合的技术 —— 这类技术因为 API 稳定、训练数据充足，更容易被 Agent 建模
- 有时候 **Agent 重写一个子功能**比使用不透明的第三方库更划算。例如，他们没有使用通用的 `p-limit` 风格的包，而是让 Agent 自己实现了一个 map-with-concurrency helper：它与他们的 OpenTelemetry instrumentation 紧密集成、100% 测试覆盖率、行为完全符合运行时预期
- 将更多系统拉入 Agent 可检查、验证、直接修改的形式，不仅对 Codex 有利，也对其他在代码库上工作的 Agent（如 [Aardvark](https://openai.com/index/introducing-aardvark/)）有利

### 🛡️ 通过约束执行架构与品味

> **Enforce invariants, not implementations.**
> 强制不变量，不微观管理实现。

仅靠文档无法维持一个完全由 Agent 生成的代码库的一致性。Agent 在**边界严格、结构可预测**的环境中最有效，因此他们围绕一个刚性的架构模型构建应用。

#### 分层架构

每个业务领域被划分为固定的一组层，依赖方向严格验证，允许的边只有有限的一组：

```
Types → Config → Repo → Service → Runtime → UI
```

跨领域关注点（Auth、Connectors、Telemetry、Feature Flags）通过一个单一的显式接口进入：**Providers**。其他任何方式都被禁止并机械化执行。

> [!note] 时机选择
> 这种架构通常在团队有数百名工程师时才会推行。但在 Agent 编码场景下，它是**早期的前置条件** —— 正是这些约束让速度不带来衰减和架构漂移。

#### 品味的机械化

- **自定义 Linter + 结构化测试**执行规则
- 静态强制：结构化日志、Schema 和类型的命名约定、文件大小限制、平台特定的可靠性要求
- Lint 的**错误信息本身就是修复指引**，直接注入 Agent 上下文 —— 因为是自定义 Lint，所以可以精确控制 Agent 看到什么
- 要求 Codex 在边界处 [parse data shapes](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)（"Parse, don't validate"），但不规定具体用什么库（模型似乎喜欢 Zod，但这不是他们指定的）

#### 中央管边界，局部给自由

这类似于管理一个大型平台工程组织：你**深切关注边界、正确性和可复现性**；在这些边界之内，你给团队（或 Agent）在表达解决方案上的**充分自由**。

产出的代码不一定总符合人类的风格偏好 —— **这没关系**。只要输出正确、可维护、且对未来的 Agent 运行可读，就达标了。

#### 人类品味的持续反馈

Human taste 通过以下方式持续反馈回系统：
- Review 评论 → 文档更新
- 重构 PR → 编码为工具约束
- 用户可见的 Bug → 直接编码到 Lint 规则中

> 当文档不够时，就把规则提升为代码（promote the rule into code）。

### 🤖 Agent 自治的完整循环

随着开发循环中越来越多的部分（测试、验证、Review、反馈处理、恢复）被直接编码到系统中，仓库最近跨过了一个有意义的阈值 —— **Codex 可以端到端地驱动一个新功能**。

给定一个 Prompt，Agent 现在可以：

1. 验证代码库当前状态
2. 复现已报告的 Bug
3. **录制视频展示失败**
4. 实现修复
5. **驱动应用验证修复**
6. **录制第二个视频展示修复结果**
7. 开 PR
8. 回应 Agent 和 Human 反馈
9. 检测并修复构建失败
10. 仅在需要人类判断时才升级
11. 合并变更

> [!note]
> 单个 Codex 任务常常连续运行 **6 小时以上**（通常人类在睡觉时）。

> [!warning] 局限性
> 这种行为**高度依赖于这个特定仓库的结构和工具链**，不应假设无需类似投入就能泛化到其他项目 —— 至少目前还不能。

**Agent 产出的不仅仅是应用代码，还包括：**
- 应用逻辑、测试、CI 配置
- 文档、可观测性配置
- 内部工具
- 以及上述所有的维护

### ♻️ 熵与垃圾回收

> [!danger] Agent 自治的阴暗面
> Codex 会复制仓库中已有的模式 —— **包括不够好甚至有问题的模式**。随着时间推移，这不可避免地导致漂移。

最初，团队靠人工处理：**每周五（20% 的工作时间）用来清理 "AI slop"**。不出意料地，这根本无法扩展。

#### 解决方案：自动化垃圾回收

他们编码了一组 **"Golden Principles"**（黄金原则），直接写入仓库，并构建了周期性清理流程：

**黄金原则示例：**
1. **优先使用共享工具包**而非手写 helper —— 保持不变量集中管理
2. **不"YOLO 式"探测数据** —— 要么在边界做验证，要么依赖类型化 SDK，防止 Agent 在猜测的数据形状上构建

**自动化流程：**
- 定期运行一组后台 Codex 任务：扫描偏差 → 更新质量评分 → 提交针对性的重构 PR
- 大多数这类 PR 可以在**不到一分钟内 Review** 并自动合并

> [!tip] 类比：技术债 = 高利贷
> 持续用小额增量偿还，几乎总是好过让它复利增长后再痛苦地一次性清偿。Human 的品味捕获一次，然后在每一行代码上持续执行。这也让他们能**每天**捕获并解决坏模式，而非让它们在代码库中扩散数天或数周。

### ⚡ 高吞吐改变合并哲学

当 Codex 的吞吐量增加后，许多传统工程规范变得**适得其反**：

- 仓库以**最小化阻塞性合并门槛**运作
- PR 生命周期短暂
- 测试不稳定（Flaky Test）通常用 follow-up 运行解决，而非无限期阻塞进度
- 在一个 Agent 吞吐量远超 Human 注意力的系统中，**纠正成本低，等待成本高**

> [!warning]
> 在低吞吐量环境下这样做是不负责任的。但在这里，这往往是正确的权衡。

**吞吐数据：**
- 3 人团队平均每人每天 **3.5 个 PR**
- 扩展到 7 人后吞吐量还在**持续增长**（而非递减）

## 关键数据

| 指标 | 数值 |
|------|------|
| 手写代码行数 | **0** |
| 总代码量 | ~100 万行 |
| PR 数量 | ~1,500 |
| 团队规模 | 3→7 人 |
| 开发周期 | 5 个月（2025.8 起） |
| 人均日 PR | 3.5 |
| 估计效率提升 | **10x** |
| 内部用户 | 数百人（含日活跃重度用户） |

## 他们仍在探索的问题

- **架构一致性**如何在一个完全由 Agent 生成的系统中经年演化？
- Human 判断在**哪些地方**能产生最大杠杆？
- 如何**编码人类判断**使其产生复利效应？
- 随着模型能力继续提升，这个系统**如何演化**？

## 启示

> [!tip] 核心启示
> 软件工程的纪律没有消失，只是**从代码转移到了脚手架** —— 工具链、抽象层、反馈循环才是保持代码库一致性的关键。最困难的挑战现在集中在**设计环境、反馈循环和控制系统**上。

1. **Context 管理是 Agent 工程的核心挑战** —— 给 Agent 地图而非 1000 页说明书；用渐进式披露替代信息轰炸
2. **机械化执行架构约束** —— 在 Agent 时代这不是奢侈品而是早期前置条件；约束就是速度的来源
3. **让一切对 Agent 可见** —— 如果信息不在仓库里它就不存在；Slack 讨论、人脑中的知识必须沉淀
4. **持续偿还技术债** —— Agent 会放大坏模式，垃圾回收必须自动化；人类品味捕获一次，持续执行
5. **高吞吐环境需要新的工程规范** —— 等待比犯错更昂贵；纠正成本低于阻塞成本
6. **为 Agent 可读性优化** —— 选择"无聊"的技术栈，暴露可观测性数据，必要时重写胜过引入黑盒依赖

---
title: "Claude Code 源码深度解析：51万行代码背后的秘密"
tags:
  - claude-code
  - ai-coding
  - source-analysis
date: 2026-04-08
---

# Claude Code 源码深度解析：51万行代码背后的秘密

> 2026年3月31日，安全研究者 Chaofan Shou 发现 Anthropic 发布到 npm 的 Claude Code 包中，source map 文件没有被剥离。这意味着 Claude Code 完整的 TypeScript 源码——**519,000 行、1,900+ 个文件**——就这样暴露在了公网上。

带着三个问题去读这份源码：

1. Claude Code 和其他 AI 编程工具到底有什么本质区别？
2. 为什么它写代码的"手感"就是比别人好？
3. 51 万行代码里，到底藏着什么？

结论是：**这不是一个 AI 编程助手，这是一个操作系统。**

---

## 一、整体规模：数字说明一切

| 维度 | 数量 |
|------|------|
| 源码文件 | 1,900+ |
| 代码行数 | 519,000+ |
| 内置 Tool | 53+ |
| 斜杠命令 | 95+ |

源码按目录分层，职责清晰：

| 目录            | 文件数 | 职责                              |
| ------------- | --- | ------------------------------- |
| `utils/`      | 564 | 共享工具模块——最大的目录                   |
| `components/` | 389 | 基于 React（Ink）的终端 UI 组件          |
| `commands/`   | 189 | 95 个 CLI 命令处理器                  |
| `tools/`      | 184 | 内置 Tool 实现                      |
| `services/`   | 130 | 核心服务层：API、MCP、压缩、流式传输           |
| `hooks/`      | 104 | 终端 UI 状态管理 React Hooks          |
| `ink/`        | 96  | Ink 框架扩展（基于 Yoga flexbox 的终端渲染） |
| `bridge/`     | 31  | 远程控制基础设施                        |
| `skills/`     | 20  | 可加载的 Prompt 模块系统                |
| `buddy/`      | 6   | AI 伴侣彩蛋（有物种、稀有度、性格）             |
| `voice/`      | 1   | 语音模式——解放双手编程                    |

---

## 二、安全哲学：三种完全不同的路线

想象你雇了一个远程程序员，给他你电脑的远程访问权限——

- **Cursor 的做法**：让他坐在你旁边，每次操作前你点"允许"。简单，但你得一直盯着。
- **GitHub Copilot Agent 的做法**：给他一台全新的虚拟机，搞完提交代码，你审核再合并。安全，但他看不到你的本地环境。
- **Claude Code 的做法**：让他直接用你的电脑——但配了一套极其精密的安检系统。他能做什么、不能做什么、哪些操作需要点头、哪些可以自己来，甚至 `rm -rf` 都要经过 9 层审查才能执行。

> [!tip] 为什么 Anthropic 选了最难的那条路？
> 只有这样，AI 才能用**你的终端、你的环境、你的配置**来干活——这才是"真正帮你写代码"，而不是"在一个干净房间里给你写一段代码然后复制过来"。

代价是什么？**他们为此写了 51 万行代码。**

---

## 三、第一个秘密：提示词是"拼装"出来的

大多数人以为 AI 编程工具是这样工作的：

```
用户输入 → 调用 LLM API → 返回结果 → 显示给用户
```

Claude Code 实际是这样的：

```
用户输入
  → 动态组装 7 层系统提示词
  → 注入 Git 状态、项目约定、历史记忆
  → 53+ 个工具各自附带使用手册
  → LLM 决定使用哪个工具
  → 9 层安全审查（AST 解析、ML 分类器、沙箱检查...）
  → 权限竞争解析（本地键盘 / IDE / Hook / AI 分类器 同时竞争）
  → 200ms 防误触延迟
  → 执行工具
  → 结果流式返回
  → 上下文接近极限？→ 三层压缩（微压缩 → 自动压缩 → 完全压缩）
  → 需要并行？→ 生成子 Agent 蜂群
  → 循环直到任务完成
```

### Prompt 的静态/动态分界线

`src/constants/prompts.ts` 中，系统提示词被分为两部分：

```typescript
export async function getSystemPrompt(...): Promise<string[]> {
  return [
    // --- 静态内容（可缓存）---
    getSimpleIntroSection(outputStyleConfig),
    getSimpleSystemSection(),
    getSimpleDoingTasksSection(),
    getActionsSection(),
    getUsingYourToolsSection(enabledTools),
    getSimpleToneAndStyleSection(),
    getOutputEfficiencySection(),

    // === 缓存边界 ===
    ...(shouldUseGlobalCacheScope() ? [SYSTEM_PROMPT_DYNAMIC_BOUNDARY] : []),

    // --- 动态内容（每次不同）---
    ...resolvedDynamicSections,
  ]
}
```

**这叫把提示词当编译器输出来优化：**
- 静态部分 = "编译后的二进制"，走缓存，不重复计费
- 动态部分 = "运行时参数"，注入当前 Git 分支、CLAUDE.md 配置、用户记忆

### 每个 Tool 都有独立的"使用手册"

每个工具目录下有一个 `prompt.ts`——**专门写给 LLM 看的行为准则**。

以 BashTool 为例（约 370 行）：

```
Git Safety Protocol:
- NEVER update the git config
- NEVER run destructive git commands (push --force, reset --hard, checkout .)
  unless the user explicitly requests
- NEVER skip hooks (--no-verify) unless the user explicitly requests
- CRITICAL: Always create NEW commits rather than amending
```

这就是为什么 Claude Code 从不会擅自 `git push --force`——**不是模型更聪明，是提示词里已经把规矩讲清楚了。**

> [!info] 内部版本 vs 外部版本
> 代码里大量出现 `process.env.USER_TYPE === 'ant'` 分支——ant 即 Anthropic 内部员工。他们的版本有更详细的代码风格指引、更激进的输出策略，以及仍在 A/B 测试的实验功能（Verification Agent、Explore & Plan Agent）。**Anthropic 自己就是 Claude Code 最大的用户。**

---

## 四、第二个秘密：53+ 个工具，分门别类

`src/tools.ts` 中工具按类别注册：

| 类别 | 工具数 | 代表工具 |
|------|--------|----------|
| 文件操作 | 6 | FileRead、FileEdit、FileWrite |
| 执行 | 3 | BashTool |
| 搜索与抓取 | 4 | GrepTool、GlobTool、WebFetch、WebSearch |
| Agent & 任务 | 11 | AgentTool、TodoWrite |
| 规划 | 5 | - |
| MCP | 4 | - |
| 系统 | 11 | - |
| 实验性 | 8 | ToolSearchTool 等 |

大部分工具你从未直接见过，因为它们是**延迟加载**的——只有当 LLM 需要时，才通过 `ToolSearchTool` 按需注入。每多一个工具，系统提示词就多一段描述，token 就多花一份钱。

### Fail-Closed 设计

```typescript
const TOOL_DEFAULTS = {
  isEnabled: () => true,
  isConcurrencySafe: (_input?) => false,   // 默认：不安全
  isReadOnly: (_input?) => false,           // 默认：会写入
  isDestructive: (_input?) => false,
}
```

**如果一个工具的作者忘了声明安全属性，系统会假设它是"不安全的、会写入的"。** 宁可过度保守，也不漏掉一个风险。

### "先读后改"的铁律

FileEditTool 会检查你是否已经用 FileReadTool 读过这个文件。**如果没有，直接报错，不让改。** 这就是为什么 Claude Code 不会"凭空写一段代码覆盖你的文件"。

---

## 五、第三个秘密：记忆系统——为什么它能"记住你"

你告诉它"不要在测试中 mock 数据库"，下次对话它就不会再 mock。背后是一个完整的记忆系统。

### 用 AI 来检索记忆

Claude Code 用**另一个 AI**（Claude Sonnet）来决定"哪些记忆和当前对话相关"：

```
你的记忆文件列表
  → Sonnet 快速扫描所有记忆的标题和描述
  → 选出最多 5 个最相关的
  → 把完整内容注入当前对话上下文
```

策略是**精确度优先于召回率**——宁可漏掉一个可能有用的记忆，也不塞进一个不相关的记忆污染上下文。

### KAIROS 模式：夜间"做梦"

> [!example] 最科幻的部分
> 在 KAIROS 模式下，长会话中的记忆存在按日期的追加式日志里。然后有一个 `/dream` 技能在"夜间"（低活跃期）运行，把原始日志**蒸馏**成结构化的主题文件：
> ```
> logs/2026/03/2026-03-30.md  ← 今天的原始日志
>         ↓ /dream 蒸馏
> memory/user_preferences.md  ← 结构化的用户偏好文件
> memory/project_context.md   ← 结构化的项目背景文件
> ```
> **AI 在"睡觉"的时候整理记忆。** 这已经不是工程了，这是仿生学。

---

## 六、第四个秘密：它不是一个 Agent，是一群

当你让 Claude Code 做复杂任务时，它可能悄悄生成了一个**子 Agent**——而且子 Agent 有严格的"自我意识"注入，防止递归生成更多子 Agent：

```
STOP. READ THIS FIRST.

You are a forked worker process. You are NOT the main agent.

RULES (non-negotiable):
1. Do NOT spawn sub-agents; execute directly.
2. Do NOT converse, ask questions, or suggest next steps
3. USE your tools directly: Bash, Read, Write, etc.
4. Keep your report under 500 words.
5. Your response MUST begin with "Scope:". No preamble.
```

**"你是一个工人，不是经理。别想着再雇人，自己干活。"**

### Coordinator 模式：经理模式

在协调器模式下，Claude Code 变成纯粹的任务编排者：

```
Phase 1: Research        → 3 个 worker 并行搜索代码库
Phase 2: Synthesis       → 主 Agent 综合理解所有发现
Phase 3: Implementation  → 2 个 worker 分别修改不同文件
Phase 4: Verification    → 1 个 worker 跑测试
```

> 核心原则：**"Parallelism is your superpower"**——只读任务并行跑，写文件任务按文件分组串行跑（避免冲突）。

### Prompt Cache 的极致优化

为了最大化子 Agent 的缓存命中率，所有 fork 子代理的工具结果都使用相同的占位符文本：

```
'Fork started — processing in background'
```

因为 Claude API 的 prompt cache 是基于**字节级前缀匹配**的。10 个子 Agent 前缀完全一致，只有第一个需要"冷启动"，后面 9 个直接命中缓存。

---

## 七、第五个秘密：三层压缩，让对话"永不超限"

当 token 消耗逼近上下文窗口时，Claude Code 启动三层压缩：

### 第一层：微压缩——最小代价

把旧的工具调用结果（比如"10分钟前读的那个 500 行文件"）替换成 `[Old tool result content cleared]`。提示词和对话主线完全保留。

### 第二层：自动压缩——主动收缩

当 token 消耗接近窗口的 **87%**（窗口大小 - 13,000 buffer）时自动触发。有**熔断器**：连续 3 次压缩失败后停止尝试，避免死循环。

### 第三层：完全压缩——AI 总结

让 AI 对整段对话生成摘要，用摘要替换所有历史消息。生成时有严厉的前置指令：

```
CRITICAL: Respond with TEXT ONLY.
Do NOT call any tools.
Tool calls will be REJECTED and will waste your only turn.
```

**"你的任务是总结，别干别的。"**

压缩后的 token 预算（这些数字不是拍脑袋定的）：
- 文件恢复：50,000 tokens
- 每个文件上限：5,000 tokens
- 技能内容：25,000 tokens

---

## 八、95 个斜杠命令，分五大类

| 类别 | 数量 | 代表命令 |
|------|------|----------|
| 配置与初始化 | 12 | `/init`、`/config` |
| 日常工作流 | 24 | `/commit`、`/review` |
| 代码审查 & Git | 13 | `/pr`、`/diff` |
| 调试与诊断 | 23 | `/debug`、`/doctor` |
| 高级 & 实验性 | 23 | `/ultraplan`、`/dream` |

---

## 九、读完源码，能学到什么

### AI Agent 的 90% 工作量在"AI"之外

51 万行代码里，真正调用 LLM API 的部分可能不到 5%。其余 95% 是：

- **安全检查**（18 个文件只为一个 BashTool）
- **权限系统**（allow/deny/ask/passthrough 四态决策）
- **上下文管理**（三层压缩 + AI 记忆检索）
- **错误恢复**（熔断器、指数退避、Transcript 持久化）
- **多 Agent 协调**（蜂群编排 + 邮箱通信）
- **UI 交互**（389 个 React 组件 + IDE Bridge）
- **性能优化**（prompt cache 稳定性 + 启动时并行预取）

> [!warning] 对 AI Agent 开发者的启示
> 如果你正在做 AI Agent 产品，这才是你真正要解决的问题。**不是模型够不够聪明，是你的脚手架够不够结实。**

### 好的提示词工程是系统工程

不是写一段漂亮的 prompt 就完事了。Claude Code 的提示词是：
- 7 层动态组装
- 每个工具附带独立的使用手册
- 缓存边界精确划分
- 内外部版本有不同的指令集
- 工具排序固定以保持缓存稳定

**这是工程化的提示词管理，不是手工艺。**

### Anthropic 把 Claude Code 当操作系统在做

| 传统 OS 概念 | Claude Code 对应物 |
|-------------|-------------------|
| 系统调用 | 53+ 个工具 |
| 用户权限管理 | 权限系统 |
| 应用商店 | Skills 系统 |
| 设备驱动 | MCP 协议 |
| 进程管理 | Agent 蜂群 |
| 内存管理 | 上下文压缩 |
| 文件系统 | Transcript 持久化 |

---

## 总结

51 万行代码。1,900+ 个文件。18 个安全文件只为一个 Bash 工具。9 层审查只为让 AI 安全地帮你敲一行命令。

**要让 AI 真正有用，你不能把它关在笼子里，也不能放它裸奔。你得给它建一套完整的信任体系。**

而这套信任体系的代价，是 51 万行代码。

---

## 参考来源

- [一文了解 Anthropic 的 Claude Code 源码](https://x.com/YukerX/status/2038959908968919297)
- [Claude Code Unpacked](https://ccunpacked.dev/)

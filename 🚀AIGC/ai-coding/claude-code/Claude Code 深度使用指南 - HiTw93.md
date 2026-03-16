---
title: Claude Code 深度使用指南
source: https://x.com/HiTw93/status/2032091246588518683
author: HiTw93 (Tw93)
tags:
  - claude-code
  - ai-coding
  - agent
  - prompt-engineering
date: 2026-03-13
---

# Claude Code 深度使用指南

> [!abstract] 概览
> 作者半年深度使用 Claude Code 的踩坑经验总结。核心观点：==Claude Code 不是 ChatBot，而是一个多层代理系统==，需要从系统工程角度去治理，而非只调 Prompt。

## 六层架构模型

把 Claude Code 拆成六层来理解，只强化其中一层系统就会失衡：

```
收集上下文 → 采取行动 → 验证结果 → [完成 or 回到收集]
     ↑                    ↓
  CLAUDE.md          Hooks / 权限 / 沙箱
  Skills             Tools / MCP
  Memory
```

> [!tip] 排查思路
> - 结果不稳定 → 查**上下文加载顺序**
> - 自动化失控 → 查**控制层**有没有设计
> - 长会话质量下降 → 中间产物把上下文**污染**了，换新会话比反复调 prompt 有用


| 层 | 职责 |
|---|---|
| CLAUDE.md / rules / memory | 长期上下文，告诉 Claude "是什么" |
| Tools / MCP | 动作能力，告诉 Claude "能做什么" |
| Skills | 按需加载的方法论，告诉 Claude "怎么做" |
| Hooks | 强制执行某些行为，不依赖 Claude 自己判断 |
| Subagents | 隔离上下文的工作者，负责受控自治 |
| Verifiers | 验证闭环，让输出可验、可回滚、可审计 |

简单记：给 Claude 新动作能力用 Tool/MCP，给它一套工作方法用 Skill，需要隔离执行环境用 Subagent，要强制约束和审计用 Hook，跨项目分发用 Plugin。




## 上下文工程（最重要）

### 真实的上下文成本构成

200K 上下文并非全部可用：

```
200K 总上下文
├── 固定开销 (~15-20K)
│   ├── 系统指令: ~2K
│   ├── Skill 描述符: ~1-5K
│   ├── MCP Server 工具定义: ~10-20K  ← 最大隐形杀手
│   └── LSP 状态: ~2-5K
├── 半固定 (~5-10K)
│   ├── CLAUDE.md: ~2-5K
│   └── Memory: ~1-2K
└── 动态可用 (~160-180K)
```

> [!warning] MCP 的隐形成本
> 一个典型 MCP Server 含 20-30 个工具定义，每个 ~200 tokens。接 5 个 Server，固定开销就达 **25,000 tokens（12.5%）**。

### 推荐的上下文分层

| 策略 | 内容 |
|---|---|
| 始终常驻 | CLAUDE.md：项目契约 / 构建命令 / 禁止事项 |
| 按路径加载 | rules：语言 / 目录 / 文件类型规则 |
| 按需加载 | Skills：工作流 / 领域知识 |
| 隔离加载 | Subagents：大量探索 / 并行研究 |
| 不进上下文 | Hooks：确定性脚本 / 审计 / 阻断 |

### 上下文最佳实践

- CLAUDE.md 保持**短、硬、可执行**（Anthropic 官方约 2.5K tokens）
- 大型参考文档拆到 Skills 的 supporting files
- 用 `.claude/rules/` 做路径/语言规则
- 任务切换优先 `/clear`，同一任务进入新阶段用 `/compact`
- ==把 Compact Instructions 写进 CLAUDE.md==，控制压缩后保留什么

### 压缩机制的陷阱与对策

默认压缩算法会把早期 Tool Output 和文件内容优先删掉，连带丢失**架构决策和约束理由**。

**对策一**：在 CLAUDE.md 中写明 Compact Instructions：

```markdown
## Compact Instructions
When compressing, preserve in priority order:
1. Architecture decisions (NEVER summarize)
2. Modified files and their key changes
3. Current verification status (pass/fail)
4. Open TODOs and rollback notes
```

**对策二**：开新会话前让 Claude 写 **HANDOFF.md**，记录进度、尝试过什么、什么有效、下一步该做什么。

### Plan Mode 的工程价值

把探索和执行拆开，探索阶段不动文件，确认方案后再执行。

> [!tip] 进阶玩法
> 开一个 Claude 写计划，再开一个 Codex 以"高级工程师"身份审这个计划，==让 AI 审 AI==。

## Skills 设计

Skill 不是模板库，是**按需加载的工作流**。描述符常驻上下文，完整内容按需加载。

### 好 Skill 的标准

- 描述要让模型知道"**何时**该用我"，而不是"我是干什么的"
- 有完整步骤、输入、输出和**停止条件**
- 正文只放导航和核心约束，大资料拆到 supporting files
- 有副作用的 Skill 设置 `disable-model-invocation: true`

### 三种典型类型

1. **检查清单型**（质量门禁）— 如 release-check
```yaml
---
name: release-check
description: Use before cutting a release to verify build, version, and smoke test.
---

## Pre-flight (All must pass)
- [ ] `cargo build --release` passes
- [ ] `cargo clippy -- -D warnings` clean
- [ ] Version bumped in Cargo.toml
- [ ] CHANGELOG updated
- [ ] `kaku doctor` passes on clean env

## Output
Pass / Fail per item. Any Fail must be fixed before release.
```

2. **工作流型**（标准化操作）— 如 config-migration，内置回滚步骤
```yaml
---
name: config-migration
description: Migrate config schema. Run only when explicitly requested.
disable-model-invocation: true
---

## Steps
1. Backup: `cp ~/.config/kaku/config.toml ~/.config/kaku/config.toml.bak`
2. Dry run: `kaku config migrate --dry-run`
3. Apply: remove `--dry-run` after confirming output
4. Verify: `kaku doctor` all pass

## Rollback
`cp ~/.config/kaku/config.toml.bak ~/.config/kaku/config.toml`
```

3. **领域专家型**（封装决策框架）— 如 runtime-diagnosis
```yaml
---
name: runtime-diagnosis
description: Use when kaku crashes, hangs, or behaves unexpectedly at runtime.
---

## Evidence Collection
1. Run `kaku doctor` and capture full output
2. Last 50 lines of `~/.local/share/kaku/logs/`
3. Plugin state: `kaku --list-plugins`

## Decision Matrix
| Symptom | First Check |
|---|---|
| Crash on startup | doctor output → Lua syntax error |
| Rendering glitch | GPU backend / terminal capability |
| Config not applied | Config path + schema version |

## Output Format
Root cause / Blast radius / Fix steps / Verification command
```


### 描述符优化
描述符写短点，每个 Skill 都在偷你的上下文空间，每个启用的 Skill，描述符常驻上下文，优化前后差距很大：

```yaml
# 低效（~45 tokens）
description: |
  This skill helps you review code changes in Rust projects.
  It checks for common issues like unsafe code, error handling...
  Use this when you want to ensure code quality before merging.

# 高效（~9 tokens）
description: Use for PR reviews with focus on correctness.
```

### auto-invoke 策略

| 频率 | 策略 |
|---|---|
| 高频（>1 次/会话） | 保持 auto-invoke，优化描述符 |
| 低频（<1 次/会话） | disable-auto-invoke，手动触发 |
| 极低频（<1 次/月） | 移除 Skill，改为文档 |





## 工具设计原则

- 名称前缀按系统分层：`github_pr_*`、`jira_issue_*`
- 错误响应要**教模型如何修正**，不要只抛 error code
- 能合并成高层任务工具时，不要暴露过多底层碎片工具

> [!example] AskUserQuestion 工具的演进教训
> 第一版加参数 → Claude 忽略；第二版约定 markdown 格式 → Claude 经常忘；第三版做成**独立工具** → 效果显著。
> 教训：==需要 Claude 停下来做一件事，就给它一个专门的工具==。

## Hooks 设计

Hooks 是把不能交给 Claude 临场发挥的事情，收回到**确定性流程**。

### 适合 vs 不适合

| ✅ 适合 | ❌ 不适合 |
|---|---|
| 阻断修改受保护文件 | 复杂语义判断 |
| Edit 后自动格式化/lint | 长时间运行的业务流程 |
| SessionStart 注入动态上下文 | 多步推理和权衡的决策 |
| 任务完成后推送通知 | |

### 三层叠加

- **CLAUDE.md**：声明规则（"提交前必须通过测试"）
- **Skill**：告诉 Claude 操作顺序和修复方法
- **Hook**：关键路径硬性校验，必要时阻断

> [!important]
> 三层少任何一层都有漏洞。只写 CLAUDE.md 规则，Claude 经常当没看见。

## Subagents 使用

核心价值不是"并行"，而是**隔离**。大量输出的事交给 Subagent，主线程只拿摘要。
> Subagent 就是从主对话派出去的一个独立 Claude 实例，有自己的上下文窗口、只用你指定的工具、干完汇报结果。核心价值不是"并行"，而是隔离，扫代码库、跑测试、做审查这类会产生大量输出的事，交给 Subagent 做，主线程只拿摘要，不会被中间过程污染。Claude Code 内置了 Explore（只读扫库，跑 Haiku 省成本）、Plan（规划调研）、General-purpose（通用），也可以自定义。



### 配置要点

- `tools / disallowedTools`：限定工具权限
- `model`：探索用 Haiku/Sonnet，审查用 Opus
- `maxTurns`：防止跑飞
- `isolation: worktree`：需要动文件时隔离文件系统

### 反模式

- 子代理权限和主线程一样宽
- 输出格式不固定，主线程拿到没法用
- 子任务之间强依赖，频繁共享中间状态

## Prompt Caching 架构

> [!quote]
> "Cache Rules Everything Around Me" — 对 agent 同样如此。

### 关键设计

- Prompt 按前缀匹配缓存，**顺序很重要**：System Prompt → Tool Definitions → Chat History → 当前输入
- 动态信息（如时间戳）放到用户消息的 `<system-reminder>` 里，不要动系统 Prompt
- ==会话中途不要切换模型==（缓存模型唯一，切换会重建缓存，反而更贵）
- Plan Mode 实现为工具调用（不改工具集），避免破坏缓存
- 工具延迟加载（`defer_loading`）：先发 stub，模型通过 ToolSearch 按需加载完整 schema
	- Claude Code 有数十个 MCP 工具，每次请求全量包含会很贵，但中途移除会破坏缓存


## 验证闭环

> [!important]
> 如果一个任务你说不清楚"什么叫做完"，那大概率也不适合直接扔给 Claude 自主完成。

**Verifier 层级**：
1. 最低层：命令退出码、lint、typecheck、unit test
2. 中间层：集成测试、截图对比、contract test
3. 更高层：生产日志验证、监控指标、人工审查

## 高频命令速查

### 上下文管理

| 命令 | 用途 |
|---|---|
| `/context` | 查看 token 占用结构 |
| `/clear` | 清空会话（被纠偏两次以上就重来） |
| `/compact` | 压缩但保留重点 |
| `/memory` | 确认哪些 CLAUDE.md 被加载 |

### 能力与治理

| 命令 | 用途 |
|---|---|
| `/mcp` | 管理 MCP 连接，检查 token 成本 |
| `/hooks` | 管理 hooks |
| `/permissions` | 查看或更新权限白名单 |
| `/model` | 切换模型 |

### 实用技巧

- **`/simplify`**：对刚改完的代码做三维检查（复用、质量、效率）
- **`/rewind`**：回到某个会话 checkpoint 重新总结
- **`/btw`**：不打断主任务快速问侧问题
- **`/insight`**：分析当前会话，提炼值得沉淀到 CLAUDE.md 的内容
- **双击 ESC**：回到上一条输入重新编辑
- **Ctrl+B**：把长时间运行的 bash 命令移到后台

## CLAUDE.md 写法

### 应该放

- 怎么 build、test、run（最核心）
- 关键目录结构与模块边界
- 代码风格和命名约束
- 绝对不能干的事（NEVER 列表）
- Compact Instructions

### 不该放

- 大段背景介绍、完整 API 文档
- 空泛原则（如"写高质量代码"）
- Claude 读仓库即可推断的信息
- 大量低频任务知识（放到 Skills）

> [!tip] 让 Claude 维护自己的 CLAUDE.md
> 每次纠正 Claude 错误后：*"Update your CLAUDE.md so you don't make that mistake again."*

一开始甚至可以什么都不写。先用起来，等你发现自己老是在重复同一件事，再把它补进去。加法也不复杂，输入 # 可以把当前对话里的内容直接追加进 CLAUDE.md，或者直接告诉 Claude「把这条加到项目的 CLAUDE.md 里」，它会知道该改哪个文件。

每次都要知道的放 CLAUDE.md，只对部分文件生效的放 rules，只在某类任务中需要的放 Skills。


### **高质量模板**

```markdown
# Project Contract

## Build And Test

- Install: `pnpm install`
- Dev: `pnpm dev`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`
- Lint: `pnpm lint`

## Architecture Boundaries

- HTTP handlers live in `src/http/handlers/`
- Domain logic lives in `src/domain/`
- Do not put persistence logic in handlers
- Shared types live in `src/contracts/`

## Coding Conventions

- Prefer pure functions in domain layer
- Do not introduce new global state without explicit justification
- Reuse existing error types from `src/errors/`

## Safety Rails

## NEVER

- Modify `.env`, lockfiles, or CI secrets without explicit approval
- Remove feature flags without searching all call sites
- Commit without running tests

## ALWAYS

- Show diff before committing
- Update CHANGELOG for user-facing changes

## Verification

- Backend changes: `make test` + `make lint`
- API changes: update contract tests under `tests/contracts/`
- UI changes: capture before/after screenshots

## Compact Instructions

Preserve:

1. Architecture decisions (NEVER summarize)
2. Modified files and key changes
3. Current verification status (pass/fail commands)
4. Open risks, TODOs, rollback notes
```


### 常见反模式

| 反模式 | 症状 | 修复 |
|--------|------|------|
| CLAUDE.md 当 wiki | 每次加载污染上下文，关键指令被稀释 | 只保留契约，资料拆到 Skills 和 rules |
| Skill 大杂烩 | 描述无法稳定触发，工作流冲突 | 一个 Skill 只做一类事，副作用显式控制 |
| 工具太多描述模糊 | 选错工具，schema 挤爆上下文 | 合并重叠工具，做明确 namespacing |
| 没有验证闭环 | Claude 只能"觉得自己完成了" | 给每类任务绑定 verifier |
| 过度自治 | 多 agent 并行无边界，出错难止损 | 角色/权限/worktree 最小化，明确 maxTurns |
| 上下文不做切分 | 研究、实现、审查全堆在主线程，有效上下文被稀释 | 任务切换 `/clear`，阶段切换 `/compact`，重型探索交给 subagent（Explore → Main 模式） |
| 自治范围过宽但治理不足 | 多 agent、外部工具全开，但缺乏权限边界和结果回收边界 | `permissions` + `sandbox` + `hooks` + subagent 组合边界 |
| 已批准命令堆积不清理 | `settings.json` 里残留 `rm -rf` 等危险操作，一旦触发不可逆 | 定期审查 `.claude/settings.json` 的 `allowedTools` 列表 |






## 工程化布局参考

```
Project/
├── CLAUDE.md
├── .claude/
│   ├── rules/
│   │   ├── core.md
│   │   ├── config.md
│   │   └── release.md
│   ├── skills/
│   │   ├── runtime-diagnosis/     # 统一收集日志、状态和依赖
│   │   ├── config-migration/      # 配置迁移回滚防污
│   │   ├── release-check/         # 发布前校验、smoke test
│   │   └── incident-triage/       # 线上故障分诊
│   ├── agents/
│   │   ├── reviewer.md
│   │   └── explorer.md
│   └── settings.json
└── docs/
    └── ai/
        ├── architecture.md
        └── release-runbook.md
```

## 配置健康检查

作者开源了 [claude-health](https://github.com/tw93/claude-health) Skill，可一键检查 Claude Code 配置状态：

```bash
npx skills add tw93/claude-health
# 然后在会话中运行 /health
```

装好之后在任意会话里跑 /health，它会自动识别项目复杂度，对 CLAUDE.md、rules、skills、hooks、allowedTools 和实际行为模式各跑一遍检查，输出一份优先级报告：需要立刻修 / 结构性问题 / 可以慢慢做。


---

> [!quote] 三个阶段
> 用 Claude Code 会经历三个阶段：从"这个功能怎么用" → 到"怎么让 agent 在约束下自己跑起来"，两件事感觉差很多。

---
title: bgclick-rev（深度逆向 Skill 范例）
tags: [agent-skills, reverse-engineering, sub-agent]
date: 2026-05-09
sources:
  - "[[sources/clippings/bgclick-rev-skillbgclick-rev-skill.md at main]]"
last-ingested: 2026-05-09
status: stable
---

`bgclick-rev` 是 Lakr233 公开的一个 macOS 闭源 GUI 自动化逆向 Skill：把"对一个会在后台点窗口的闭源 app 做 1:1 复刻"这件事拆成 8 个有 checkpoint 的 phase，每个 phase 派 sub-agent 并固定写出 `research/` 下的研究档。它是 [[wiki/skills/skills-9-分类|Skills 9 大分类]] 之外的一种"深度研究型 Skill"模板，可作为任何长链条逆向/审计任务的参考骨架。

> [!note] 前置门槛被写进 description
> Skill 自己的 description 里就声明：「**Prerequisite — IDA Pro with IDA MCP attached; skip politely if the user has no IDA**」。这是 [[wiki/skills/skill-编写实践|Skill 编写实践]]里的一条隐含规则——**门槛要写在 description 里，让模型在触发前就能 short-circuit**，而不是跑到 Phase 1 才发现工具不在。

## 8 phase 的 checkpoint 形态

Skill 把"逆向 + 复刻"切成 8 个 phase，每个 phase 都有明确的"必须先写完哪几个文件才能进下一个 phase"。这与 [[wiki/agent-engineering/workflow/sprint-七阶段范式|Sprint 七阶段范式]]同属"phased + 强制工件"的家族，差异在于：sprint 是开发流程，bgclick-rev 是研究流程，工件类型不一样。

> [!example] 8 phase 概览
> | # | 名字 | 产物 |
> |---|---|---|
> | 0 | Workspace + target triage | `SHARED-CONTEXT.md`（briefing 给所有 sub-agent 读） |
> | 1 | CG/AX call-site audit | `research/findings/phase1-call-site-map.md` |
> | 2 | Async continuation chain | `research/sub_<addr>-*.md` × N + `research/frame-map.md` |
> | 3 | dyld-hash 解析器 | `research/sub_<addr>-<symbolname>.md` × 7（并行） |
> | 4 | CGEvent field 映射 | `research/findings/cgevent-fields.md` |
> | 5 | Open-question hunt | `research/findings/Q<N>-<slug>.md`（每问一文件，并行） |
> | 6 | Swift 复刻 | `Sources/<Module>/BackgroundClicker.swift` |
> | 7 | VM 测试台 + 经验日志 | `EchoApp/main.swift` + `impl-research.md` |
> | 8 | FINAL-REPORT | `research/FINAL-REPORT.md`（行为 spec + 证据表 + 复刻 diff） |

每个 phase 不是"建议"而是 checkpoint——**没有写出 phase 产物就不能进下一个 phase**。这强制了"先有证据再前进"的纪律，与 [[wiki/agent-engineering/workflow/验证驱动|验证驱动]]同构。

## 把"先验"写在 Skill 正文里

最有意思的一段是 §"Invariant background facts (treat as ground truth, verify against target)"——Skill 直接给了 9 条"这类 app 通常做了什么"的先验断言（比如"posting mechanism 一定是 `CGEvent.postToPid` 经 dyld-hash 解析"、"flags trick 用的是 `0x100000` Command 而不是常被搞混的 `0x100` NonCoalesced"）。Skill 明确说："**Use these as priors when auditing. Verify each one against the target binary before relying on it.**"

> [!important] 先验不是答案，是 hypothesis 列表
> 这种写法把"领域 know-how"压缩成可被逐条 falsify 的列表，让 sub-agent 每条都要对着目标二进制验证。它和 [[wiki/agent-engineering/workflow/enforce-invariants|Enforce Invariants, Not Implementations]]互补：后者讲测试中的不变量，这里讲**研究中的认知先验**——先把"我以为对"的东西写下来，再去打它。

## Sub-agent 纪律的 5 条铁律

Skill 的 §"Sub-agent discipline" 段是任意复杂多 sub-agent skill 都可以直接抄的范本。详见 [[wiki/agent-engineering/workflow/sub-agent-纪律|Sub-agent 纪律]]，这里只列骨架：

1. 第一动作必须是读 `SHARED-CONTEXT.md`
2. 一个 sub-agent 只拥有一个 question 或一个 function
3. 一个 sub-agent 只产出一个文件
4. 输出文件第一行就是 verdict，证据放后面
5. sub-agent 不改源码，只写研究档

这是 [[wiki/agent-engineering/workflow/subagent-driven-development|Subagent-Driven Development]]的"研究版"——不是"每个 plan task 派一个 sub-agent"，而是"每个 question 派一个 sub-agent"。

## Known failure modes 是信息密度最高的章节

Skill 末尾的 §"Known failure modes" 列了 4 条具体的认知陷阱（如"误判 `0x100000` 是 NonCoalesced，其实是 Command"、"误把 Swift `Array.append` specialization 当成事件 poster"）。这印证了 [[wiki/skills/skill-编写实践|Skill 编写实践]]里的一条："踩坑点章节是信息密度最高的部分"——把模型最容易踏的坑显式列出来，比写一堆"how to"更有效。

## 与本 wiki 其他概念的连接

> [!compare] bgclick-rev 命中的几条范式
> | 范式 | 命中点 |
> |---|---|
> | [[wiki/skills/agent-skills\|Agent Skills 规范]] | 标准 skill.md + description |
> | [[wiki/agent-engineering/workflow/sub-agent-纪律\|Sub-agent 纪律]] | 5 条铁律源出处 |
> | [[wiki/agent-engineering/workflow/subagent-driven-development\|Subagent-Driven Development]] | 每 question / 每 function 派一个 |
> | [[wiki/agent-engineering/workflow/coordinator-模式\|Coordinator 模式]] | Phase 3、Phase 5 并行 sub-agent |
> | [[wiki/agent-engineering/workflow/验证驱动\|验证驱动]] | phase checkpoint = 写完证据才能前进 |
> | [[wiki/claude-code/mcp\|MCP]] | IDA MCP 作为 hard prerequisite |

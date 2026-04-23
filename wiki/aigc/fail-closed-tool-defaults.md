---
title: Fail-Closed 工具默认
tags: [claude-code, security, tool-design]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code 源码深度解析：51万行代码背后的秘密]]"
last-ingested: 2026-04-23
status: stable
---

[[claude-code|Claude Code]] 内部 53+ 个工具在注册时统一应用一套**保守默认**——任何工具如果作者忘了显式声明安全属性，系统**假设它是不安全的**。这是 Fail-Closed（默认拒绝）原则在 Agent 工具系统里的具体落地。

> [!example] 源码里的默认值
> ```typescript
> const TOOL_DEFAULTS = {
>   isEnabled: () => true,
>   isConcurrencySafe: (_input?) => false,   // 默认：不能并发
>   isReadOnly: (_input?) => false,           // 默认：会写入
>   isDestructive: (_input?) => false,        // 注：destructive 默认 false 是为了不让"未知工具"自动叠加额外审查，但 read-only/concurrency 默认收紧
> }
> ```

> [!important] 为什么 Read-Only 默认 false 是对的
> 直觉上似乎应该默认 `isReadOnly: true`（"无害推定"）。但 Claude Code 选了反向——因为 read-only 标记直接影响**并发调度**和**权限审查**。如果一个会写文件的工具被错标为 read-only，它会和其他工具并发执行，可能造成竞态。**宁可让"真正只读的工具"忘标声明而损失一次并发优化，也不能让"会写入的工具"漏标声明而引发数据损坏**。

**Fail-Closed 的三个层级**

Claude Code 的工具系统在三层做 Fail-Closed：

| 层 | 默认 | 失误的代价 |
|---|---|---|
| **工具属性声明** | 全 false | 漏标 = 走最严格的执行路径（慢但安全） |
| **权限决策** | ask 或 deny | 漏配 = 用户被多问一次（烦但安全） |
| **沙箱配置** | 启用 | 漏配 = 工具不能跑（明显错误，立即修） |

**与 [[wiki/ai-coding/enforce-invariants|Enforce Invariants]] 的关系**：Fail-Closed 是"在边界处强制不变量"的具体技巧——把"工具默认是危险的"作为系统不变量，让任何新工具**必须显式声明自己是安全的**才能享受优化路径。这与 [[hooks|Hooks]] 的"必须每次都执行"是一类思路。

> [!tip] 写自定义工具时学这个习惯
> 如果你给 Claude Code 写自定义工具（或写自己的 Agent 工具系统）：**所有"宽松属性"必须显式声明**，不要依赖默认。即使工具的代码很简单，下次重构时这种显式声明能救你——它把"是否安全"变成 review 时必查的字段，而不是"看代码自己判断"。

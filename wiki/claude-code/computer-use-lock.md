---
title: Computer Use 跨进程文件锁（O_EXCL）
tags: [computer-use, claude-code, concurrency]
date: 2026-05-16
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/cc-haha-computer-use]]"
last-ingested: 2026-05-16
status: draft
---

Claude Code 的 Computer Use 模块用一个文件锁保证多个会话不会并发操控同一台机器：`~/.claude/computer-use.lock`。实现核心是 Node.js 的 `O_EXCL` 标志——原子的 test-and-set，无需额外锁原语。

> [!note] 锁的内容
> ```typescript
> { sessionId: string, pid: number, acquiredAt: number }
> ```

## 获锁流程

```
1. writeFile(lockPath, data, { flag: 'wx' })
   ├─ 成功 → fresh acquire，拿到锁
   └─ 失败（文件已存在）→ 读出锁内容
        ├─ 同 sessionId → reentrant，继续
        ├─ 不同 sessionId + PID 存活（process.kill(pid, 0) 不报错）→ blocked
        └─ 不同 sessionId + PID 已死 → stale 锁，unlink 后重试 O_EXCL
```

**`{ flag: 'wx' }` = POSIX `O_WRONLY | O_CREAT | O_EXCL`**：创建文件时若已存在则立即报错，不会覆盖。这是跨进程互斥的正确做法——没有 check-then-set 的竞争窗口。

## 两种检查接口

| 接口 | 用途 | 行为 |
|---|---|---|
| `acquireCuLock` | 进入 Computer Use 模式时调用 | 真正尝试获取锁 |
| `checkComputerUseLock` | `request_access` / `list_granted_applications` 等只读工具 | 只检查，不获取锁，避免触发 CU 模式通知 |

`isLockHeldLocally()` 是零系统调用的进程内标记，让非 CU turn 不触碰磁盘。

## Stale 检测的已知局限

> [!warning] PID 复用窗口
> stale 检测基于"老 PID 已不存活"：owner 进程死亡的同时，如果有新进程恰好分配到同一 PID，stale 检测会误判为"锁仍有效"。这是已知的小窗口，注释里承认"极不可能"发生。
>
> 不用 `fcntl advisory lock` 的原因：需要保留跨进程感知能力（读 `pid` 字段后仍能确认是哪个会话持有锁）。

## 释放时机

每次 Computer Use turn 结束（自然结束 / abort streaming / abort tools 三个入口）统一走 `cleanup.ts`：

1. 把 `prepareForAction` hide 的 app 重新 unhide（5 秒超时）
2. 释放 `computerUseLock`
3. 发 OS 通知"Claude is done using your computer"

注册了 `cleanupRegistry` 兜底，确保进程意外退出时也能释放锁。

## 通用性

这套模式适用于任何"多进程竞争单资源"的场景：
- 用 `O_EXCL` 创建锁文件做原子互斥
- 锁内存储持有者标识（sessionId / pid）
- PID 探活（`process.kill(pid, 0)` 不抛 = 进程存在）做 stale 检测
- 注册进程退出钩子做兜底释放

## 相关页面

- [[computer-use-架构|Computer Use 架构与 MCP 借壳模式]]
- [[cc-haha|cc-haha 项目概述]]
- [[agent-engineering/workflow/agent-loop|Agent Loop]] — Lock 在 loop 每轮开始时检查

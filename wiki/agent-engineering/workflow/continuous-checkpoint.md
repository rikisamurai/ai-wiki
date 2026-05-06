---
title: Continuous Checkpoint Mode（WIP commit + 上下文恢复）
tags: [workflow, checkpoint, git]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: draft
---

[[gstack]] 的可选模式：agent 在干活过程中**自动 git commit** 中间状态——commit message 用 `WIP:` 前缀 + 结构化的 `[gstack-context]` body（含决策、剩余工作、失败过的方案）。会话崩溃 / context 切换后用 `/context-restore` 读回这些 commit 重建状态。`/ship` 在 PR 前自动 filter-squash 掉 WIP commit，保留正式 commit 让 bisect 干净。

## 解决什么问题

> [!important] Long-horizon agent 最大的不可恢复损失
> 跑一个 [[long-horizon-agent|长时任务]] 30 分钟后突然崩了——没 checkpoint 时丢的不只是代码（git stash 救得回），而是 agent 头脑里 **"我已经试过 X 失败了、现在准备试 Y"** 的隐式状态。重启后 agent 不知道 X 不行，会再试一遍。
>
> Continuous Checkpoint 把这块隐式状态硬 commit 到 git——下一会话读 commit message 就能 catch up。

## WIP commit 的结构化 body

> [!example] commit message 长这样
> ```
> WIP: 实现 user notification settings 的 toggle
>
> [gstack-context]
> Decisions:
> - 用 react-hook-form 管理状态（已确认 mvp 范围）
> - settings 持久化到 localStorage 不接 backend（feedback 后续再加）
>
> Remaining work:
> - 写 onSubmit 调用 mutation
> - 加 toast 反馈
> - 写 e2e 测试
>
> Failed approaches:
> - 试过用 useReducer 自管状态，但和 react-hook-form 重复，弃
> - 试过把 toast 放 layout level，但权限太大，回退到组件 level
> ```

`/context-restore` 解析 `[gstack-context]` 段落，把"已做的决策 / 剩余工作 / 失败过的方案"重新喂给新会话的 system prompt。

## /ship 的 filter-squash

> [!tip] WIP commit 不上 PR
> 启用 continuous checkpoint 后会出现大量 WIP commit。`/ship` 在打 PR 前**自动 filter-squash**：
> - 保留所有非 WIP commit（你手工写的那些）
> - 把 WIP commit 压成单个 squash commit（或全部丢弃，按配置）
>
> 结果：bisect 仍然能精确定位回归 commit；review 看到的 PR 是干净的，不被 WIP 噪声淹没。

## 默认 local，push 是 opt-in

> [!warning] 别让 WIP commit 触发 CI
> 默认 `checkpoint_push=false`——只 commit 到本地不 push。否则每个 WIP commit 都会触发 CI，浪费 runner、被同事看到中间状态。
>
> opt-in `checkpoint_push=true` 适用场景：
> - 跑长时无人值守任务，担心机器死机要换台机器接手
> - 多人协作同一分支（罕见）

## 与其他状态恢复方式的对比

> [!compare] 三种"agent 状态恢复"
> | 机制 | 单元 | 持久化层 |
> |---|---|---|
> | **Continuous Checkpoint** | git commit message | `.git/` |
> | **[[handoff-md\|HANDOFF.md]]** | 显式 markdown 文件 | repo 根目录 |
> | **[[wiki/claude-code/auto-memory\|Auto Memory]]** | per-project memory file | `.claude/` |
>
> 三者非互斥：
> - HANDOFF.md 适合**会话边界明确**的交接（"我下班了，明天继续"）
> - Auto Memory 适合**跨项目偏好**（"我喜欢 tabs 不喜欢 spaces"）
> - Continuous Checkpoint 适合**会话内崩溃保护 + 长任务暂停**

## 与 [[rewind-胜过纠正|Rewind 胜过纠正]] 的协同

WIP commit 给 rewind 提供细粒度回退点。Agent 走错方向时，可以 `git reset --hard <某个 WIP commit>` 回到分叉前——比手工 stash 精确得多，因为每个 WIP 都带 context 说"那时我在想什么"。

## 配置

> [!example] 启用方式
> ```bash
> gstack-config set checkpoint_mode continuous
> # 默认本地不 push
> gstack-config set checkpoint_push true   # 可选，触发 CI
> ```
>
> 关闭：`gstack-config set checkpoint_mode off`。

## 关联

- 工具栈：[[gstack]]
- 同类持久化：[[handoff-md]]、[[wiki/claude-code/auto-memory|Auto Memory]]、[[kairos-记忆蒸馏]]
- 长任务保护：[[long-horizon-agent]]
- 回退场景：[[rewind-胜过纠正]]

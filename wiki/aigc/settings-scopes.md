---
title: Claude Code Settings Scopes
tags: [claude-code, configuration, settings]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/💡claude-tips]]"
last-ingested: 2026-04-23
status: stable
---

Claude Code 的设置（settings、subagents、MCP server、plugins、[[claude-code-memory|CLAUDE.md]]）按**作用域分层**存储。理解这个层级才能想清楚一条规则该写在哪——团队共享还是个人本地，跨项目还是只对当前仓库生效。

> [!compare] 5 个作用域，谁优先级高？
> | 作用域 | 位置 | 影响谁 | 是否共享 |
> |---|---|---|---|
> | **Managed** | 系统级 `managed-settings.json` / plist / registry | 整台机器上所有用户 | 是（IT 部署） |
> | **CLI 参数** | 临时传入 | 当前会话 | 否 |
> | **Local** | `.claude/settings.local.json`（gitignore） | 你 + 当前仓库 | 否 |
> | **Project** | `.claude/settings.json`（git 跟踪） | 仓库所有协作者 | 是（commit） |
> | **User** | `~/.claude/settings.json` | 你 + 所有项目 | 否 |
>
> 优先级从高到低：**Managed → CLI → Local → Project → User**。冲突时更具体的覆盖更宽泛的——例如 user 允许的工具，project 禁用就被禁。

> [!important] 同一类资源在 5 个作用域的存放位置
> | 资源 | User | Project | Local |
> |---|---|---|---|
> | **Settings** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
> | **Subagents** | `~/.claude/agents/` | `.claude/agents/` | — |
> | **MCP servers** | `~/.claude.json` | `.mcp.json` | `~/.claude.json`（按项目） |
> | **Plugins** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
> | **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` 或 `.claude/CLAUDE.md` | `CLAUDE.local.md` |
>
> Subagents 没有 local 层（不区分"我自己用 vs 团队共享"——要么个人级要么项目级）；MCP 和 Plugins 三层齐全。

> [!tip] 决策树：这条配置写在哪
> - 队友也要遵守，且不含密钥 → **Project**（commit 进 git）
> - 只有你自己临时调试 → **Local**（gitignored）
> - 跨所有项目都要 → **User**
> - 公司统一管控（如禁用某些工具） → **Managed**
> - 单次会话试一下 → **CLI 参数**
>
> 经验：[[wiki/aigc/auto-memory|Auto Memory]] 的位置就是 user 级（`~/.claude/projects/...`）——属于"个人本地、不跨机器"的典型；[[claude-code-memory|CLAUDE.md]] 默认放 project 级，是团队共享约定的载体。

> [!warning] Local 文件的常见误用
> `.claude/settings.local.json` 必须在 `.gitignore` 里，否则把 API key 或个人偏好 commit 出去——这条 Claude Code 不会替你检查。新仓库初始化时**第一件事**就是确认 `.gitignore` 已经包含 `.claude/settings.local.json` 和 `CLAUDE.local.md`。

**与 [[wiki/aigc/permission-modes|权限模式]] 的关系**：权限模式（YOLO/Safe/Plan）是一次会话内的全局开关，可以通过 CLI 参数 `--dangerously-skip-permissions` 或 `--allowedTools "Edit,Write"` 临时设定；持久化的权限策略（哪些命令永远禁、哪些永远允许）则写在 settings.json 里——选哪个 scope 取决于这条规则该影响谁。

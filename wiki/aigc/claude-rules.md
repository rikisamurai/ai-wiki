---
title: .claude/rules/ 规则系统
tags: [claude-code, rules, modular]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/claude-code/blog/Claude Code Memory 机制详解]]"
last-ingested: 2026-04-22
status: stable
---

`.claude/rules/` 是把 [[claude-code-memory|CLAUDE.md]] 拆成多个**模块化规则文件**的目录约定，便于团队维护。每条规则可以用 YAML frontmatter 的 `paths` 字段限定到特定文件 glob，只在相关文件被处理时按需加载，避免常驻上下文。

> [!example] 典型结构
> ```
> .claude/
> ├── CLAUDE.md
> └── rules/
>     ├── code-style.md    # 代码风格
>     ├── testing.md       # 测试约定
>     └── security.md      # 安全要求
> ```

**路径限定（path-scoped rule）**

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
```

只有 Claude 处理 `src/api/**/*.ts` 下的文件时，这条规则才会被加载。常用 glob：

| 模式 | 匹配 |
|---|---|
| `**/*.ts` | 任意目录下的 TypeScript 文件 |
| `src/**/*` | `src/` 下所有文件 |
| `src/components/*.tsx` | 指定目录下的 React 组件 |

> [!tip] 跨项目共享规则
> 用符号链接把公司 / 团队层面的规则库挂进每个项目：
> ```bash
> ln -s ~/shared-claude-rules .claude/rules/shared
> ln -s ~/company-standards/security.md .claude/rules/security.md
> ```
> 规则的真实存放位置在 home 目录，多个项目共享同一份；更新一处，所有项目同步。

**和 [[渐进式披露]] 的关系**：`.claude/rules/` 是 CLAUDE.md 的"目录索引下沉"——CLAUDE.md 只放跨域通用指令，特定文件类型的规范下沉到 `rules/`，按 path 触发。这与 [[skill-编写实践|Skill 的 references/ 下沉]]、[[agents-md|AGENTS.md 的 docs/ 下沉]] 是同一种工程范式：**让上下文按需加载，而不是常驻**。

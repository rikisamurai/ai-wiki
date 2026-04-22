---
title: Skills 9 大分类
tags: [agent-skills, taxonomy, claude-code]
date: 2026-04-22
sources:
  - "[[sources/posts/aigc/ai-coding/blog/🛠️ 构建 Claude Code 的经验：如何使用 Skills]]"
last-ingested: 2026-04-22
status: draft
---

Anthropic 内部活跃使用的 [[agent-skills|Skills]] 已达几百个。Claude Code 团队梳理后发现它们大致归为 9 个反复出现的类别。**好的 Skills 清晰地落在某一个类别里；让人困惑的 Skills 往往横跨了好几个**——这条经验法则可以用来反向自检自己写的 Skill 是否过于"什么都想干"。

> [!compare] 9 类 + 典型实例
> | # | 类别 | 典型 Skills |
> |---|---|---|
> | 1 | 库与 API 参考 | `billing-lib`、`internal-platform-cli`、`frontend-design` |
> | 2 | 产品验证 | `signup-flow-driver`、`checkout-verifier`、`tmux-cli-driver` |
> | 3 | 数据获取与分析 | `funnel-query`、`cohort-compare`、`grafana` |
> | 4 | 业务流程与团队自动化 | `standup-post`、`create-ticket`、`weekly-recap` |
> | 5 | 代码脚手架与模板 | `new-<framework>-workflow`、`new-migration`、`create-app` |
> | 6 | 代码质量与审查 | `adversarial-review`、`code-style`、`testing-practices` |
> | 7 | CI/CD 与部署 | `babysit-pr`、`deploy-<service>`、`cherry-pick-prod` |
> | 8 | 运维手册 | `<service>-debugging`、`oncall-runner`、`log-correlator` |
> | 9 | 基础设施运维 | `<resource>-orphans`、`dependency-management`、`cost-investigation` |

> [!tip] 投资重点：产品验证类
> Anthropic 的经验是——**值得安排一个工程师花上一周时间专门打磨产品验证类 Skills**。验证 Skill 一旦稳定下来，能持续把 [[agent-等待时间|Agent 等待时间]] 降到接近 0；它是真正打通 [[harness-engineering|Harness Engineering]] 闭环的关键。

**类别选择即设计**：在写一个新 Skill 之前先判断它属于哪一类，能帮你确定该用什么文件结构、要不要带脚本、是否需要 Hooks、`description` 字段该怎么写。具体技巧见 [[skill-编写实践]]。

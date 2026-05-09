---
title: Coding Agent Eval
tags: [evals, coding-agent, swe-bench]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

Coding agent 评估的天然优势：**软件本身就有 deterministic 的对错判定**——代码能不能跑、单测过不过。SWE-bench Verified 和 Terminal-Bench 是两条主流路线：前者用 GitHub issue + 仓库自带测试套件、后者跑真实端到端技术任务。LLM 在 SWE-bench Verified 上一年内从 40% 涨到 >80%，已逼近 [[capability-vs-regression-eval|饱和]]。

## 两条主流 benchmark

> [!compare] SWE-bench Verified vs Terminal-Bench
> | 维度 | SWE-bench Verified | Terminal-Bench |
> |---|---|---|
> | 任务来源 | 流行 Python 仓库的 GitHub issues | 端到端真实技术任务（编 Linux 内核、训 ML 模型等） |
> | grader | 跑仓库原有测试套件——必须修好 failing test 且不能破坏 passing test | task-specific 验证脚本 |
> | 强调的能力 | 在熟悉 codebase 中精准修 bug | 长链路、跨工具、有副作用的端到端执行 |
> | 现状 | 一年从 40% → >80% | 仍有较大爬坡空间 |

## 单测之上：grade 轨迹

> [!note] outcome + transcript 双层评估
> 单测告诉你"对错"，但同样通过单测的代码可能：
> - 风格糟糕、违反代码规范
> - 用了反模式（hard-coded、重复逻辑）
> - 写得满是无用 try/except 把 bug 吞掉
>
> 所以 coding agent eval 通常组合：
> - **deterministic_tests**：单测是核心
> - **llm_rubric**：评代码质量、可读性、是否真正解决问题
> - **static_analysis**：ruff / mypy / bandit 等
> - **state_check**：security_logs、数据库副作用等
> - **tool_calls**：必需工具是否被调用（read_file / edit_file / run_tests）
> - **tracked metrics**：n_turns / n_toolcalls / n_tokens / latency

## 一个 task 的样例（取自原文）

```yaml
task:
  id: "fix-auth-bypass_1"
  desc: "Fix authentication bypass when password field is empty and ..."
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: state_check
      expect:
        security_logs: {event_type: "auth_blocked"}
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
  tracked_metrics:
    - type: transcript
      metrics: [n_turns, n_toolcalls, n_total_tokens]
    - type: latency
      metrics: [time_to_first_token, output_tokens_per_sec, time_to_last_token]
```

> [!warning] 这是"全口味展示"，不是推荐配置
> 实际项目里 coding eval **典型只用单测 + 代码质量 LLM rubric**，其他 grader 按需加。一开始就堆全套 grader 会让维护爆炸、且容易过约束（参见 [[eval-grader-三类|不要规定 tool 顺序]]）。

## 度量首选 pass@1

Coding agent 的产品形态决定了 [[pass-at-k-vs-pass-power-k|pass@1]] 是首选——开发者最关心"agent 一次性能不能交出可用 PR"。但 pass@k（k=3–5）也有信息量：能告诉你"再让它试几次能不能对"，对 background agent / coordinator 模式有意义。

## 与 [[claude-code|Claude Code]] 的实践链

Claude Code 自身的 eval 演化路径正是 [[eval-driven-development|EDD]] 的具体范例：

> [!example] Claude Code 的 eval 演化
> - 初期：靠 dogfooding + 内部 + 外部用户反馈快速迭代
> - 中期：加 narrow eval——concision、file edits
> - 后期：加更复杂行为 eval——over-engineering（典型 [[plausible-code|似是而非的代码]] 风险）
> - 持续期：eval + production monitoring + A/B + user research 多层叠加（[[eval-方法矩阵]]）

## 关联

- 总览：[[agent-evals]]
- 范式：[[eval-driven-development]]
- 模型饱和后怎么办：[[capability-vs-regression-eval]]
- 同类主体不同 agent：[[conversational-agent-eval]]、[[research-agent-eval]]、[[computer-use-agent-eval]]

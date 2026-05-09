---
title: Eval 方法矩阵（Swiss Cheese 模型）
tags: [evals, observability, methodology]
date: 2026-05-06
sources:
  - "[[sources/clippings/Demystifying evals for AI agents]]"
last-ingested: 2026-05-06
status: stable
---

理解 agent 性能不能只靠一种方法。Anthropic 推荐**多层叠加**——automated eval、production monitoring、A/B test、user feedback、manual transcript review、systematic human study 各补一层。这套思路类比安全工程的 **Swiss Cheese Model**：单层都有洞，但多层叠起来洞会被错开。

## 六层方法对比

> [!compare] 六种方法各司其职
> | 方法 | 强项 | 弱点 |
> |---|---|---|
> | **Automated evals** | 迭代快、可复现、不影响用户、能在每次 commit 跑、规模化 | 前期投入大、要持续维护防漂移、若不像真实使用会造成虚假信心 |
> | **Production monitoring** | 真实用户行为、抓 synthetic eval 抓不到的问题 | 反应式、问题已伤到用户才知道、缺 ground truth |
> | **A/B testing** | 测真实用户结果、控混淆变量、规模化 | 慢（要数天/周达显著性）、只能测已部署版本、对"为什么变了"信号弱 |
> | **User feedback** | 暴露未预期问题、来自真人 | 稀疏、自选偏差、用户很少解释 *why*、过度依赖会伤用户 |
> | **Manual transcript review** | 建立失败模式直觉、抓自动 grader 抓不到的细微问题 | 耗时、不可规模化、覆盖不一致、信号偏定性 |
> | **Systematic human studies** | 金标准、处理主观/歧义任务、给 LLM grader 提供校准数据 | 贵且慢、不能频繁跑、跨标注员要协调、复杂域要专家 |

## 各阶段配比

> [!note] 不同阶段权重不一样
> - **Pre-launch / CI/CD**：automated eval 是第一道防线，每次 agent 改动 + 模型升级都跑
> - **Post-launch**：production monitoring 接力，捕捉 distribution drift 和真实失败
> - **重大改动**：A/B test 在有足够流量时验证
> - **持续**：user feedback 和 transcript review 填补——周抽样读、每天 triage 反馈
> - **校准 / 主观任务**：systematic human study 仅用于校准 LLM grader 或评开放式输出

## 为什么是 Swiss Cheese 而不是单一方法

> [!important] 没有单层能 catch 一切
> - 只跑 [[agent-evals|automated eval]]：synthetic 永远偏离真实分布，会有意想不到的失败
> - 只看 production monitoring：发现问题时用户已经被伤到了
> - 只靠 A/B：决策慢、对"为什么"的信号弱
> - 只看 user feedback：稀疏 + self-selected，严重偏向极端 case
> - 只读 transcript：定性而非定量，且不可规模化
>
> 必须叠加。但叠加不是平均用力——用上面"各阶段配比"的优先级。

## 跟 [[读-transcript|读 transcript]] 的位置

读 transcript 在六种方法里横跨 **automated eval**、**production monitoring**、**user feedback** 三层——它是这些层产生的 trace 上的**人工解读步骤**，而不是独立的方法。这件事的瓶颈始终是"人愿不愿意打开文件读"。

## 关联

- 自动化 eval 怎么写：[[agent-evals]]、[[eval-grader-三类]]
- 范式背景：[[eval-driven-development]]
- 监控类比：[[self-healing-loop]]——把 production monitoring 的 trace 当作 agent eval 的另一个数据源
- 反例：[[plausible-code]]——单层防御漏掉的"看着对的代码"必须靠 monitoring/transcript review 兜底

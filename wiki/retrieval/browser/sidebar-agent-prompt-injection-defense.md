---
title: Sidebar Agent Prompt Injection 防御
tags: [browser, security, prompt-injection]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: draft
---

[[gstack]] Browser 的 sidebar agent（在 Chrome 侧栏跑的 Claude 子实例）面对最大威胁：**敌意网页通过页面内容劫持 agent**。gstack 用**多分类器集成 + canary token + verdict combiner** 三层防御，是当前个人浏览器 agent 中相对成熟的反 prompt injection 范式。

## 三层防御栈

> [!example] 多模型集成 + 行为检测 + 共识决策
> | 层 | 机制 | 检测什么 |
> |---|---|---|
> | **1. 本地 ML 分类器** | 22MB 小模型，浏览器随包发，扫每个 page + 每次 tool output | 已知 prompt injection 模式（"忽略上述指令…"） |
> | **2. Claude Haiku 整盘检查** | 看完整对话**形状**（不是单条消息），投票 | 对话是不是被劫持到偏离用户意图 |
> | **3. Canary Token** | 系统 prompt 里随机注入 token，扫所有出站文本/工具参数/URL/文件写入 | 会话被 exfil 时（token 出现在不该出现的地方）报警 |
>
> **Verdict combiner 要求两个分类器同意才 block**——这是关键设计：单分类器 false positive 在 Stack Overflow 这种"真的在讨论 prompt injection"的页面上很常见，单模型容易误杀。

## 为什么需要"形状"检测

> [!important] 单条消息看不出劫持
> Prompt injection 的本质是**对话方向被改变**。单看"网页内容"或"tool output"很难判断恶意——某段话可能是正常分享、可能是攻击 payload。
>
> Claude Haiku 检查的是**整段会话的轨迹**：
> - 用户原本要找 X
> - agent 走着走着开始干 Y
> - Y 跟 X 完全无关
>
> 这是 [[读-transcript|Read the Transcripts]] 范式的实时安全应用——人读 transcript 是事后审查、Haiku 实时读 transcript 是会话内防护。

## Canary Token 的细节

> [!tip] 为什么 canary 比 keyword filter 强
> 静态 keyword filter（"don't say credit card"）容易绕：
> - 攻击者用 base64 / 同义词 / 拆字
> - 攻击者跟 agent 说"假装 X"
>
> **Canary token 是会话独有的随机字符串**：
> - 它不在攻击者的字典里
> - 它本应只在内部 system prompt 见到
> - 一旦它出现在出站 HTTP / 文件写入 / tool 参数里，几乎一定是会话内容被 exfil
>
> 检测覆盖：text、tool args、URL、file writes——所有可能"带着内容走出 agent 边界"的地方。

## Opt-in 升级：DeBERTa-v3 集成

> [!compare] 默认 22MB vs 升级 721MB
> | 配置 | 模型 | 延迟 | 准确率 |
> |---|---|---|---|
> | 默认 | 22MB ML 分类器 + Haiku | 几十 ms | 实战已经够 |
> | `GSTACK_SECURITY_ENSEMBLE=deberta` | 721MB DeBERTa-v3 + 默认两个 | 慢一些 | 需要 2/3 同意才 block |
>
> 默认对小模型敏感的场景升级；多数人用默认即可。

## 紧急关闭与边界

> [!warning] 紧急 kill switch
> `GSTACK_SECURITY_OFF=1` 全关。**慎用**——你正在跑 agent 浏览敌意网页时关掉 = 直接裸奔。
>
> 适用场景：
> - 调试本地代码、确定不会触敌意网页
> - 反复 false positive 阻断真实工作（应当先 report 给 gstack 修分类器，不是默认关）

## 与 [[fail-closed-tool-defaults|Fail-Closed]] 的对应

> [!important] 默认拒绝、显式允许
> Verdict combiner 的"两个分类器同意才 block"看起来是 fail-open（疑似就放过），但配合 canary token 和 system prompt 设计是 fail-closed 的：
> - 一旦 canary 出现在出站，**直接 block 不投票**——这条 fail-closed
> - 普通可疑模式两投一通过——这条偏 fail-open 减少误杀
>
> 安全等级靠**多层组合**而不是单层 strict——单层 strict 会被 false positive 训得用户全关掉。

## 与 sidebar agent 自身设计的关系

Sidebar agent 是 **isolated session**——跟主 Claude Code 窗口不共享上下文。这本身就是一层"爆炸半径"控制：sidebar 被劫持，主会话不受影响。Anti-bot stealth + 自动 model routing（Sonnet 跑 action / Opus 跑 analysis）是性能层；prompt injection defense 是安全层。两层独立。

## 关联

- 浏览器范式：[[gstack]]、[[wiki/retrieval/browser/agent-browser|agent-browser]]、[[wiki/retrieval/browser/cdp|CDP]]
- 同源记忆：[[domain-skills]]
- 对照：[[fail-closed-tool-defaults|Fail-Closed Tool Defaults]]、[[permission-modes|权限模式]]
- 检测范式：[[读-transcript|Read the Transcripts]]——Haiku 整盘检查是其实时版
- 上游 review：[[gstack|/cso（Chief Security Officer）]] 在代码层做 OWASP / STRIDE，sidebar defense 在浏览器层做 prompt injection

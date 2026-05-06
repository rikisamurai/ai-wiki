---
title: Design Shotgun（mockup → HTML 流水线）
tags: [workflow, design, ai-design]
date: 2026-05-06
sources:
  - "[[sources/clippings/garrytangstack Use Garry Tan's exact Claude Code setup 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA]]"
last-ingested: 2026-05-06
status: draft
---

[[gstack]] 的设计工作流：**`/design-shotgun`** 一次生成 4–6 个 mockup 变体在浏览器里并排，让你点选偏好和反馈、迭代到满意 → **`/design-html`** 把选中的 mockup 转成可上线 HTML/CSS。核心解决的是"用文字描述 vision、AI 猜不准"的痛点——**让你看选项、不让你描述选项**。

## 为什么"霰弹"模式有效

> [!important] 视觉迭代 >> 文字描述
> 传统流程："我想要 hero 区简洁一点、配色蓝灰、字体大一点" → AI 出一个 → 不对 → 再描述 → 再出一个。每一轮你都要把脑中的画面**翻译成文字再让 AI 翻译回画面**——双重信息丢失。
>
> Design Shotgun 反过来：
> 1. AI 一次出 4–6 个变体（GPT Image 生成 mockup）
> 2. 在浏览器对比板里并排展示
> 3. 你点 favorite + 留反馈（"more whitespace"、"lose the gradient"）
> 4. AI 基于偏好生成下一轮 4–6 个
>
> 几轮后，"taste memory" 启动，开始向你实际选过的方向偏移。**你描述偏好的成本远低于描述方案**。

## Taste Memory：偏好沉淀

> [!example] gstack-taste-update
> `gstack-taste-update` CLI 把每次的 approval / rejection 写进**项目级 taste profile**，每周衰减 5%（防止旧偏好把当前方向锁死）。下一轮变体生成时把 taste profile 喂回 prompt——agent 学会你这个项目里偏好什么风格。
>
> 跟 [[wiki/claude-code/auto-memory|Auto Memory]] 同构：都是把"你给过的反馈"持久化为 [[wiki/agent-engineering/context/隐性知识与上下文|隐性知识]]。差别是 taste 是**视觉偏好**，需要的不是文字记忆而是 image-conditional bias。

## /design-html：mockup → 真 HTML

> [!compare] AI 出 HTML 的常见失败 vs gstack 解法
> | 失败模式 | gstack 的解 |
> |---|---|
> | 一个 viewport 看着对、其它 viewport 全乱 | **Pretext 计算文本布局** —— text 真的会 reflow、height adapt to content |
> | 输出"看起来像 demo"，没法直接上线 | 30KB overhead、零依赖；按 landing page / dashboard / form / card 不同 pattern 路由 |
> | 不知道项目用 React / Svelte / Vue | 自动检测框架、输出对应组件 |
> | AI Slop（魔法数字 / 硬编码 / 无意义动画） | `/plan-design-review` 的 AI Slop detection 串在前面 |

## 在 [[sprint-七阶段范式|七阶段]] 中的位置

```
Think  →  Plan  →  Build  →  Review  →  Test  →  Ship  →  Reflect
                    │
                    ├─ /design-consultation    → DESIGN.md（design system）
                    ├─ /design-shotgun         → 选中的 mockup
                    ├─ /design-html            → 可上线的 HTML/CSS
                    └─ /design-review          → 0-10 评分 + 编辑到 10
```

> [!tip] 与 [[plan-mode|Plan Mode]] 的对应
> Design Shotgun 是 design 维度的 Plan Mode——**先视觉对齐再写代码**，避免 AI 写出 800 行 React 组件后才发现方向错了要重来（属于典型的 [[rewind-胜过纠正|应该 rewind 的场景]]）。

## 与 GPT Image / Pretext 的依赖

- **GPT Image**：生成 mockup 变体的图像模型
- **Pretext**：gstack 自家的"computed text layout"——让 HTML 里的文本真正按内容动态调整尺寸

这两个是 design-shotgun → design-html 链路的关键基础设施。Pretext 不是普通框架——它解决的是"AI 出的 HTML 在不同 viewport 下不可靠"这个长期痛点。

## 关联

- 工具栈来源：[[gstack]]
- 流水线位置：[[sprint-七阶段范式]]
- 偏好持久化同族：[[wiki/claude-code/auto-memory]]、[[domain-skills]]
- UI 库参考：[[wiki/frontend/ui-libraries/shadcn-ui|shadcn/ui]]、[[wiki/frontend/ui-libraries/headless-ui|Headless UI]]
- 视觉迭代的反范式：[[plausible-code]]——AI 出的"看着像但不对"在 UI 上更隐蔽

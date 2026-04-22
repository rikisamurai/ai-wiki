---
title: 构建 Claude Code 的经验：如何使用 Skills
tags:
  - ai
  - claude-code
  - skills
  - agent
date: 2026-03-18
---

# 🚀 构建 Claude Code 的经验：如何使用 Skills

> [!info] 文章来源
> - 原文：Thariq Shihipar（Anthropic Claude Code 团队工程师）— [Lessons from Building Claude Code: How We Use Skills](https://x.com/trq212/status/2033949937936085378)
> - 翻译/注解：[@dotey（宝玉）](https://x.com/dotey/status/2034002188994060691)

Skills 是 Claude Code 中使用最广泛的扩展点之一。Anthropic 内部活跃使用的 Skills 已达**几百个**。本文是 Claude Code 团队从大规模内部实践中提炼出的经验总结——做什么类型的 Skills、怎么写、怎么在团队里推广。

## Skills 不只是 Markdown 文件

一个常见误解是 Skills "只不过是 markdown 文件"。实际上 Skills 是**文件夹**，可以包含脚本、资源文件、数据等。Claude Code 的 Agent 可以发现、探索和使用这些内容。Skills 还拥有丰富的配置选项，包括注册动态 Hooks。最有意思的那些 Skills，往往就是创造性地利用了文件夹结构和配置选项。

## 9 大 Skills 分类

Anthropic 梳理了内部所有 Skills 后，发现它们大致可归为 9 个反复出现的类别。**好的 Skills 清晰地落在某一个类别里；让人困惑的 Skills 往往横跨了好几个。**

### 1. 库与 API 参考

帮助正确使用某个库、CLI 工具或 SDK。通常包含参考代码片段和踩坑点列表。

- `billing-lib` — 内部计费库的边界情况和常见陷阱
- `internal-platform-cli` — 内部 CLI 工具的子命令及使用示例
- `frontend-design` — 让 Claude 更好地理解你的设计系统

### 2. 产品验证

描述如何测试或验证代码是否正常工作。通常搭配 Playwright、tmux 等工具。

> [!tip] 值得安排一个工程师花上一周时间专门打磨验证类 Skills。

- `signup-flow-driver` — 在无头浏览器中跑完注册→邮件验证→引导流程
- `checkout-verifier` — 用 Stripe 测试卡驱动结账 UI，验证发票状态
- `tmux-cli-driver` — 针对需要 TTY 的交互式命令行测试

### 3. 数据获取与分析

连接数据和监控体系。可能包含凭证、仪表盘 ID、常用工作流说明。

- `funnel-query` — 注册→激活→付费的转化分析
- `cohort-compare` — 对比用户群留存或转化率
- `grafana` — 数据源 UID、集群名称、问题→仪表盘对照表

### 4. 业务流程与团队自动化

把重复性工作流自动化为一条命令。通常指令较简单，但可能依赖其他 Skills 或 MCP。

- `standup-post` — 汇总任务追踪器、GitHub 活动和 Slack 消息→生成站会汇报
- `create-ticket` — 强制执行 schema 和创建后的通知工作流
- `weekly-recap` — 已合并 PR + 已关闭工单 + 部署记录→周报

### 5. 代码脚手架与模板

为特定功能生成框架样板代码。当脚手架有自然语言需求、无法纯靠代码覆盖时特别有用。

- `new-<framework>-workflow` — 用注解搭建新的服务/工作流/处理器
- `new-migration` — 数据库迁移文件模板加踩坑点
- `create-app` — 新建内部应用，预配认证、日志和部署

### 6. 代码质量与审查

执行代码质量标准并辅助 Code Review。可以作为 Hooks 或 GitHub Action 的一部分自动运行。

- `adversarial-review` — 生成全新视角的子 Agent 来挑刺，反复迭代
- `code-style` — 强制执行 Claude 默认做不好的代码风格
- `testing-practices` — 关于如何写测试以及测试什么的指导

### 7. CI/CD 与部署

帮你拉取、推送和部署代码。

- `babysit-pr` — 监控 PR→重试不稳定 CI→解决合并冲突→启用自动合并
- `deploy-<service>` — 构建→冒烟测试→渐进式流量切换→指标恶化时回滚
- `cherry-pick-prod` — 隔离的 worktree→cherry-pick→解决冲突→创建 PR

### 8. 运维手册

接收现象（Slack 消息、告警、错误特征），引导走完排查流程，生成结构化报告。

- `<service>-debugging` — 把现象对应到工具→查询模式
- `oncall-runner` — 拉取告警→检查常见嫌疑→格式化排查结论
- `log-correlator` — 给定请求 ID，从所有系统拉取匹配日志

### 9. 基础设施运维

执行日常维护和运维操作，涉及破坏性操作时需要安全护栏。

- `<resource>-orphans` — 找到孤立 Pod/Volume→等待确认→级联清理
- `dependency-management` — 依赖审批工作流
- `cost-investigation` — 存储/带宽费用异常排查

## 编写 Skills 的最佳实践

### 不要说显而易见的事

Claude 对代码库已经非常了解，重点放在能**打破 Claude 常规思维模式**的信息上。比如 Anthropic 内部的 `frontend-design` Skill 就是通过反复迭代改进 Claude 的设计品味，专门避免 Inter 字体和紫色渐变等套路。

### 建一个踩坑点章节

![[Pasted image 20260318163149.png]]

任何 Skill 中信息量最大的部分就是踩坑点（Gotchas）章节。应该根据 Claude 使用 Skill 时遇到的常见失败点逐步积累。


### 利用文件系统与渐进式披露

Skill 是文件夹，把整个文件系统当作 Context Engineering 和渐进式披露的工具。不要一次性把所有信息塞给模型，而是告诉 Claude 有哪些文件，让它在需要时去读取，节省上下文窗口。

> [!example] 渐进式披露的简单形式
> - 详细的函数签名拆到 `references/api.md`
> - 输出模板放在 `assets/` 目录
> - 参考资料、脚本、示例分别归入对应文件夹





### 不要把 Claude 限制得太死

由于 Skills 的复用性很强，指令不要写得太具体。给 Claude 需要的信息，但留给它适应具体情况的灵活性。
![[Pasted image 20260318170757.png]]



### 考虑好初始设置

有些 Skills 需要用户提供上下文完成初始设置。好的做法是把设置信息存在 Skill 目录下的 `config.json` 里，如果配置未设置，Agent 会向用户询问。

### description 字段是给模型看的

Claude Code 启动会话时会构建可用 Skills 清单，通过扫描 description 判断该用哪个 Skill。**description 不是摘要，而是描述何时该触发这个 Skill**，读起来更像 if-then 条件。
![[Pasted image 20260318113942.png]]


### 记忆与数据存储

Skills 可以通过存储数据实现记忆——简单的 JSON/文本日志，或 SQLite 数据库。数据应存在稳定文件夹（如 `${CLAUDE_PLUGIN_DATA}`），避免 Skill 升级时丢失。

例如，一个 standup-post Skill 可以保留一份 standups.log，记录它写过的每一条站会汇报。这样下次运行时，Claude 会读取自己的历史记录，就能知道从昨天到现在发生了什么变化。

### 存储脚本与生成代码

你能给 Claude 的最强大的工具之一就是代码。给 Claude 提供脚本和库，让它把精力花在组合编排上——决定下一步做什么，而不是重新构造样板代码。

给 Claude 提供脚本和库，让它把精力花在组合编排上。例如在数据科学 Skill 中放一组从事件源获取数据的函数库，Claude 可以即时生成脚本组合它们。

### 按需 Hooks
> [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks#hooks-reference)

Skills 可以包含只在被调用时才激活的 Hooks（On Demand Hooks），在整个会话期间保持生效。

- `/careful` — 通过 PreToolUse 拦截 `rm -rf`、`DROP TABLE`、`force-push` 等危险操作
- `/freeze` — 阻止对特定目录之外的任何写操作，调试时防止误改



## 衡量 Skills 的效果

为了了解一个 Skill 的表现，我们使用了一个 PreToolUse 钩子来在公司内部记录 Skill 的使用情况（[示例代码在这里](https://gist.github.com/ThariqS/24defad423d701746e23dc19aace4de5)）。这样我们就能发现哪些 Skills 很受欢迎，或者哪些触发频率低于预期。

Skills 是 AI 智能体（AI Agent）极其强大且灵活的工具，但这一切还处于早期阶段，我们都在摸索怎样用好它们。

与其把这篇文章当作权威指南，不如把它看作我们实践中验证过有效的一堆实用技巧合集。理解 Skills 最好的方式就是动手开始做、不断试验、看看什么对你管用。我们大多数 Skills 一开始就是几行文字加一个踩坑点，后来因为大家不断补充 Claude 遇到的新边界情况，才慢慢变好的。

希望这篇文章对你有帮助，如果有任何问题欢迎告诉我。
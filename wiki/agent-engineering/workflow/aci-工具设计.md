---
title: ACI 工具设计（Agent-Computer Interface）
tags: [tool-design, aci, agent-engineering]
date: 2026-05-16
sources:
  - "[[sources/clippings/你不知道的 Agent：原理、架构与工程实践]]"
last-ingested: 2026-05-16
status: draft
---

ACI（Agent-Computer Interface）是一种工具设计哲学：**工具应对应 Agent 的目标，而不是底层 API 操作**。类比 HCI 对人的影响，工具设计对 Agent 的影响同样直接——不能只看"工具能不能调用"，还要看"调用错了之后能不能自己修回来"。

工具设计从三个阶段演进而来：

## 三代演进

**第一代 — API 封装**：每个 API Endpoint 对应一个工具，粒度过细。Agent 常需协调多个工具才能完成一个目标。

**第二代 — ACI**：工具对应 Agent 的目标，而非底层操作。

> [!compare] 差 vs 好
> ```
> ❌ 三个工具：create_file + write_content + set_permissions
> ✓ 一个工具：create_script(path, content, executable)
> ```

**第三代 — Advanced Tool Use**：在工具设计之上优化发现、调用和描述方式：

| 技术 | 做法 | 效果 |
|---|---|---|
| **Tool Search（动态发现）** | 模型通过 `search_tools` 按需获取工具定义 | 上下文保留率 95%，准确率 49% → 74% |
| **Programmatic Tool Calling** | 模型用代码编排多工具调用，中间结果在执行环境流转 | token 消耗 150,000 → 2,000 |
| **Tool Use Examples（示例驱动）** | 每个工具附带 1-5 个真实调用示例 | 调用准确率 72% → 90% |

## ACI 三原则

> [!note] 1. 面向目标，而非 API
> 把多步 API 操作合并为一个对应用户目标的工具，降低 Agent 的协调负担。

> [!note] 2. 参数防错
> 用 Zod schema 等类型系统约束参数格式，把问题暴露在编译期。参数描述要包含格式示例（"纯数字字符串，如 '12345678'"）。

> [!note] 3. 结构化错误 + 修正建议
> 错误不能只返回字符串，要给出可操作的修正路径：
> ```typescript
> throw new ToolError("文章 ID 不存在", {
>   error_code: "POST_NOT_FOUND",
>   suggestion: "请先调用 list_yuque_posts 获取有效的 post_id",
> });
> ```

## 调试优先法则

**调试 Agent 时应先检查工具定义，而不是先怀疑模型能力**。大多数工具选择错误源于描述不准确，不在模型本身。

工具数量也要克制——能用 Shell 处理的、只需静态知识的、更适合用 [[skills/skill-编写实践|Skill]] 的，都不需要新增工具。5 个 MCP 服务器可能带来约 55,000 tokens 的定义开销。

## 工具消息隔离

框架内部事件（压缩发生、通知推送、工具调用跳过）需要记录在会话历史里，但不应直接进入 LLM。做法：定义两种消息类型——`AgentMessage`（携带自定义字段）和发给 LLM 的 `Message`（只含 user/assistant/tool_result），调用前过滤一遍。

## 相关页面

- [[workflow/工具错误分类法|工具错误分类法]] — 工具调用失败的系统性分类
- [[agent-loop|Agent Loop]] — 工具调用在 ReAct 循环中的位置
- [[skills/skill-编写实践|Skill 编写实践]] — 知识型内容用 Skill 替代工具的实践
- [[agent-engineering/context/context-rot|Context Rot]] — 工具定义过多对上下文的影响

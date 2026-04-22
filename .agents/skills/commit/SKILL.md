---
name: commit-doc
description: Use when the user wants to commit changes - runs git diff, generates a commit message, and commits automatically. Trigger with /commit slash command.
---

# Git Auto Commit（Obsidian 知识库专用）

当用户触发 `/commit` 时，自动分析当前改动并生成 commit message，完成提交。

## Workflow

按顺序执行以下步骤，**不要跳过，不要提前询问用户**：

### 1. 获取当前状态

先暂存所有改动，再统一查看 diff：

```bash
git add -A
```

然后并行运行：
- `git diff --cached` — 查看所有已暂存的改动，**包括新增文件**（新文件以 `+++ b/file` 形式完整展示）
- `git log --oneline -5` — 了解本项目的 commit 风格

### 2. 分析改动

根据 `git diff --cached` 的内容判断：
- **改动类型**：新增笔记、修改笔记、结构调整、配置变更等
- **影响范围**：哪些目录或笔记受影响
- **核心意图**：这次改动的主要目的

### 3. 生成 commit message

**格式规则：**
- 使用 Conventional Commits 前缀，聚焦文档场景：
  - `docs` — 新增或修改笔记内容
  - `feat` — 新增功能性结构（新目录、新 Canvas、新 skill 等）
  - `chore` — 配置调整、整理归档、非内容性变更
  - `fix` — 修正笔记中的错误内容
- 中文撰写，英文专有名词保持英文（如 Claude Code、Agent、MCP）
- 主题行不超过 72 字符
- 只有一行 subject，不加 body（除非改动非常复杂）

**示例：**
```
docs: 新增 Claude Code hooks 使用笔记
docs: 更新 MCP 配置说明，补充示例
feat: 新增 AIGC 目录结构
chore: 整理 skills 软链接
fix: 修正 Prompt Engineering 笔记中的错误描述
```

### 4. 验收 commit message

确认面板打开后，用户往往看不到**上一条** assistant 气泡里的 commit message，因此：

1. **必须把完整 commit message 写进 `AskUserQuestion` 的 `prompt`**（主展示位），不要假设用户还能看见别处的内容。
2. `prompt` 结构建议：一两句说明 +  fenced 代码块包住 message + 一句「是否采用？若要修改请在本轮对话里直接写出新的 message」。
3. 可选：在同一条 assistant 消息正文里再用代码块写一遍（与 `prompt` 内**完全一致**），便于在时间线里搜索；**以即将提交的内容为准，即 `prompt` 里的那段**。

`prompt` 模板示例（外层围栏用四个反引号，内层才能再写三反引号代码块）：

````text
准备提交，commit message 如下：

```
<生成的 commit message>
```

是否采用？若要改成别的，请在本轮对话里直接写出完整新 message；选「取消」则中止提交。
````

根据用户回复：
- **确认** → 使用原 message 执行 Step 5 提交
- **提供新 message** → 使用用户提供的 message 执行 Step 5 提交
- **取消** → 中止提交，告知用户已取消

### 5. 提交

文件已在 Step 1 暂存，直接提交：

```bash
git commit -m "$(cat <<'EOF'
<确认的 commit message>
EOF
)"
```

**注意：**
- 不要添加 `--no-verify`，遵守项目 hooks
- 如果 commit 失败（如 hook 报错），修复问题后重新提交，不要 amend

### 6. 展示结果

提交成功后，运行 `git show --stat HEAD` 并输出：
1. 提交的 commit hash 和 git message
2. 改动了哪些文件

## 特殊情况

**没有改动：** `git add -A` 后 `git diff --cached` 无输出，告知用户当前工作区是干净的，无需提交。

**有冲突文件：** 停止提交，提示用户先解决冲突。

**用户传入参数（如 `/commit docs: 新增笔记`）：** 将参数作为 commit message 直接使用，跳过自动生成步骤。

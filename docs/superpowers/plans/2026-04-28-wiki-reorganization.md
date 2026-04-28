# wiki/ 目录重组 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `wiki/` 从 4 个一级目录（ai-coding / aigc / frontend / obsidian）重组为 8 个（agent-engineering / claude-code / skills / retrieval / frontend / business / obsidian / _orphans），ai-coding/frontend/retrieval 引入二级子目录，共移动 117 个文件、批改 362 处全路径 wikilink + 4 处 sources 反向引用。

**Architecture:** 在 feature branch `wiki-reorg-2026-04` 上做 3 个原子 commit：(1) 一个 Python 重组脚本，(2) 跑脚本完成所有文件移动 + wikilink 替换，(3) 同步 schema 文件（AGENT.md / ingest.md / index.md / log.md）。

**Tech Stack:** Python 3（标准库即可，跨平台、字符串处理可靠）+ git + ripgrep。

**Spec:** `docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md`

---

## 任务 0: 预备工作

**Files:**
- 影响：本地 git 状态、Obsidian app

- [ ] **Step 0.1: 检查 git status，记录当前未提交的改动**

```bash
git status
```

预期：会看到 `.obsidian/plugins/manual-sorting/data.json` 和 `log.md` 的 modified 状态（来自前期工作）。`log.md` 是上一轮 query 追加的合法记录，应单独 commit；plugin 的 data.json 是无关 plugin state，stash 即可。

- [ ] **Step 0.2: 提交 log.md 的 query 日志（来自上一轮 query）**

```bash
git add log.md
git commit -m "docs: log query 记录"
```

预期：commit 落定。`git status` 仅剩 plugin data.json 的 modified。

- [ ] **Step 0.3: stash plugin state**

```bash
git stash push -m "manual-sorting plugin state during wiki reorg" .obsidian/plugins/manual-sorting/data.json
```

预期：`git status` 完全干净。

- [ ] **Step 0.4: 创建 feature branch**

```bash
git checkout -b wiki-reorg-2026-04
git status
```

预期：分支切到 `wiki-reorg-2026-04`，工作树干净。

- [ ] **Step 0.5: 提示用户关闭 Obsidian app**

输出消息：

> 接下来要批量移动 138 个 wiki 文件并改 wikilink。请关闭 Obsidian app（或至少这个 vault），避免 "Update internal links" 设置和脚本竞态。关好后说 ok。

等待用户确认。

---

## 任务 1: 写重组脚本 + dry-run（Commit 1）

**Files:**
- Create: `scripts/reorg-wiki.py`

- [ ] **Step 1.1: 创建 scripts/ 目录**

```bash
mkdir -p scripts
ls scripts/
```

预期：目录存在或已新建。

- [ ] **Step 1.2: 写 scripts/reorg-wiki.py 完整内容**

写入下面文件（完整 117 行 mapping）：

```python
#!/usr/bin/env python3
"""Reorganize wiki/ directory per docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md.

Run from repo root:
  DRY_RUN=1 python3 scripts/reorg-wiki.py   # preview only
  python3 scripts/reorg-wiki.py             # actually move + rewrite

Step 1: git mv each (old, new) pair.
Step 2: scan wiki/ + sources/ for [[wiki/<old>]] and [[wiki/<old>|alias]] forms,
        replace with new paths.
"""

import os
import subprocess
import sys

# (old_path_without_md, new_path_without_md) — 117 entries.
MAPPING = [
    # === ai-coding/ → agent-engineering/ (52 files) ===
    # philosophy (19)
    ("ai-coding/agent-工作量分布", "agent-engineering/philosophy/agent-工作量分布"),
    ("ai-coding/agentic-coding", "agent-engineering/philosophy/agentic-coding"),
    ("ai-coding/ai-first-vs-ai-assisted", "agent-engineering/philosophy/ai-first-vs-ai-assisted"),
    ("ai-coding/ai-first-工程前提", "agent-engineering/philosophy/ai-first-工程前提"),
    ("ai-coding/ai-first-适用边界", "agent-engineering/philosophy/ai-first-适用边界"),
    ("ai-coding/harness-engineering", "agent-engineering/philosophy/harness-engineering"),
    ("ai-coding/harness-成熟度", "agent-engineering/philosophy/harness-成熟度"),
    ("ai-coding/opc-一人公司", "agent-engineering/philosophy/opc-一人公司"),
    ("ai-coding/plausible-code", "agent-engineering/philosophy/plausible-code"),
    ("ai-coding/spec-coding", "agent-engineering/philosophy/spec-coding"),
    ("ai-coding/vibe-coding", "agent-engineering/philosophy/vibe-coding"),
    ("ai-coding/vibe-coding-对-saas-的通缩", "agent-engineering/philosophy/vibe-coding-对-saas-的通缩"),
    ("ai-coding/vibe-coding-的代价", "agent-engineering/philosophy/vibe-coding-的代价"),
    ("ai-coding/worse-is-better", "agent-engineering/philosophy/worse-is-better"),
    ("ai-coding/yagni-与-dry-反论", "agent-engineering/philosophy/yagni-与-dry-反论"),
    ("ai-coding/架构师-操作员二分", "agent-engineering/philosophy/架构师-操作员二分"),
    ("ai-coding/约束悖论", "agent-engineering/philosophy/约束悖论"),
    ("ai-coding/行为正确性", "agent-engineering/philosophy/行为正确性"),
    ("ai-coding/高吞吐合并哲学", "agent-engineering/philosophy/高吞吐合并哲学"),
    # context (12)
    ("ai-coding/cache-keep-alive", "agent-engineering/context/cache-keep-alive"),
    ("ai-coding/cache-命中率", "agent-engineering/context/cache-命中率"),
    ("ai-coding/cache-失效陷阱", "agent-engineering/context/cache-失效陷阱"),
    ("ai-coding/compact-vs-clear", "agent-engineering/context/compact-vs-clear"),
    ("ai-coding/context-rot", "agent-engineering/context/context-rot"),
    ("ai-coding/context-window", "agent-engineering/context/context-window"),
    ("ai-coding/kv-cache", "agent-engineering/context/kv-cache"),
    ("ai-coding/prefix-cache", "agent-engineering/context/prefix-cache"),
    ("ai-coding/会话管理动作", "agent-engineering/context/会话管理动作"),
    ("ai-coding/冻结快照模式", "agent-engineering/context/冻结快照模式"),
    ("ai-coding/稳定前缀-动态后缀", "agent-engineering/context/稳定前缀-动态后缀"),
    ("ai-coding/隐性知识与上下文", "agent-engineering/context/隐性知识与上下文"),
    # workflow (17 from ai-coding)
    ("ai-coding/agent-可读性", "agent-engineering/workflow/agent-可读性"),
    ("ai-coding/agent-等待时间", "agent-engineering/workflow/agent-等待时间"),
    ("ai-coding/agents-md", "agent-engineering/workflow/agents-md"),
    ("ai-coding/doc-gardening", "agent-engineering/workflow/doc-gardening"),
    ("ai-coding/enforce-invariants", "agent-engineering/workflow/enforce-invariants"),
    ("ai-coding/long-horizon-agent", "agent-engineering/workflow/long-horizon-agent"),
    ("ai-coding/ralph-loop", "agent-engineering/workflow/ralph-loop"),
    ("ai-coding/rewind-胜过纠正", "agent-engineering/workflow/rewind-胜过纠正"),
    ("ai-coding/self-healing-loop", "agent-engineering/workflow/self-healing-loop"),
    ("ai-coding/subagent-driven-development", "agent-engineering/workflow/subagent-driven-development"),
    ("ai-coding/subagent-上下文隔离", "agent-engineering/workflow/subagent-上下文隔离"),
    ("ai-coding/writer-reviewer-模式", "agent-engineering/workflow/writer-reviewer-模式"),
    ("ai-coding/两次纠正规则", "agent-engineering/workflow/两次纠正规则"),
    ("ai-coding/任务三维划分", "agent-engineering/workflow/任务三维划分"),
    ("ai-coding/探索-规划-编码-验证", "agent-engineering/workflow/探索-规划-编码-验证"),
    ("ai-coding/采访驱动-spec", "agent-engineering/workflow/采访驱动-spec"),
    ("ai-coding/验证驱动", "agent-engineering/workflow/验证驱动"),
    # code-review (4)
    ("ai-coding/ai-code-review", "agent-engineering/code-review/ai-code-review"),
    ("ai-coding/ai-写-lint", "agent-engineering/code-review/ai-写-lint"),
    ("ai-coding/review-带宽瓶颈", "agent-engineering/code-review/review-带宽瓶颈"),
    ("ai-coding/shift-left", "agent-engineering/code-review/shift-left"),

    # === aigc/ → claude-code/ skills/ retrieval/ + 1 to agent-engineering/workflow (38 files) ===
    # claude-code (22)
    ("aigc/claude-code", "claude-code/claude-code"),
    ("aigc/claude-code-memory", "claude-code/claude-code-memory"),
    ("aigc/claude-code-六层架构", "claude-code/claude-code-六层架构"),
    ("aigc/claude-rules", "claude-code/claude-rules"),
    ("aigc/claude-health", "claude-code/claude-health"),
    ("aigc/claude-hud", "claude-code/claude-hud"),
    ("aigc/hooks", "claude-code/hooks"),
    ("aigc/settings-scopes", "claude-code/settings-scopes"),
    ("aigc/permission-modes", "claude-code/permission-modes"),
    ("aigc/plan-mode", "claude-code/plan-mode"),
    ("aigc/fail-closed-tool-defaults", "claude-code/fail-closed-tool-defaults"),
    ("aigc/read-before-edit", "claude-code/read-before-edit"),
    ("aigc/inline-edit", "claude-code/inline-edit"),
    ("aigc/handoff-md", "claude-code/handoff-md"),
    ("aigc/kairos-记忆蒸馏", "claude-code/kairos-记忆蒸馏"),
    ("aigc/auto-memory", "claude-code/auto-memory"),
    ("aigc/everything-claude-code", "claude-code/everything-claude-code"),
    ("aigc/opencli", "claude-code/opencli"),
    ("aigc/codex", "claude-code/codex"),
    ("aigc/codex-plugin", "claude-code/codex-plugin"),
    ("aigc/codex-sandbox-approval", "claude-code/codex-sandbox-approval"),
    ("aigc/mcp", "claude-code/mcp"),
    # skills (7)
    ("aigc/agent-skills", "skills/agent-skills"),
    ("aigc/skill-编写实践", "skills/skill-编写实践"),
    ("aigc/skills-9-分类", "skills/skills-9-分类"),
    ("aigc/skills-marketplace", "skills/skills-marketplace"),
    ("aigc/skills-vs-automations", "skills/skills-vs-automations"),
    ("aigc/superpowers", "skills/superpowers"),
    ("aigc/渐进式披露", "skills/渐进式披露"),
    # retrieval/rag (4)
    ("aigc/rag", "retrieval/rag/rag"),
    ("aigc/agentic-rag", "retrieval/rag/agentic-rag"),
    ("aigc/graph-rag", "retrieval/rag/graph-rag"),
    ("aigc/hybrid-retrieval", "retrieval/rag/hybrid-retrieval"),
    # retrieval/browser (4)
    ("aigc/agent-browser", "retrieval/browser/agent-browser"),
    ("aigc/browser-use", "retrieval/browser/browser-use"),
    ("aigc/cdp", "retrieval/browser/cdp"),
    ("aigc/cdp-能力边界", "retrieval/browser/cdp-能力边界"),
    # 1 to agent-engineering/workflow
    ("aigc/coordinator-模式", "agent-engineering/workflow/coordinator-模式"),

    # === frontend/ → frontend/<sub>/ + business/ (27 files) ===
    # web-platform (5)
    ("frontend/bun", "frontend/web-platform/bun"),
    ("frontend/vercel", "frontend/web-platform/vercel"),
    ("frontend/webcontainers", "frontend/web-platform/webcontainers"),
    ("frontend/mutation-observer", "frontend/web-platform/mutation-observer"),
    ("frontend/resize-observer", "frontend/web-platform/resize-observer"),
    # network (5)
    ("frontend/http-3", "frontend/network/http-3"),
    ("frontend/quic", "frontend/network/quic"),
    ("frontend/0-rtt-握手", "frontend/network/0-rtt-握手"),
    ("frontend/connection-migration", "frontend/network/connection-migration"),
    ("frontend/head-of-line-blocking", "frontend/network/head-of-line-blocking"),
    # react-patterns (5)
    ("frontend/no-useeffect-rule", "frontend/react-patterns/no-useeffect-rule"),
    ("frontend/usemounteffect", "frontend/react-patterns/usemounteffect"),
    ("frontend/key-重置组件", "frontend/react-patterns/key-重置组件"),
    ("frontend/派生状态", "frontend/react-patterns/派生状态"),
    ("frontend/组件强制函数", "frontend/react-patterns/组件强制函数"),
    # react-native (4)
    ("frontend/flash-list", "frontend/react-native/flash-list"),
    ("frontend/view-recycling", "frontend/react-native/view-recycling"),
    ("frontend/pressable-vs-touchable", "frontend/react-native/pressable-vs-touchable"),
    ("frontend/react-native-core-components", "frontend/react-native/react-native-core-components"),
    # ui-libraries (6)
    ("frontend/shadcn-ui", "frontend/ui-libraries/shadcn-ui"),
    ("frontend/headless-ui", "frontend/ui-libraries/headless-ui"),
    ("frontend/css-scrollbar-styling", "frontend/ui-libraries/css-scrollbar-styling"),
    ("frontend/overlay-scrollbar-pattern", "frontend/ui-libraries/overlay-scrollbar-pattern"),
    ("frontend/overlayscrollbars", "frontend/ui-libraries/overlayscrollbars"),
    ("frontend/scrollbar-mock-vs-overlay", "frontend/ui-libraries/scrollbar-mock-vs-overlay"),
    # business (2)
    ("frontend/js-盈利模式分类", "business/js-盈利模式分类"),
    ("frontend/per-seat-licensing", "business/per-seat-licensing"),
]

DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"


def assert_repo_root() -> None:
    if not os.path.isdir(".git") or not os.path.isdir("wiki"):
        sys.exit("error: run from repo root (where .git/ and wiki/ live)")


def move_files() -> None:
    print(f"=== Step 1: moving {len(MAPPING)} files ===")
    for old, new in MAPPING:
        old_path = f"wiki/{old}.md"
        new_path = f"wiki/{new}.md"
        if not os.path.isfile(old_path):
            sys.exit(f"error: {old_path} not found (already moved?)")
        if DRY_RUN:
            print(f"  DRY: git mv {old_path} {new_path}")
        else:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            subprocess.run(["git", "mv", old_path, new_path], check=True)
    print(f"  ok: {len(MAPPING)} files moved")


def rewrite_wikilinks() -> None:
    print("=== Step 2: rewriting wikilinks in wiki/ + sources/ ===")
    changed = 0
    for root in ("wiki", "sources"):
        for dirpath, _, files in os.walk(root):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dirpath, fn)
                with open(path, encoding="utf-8") as f:
                    original = f.read()
                content = original
                for old, new in MAPPING:
                    content = content.replace(f"[[wiki/{old}|", f"[[wiki/{new}|")
                    content = content.replace(f"[[wiki/{old}]]", f"[[wiki/{new}]]")
                if content != original:
                    if DRY_RUN:
                        print(f"  DRY: would rewrite {path}")
                    else:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"  rewritten: {path}")
                    changed += 1
    print(f"  ok: {changed} files rewritten")


def main() -> None:
    assert_repo_root()
    move_files()
    if DRY_RUN:
        print("\nDRY_RUN=1 → 跳过 wikilink 重写（依赖文件已被移动）。")
        print("Set DRY_RUN=0 (or unset) to actually run.")
        return
    rewrite_wikilinks()
    print("\n=== done ===")


if __name__ == "__main__":
    main()
```

- [ ] **Step 1.3: 让脚本可执行**

```bash
chmod +x scripts/reorg-wiki.py
```

- [ ] **Step 1.4: dry-run 验证脚本能解析所有 mapping 且每个旧路径都存在**

```bash
DRY_RUN=1 python3 scripts/reorg-wiki.py 2>&1 | tail -5
```

预期输出最后几行：
```
  DRY: git mv wiki/frontend/per-seat-licensing.md wiki/business/per-seat-licensing.md
  ok: 117 files moved

DRY_RUN=1 → 跳过 wikilink 重写（依赖文件已被移动）。
Set DRY_RUN=0 (or unset) to actually run.
```

如果有 "error: wiki/X.md not found" → 检查 mapping 拼写。

- [ ] **Step 1.5: 提交 commit 1**

```bash
git add scripts/reorg-wiki.py
git commit -m "$(cat <<'EOF'
chore: 准备 wiki 重组脚本

scripts/reorg-wiki.py 含完整 117 行 mapping + dry-run 支持。详见 docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md。
EOF
)"
git log --oneline -1
```

预期：commit 落定，消息如上。

---

## 任务 2: 执行重组（Commit 2）

**Files:**
- 移动 117 个 wiki/*.md 文件
- 修改所有 wiki/**/*.md 含 `[[wiki/<old>]]` 的内容
- 修改 sources/posts/frontend/libraries/overlayscrollbars.md（4 处反向引用，由脚本捎带处理）

- [ ] **Step 2.1: 实跑脚本**

```bash
python3 scripts/reorg-wiki.py
```

预期输出末尾：
```
=== Step 1: moving 117 files ===
  ok: 117 files moved
=== Step 2: rewriting wikilinks in wiki/ + sources/ ===
  rewritten: wiki/agent-engineering/...
  ...
  ok: <N> files rewritten
=== done ===
```

中途若失败，看错误信息：
- "git mv X Y: fatal: ... not under version control" → 之前有未追踪文件，先 `git status`
- "Permission denied" → 没 chmod，重跑 Step 1.3

- [ ] **Step 2.2: 硬验证 #1—旧目录已不存在**

```bash
[ ! -d wiki/ai-coding ] && [ ! -d wiki/aigc ] && echo "PASS" || echo "FAIL"
```

预期：`PASS`

- [ ] **Step 2.3: 硬验证 #2—文件总数仍为 138**

```bash
find wiki -name '*.md' | wc -l
```

预期：`138`

- [ ] **Step 2.4: 硬验证 #3—无残留指向 ai-coding/aigc 旧路径的 wikilink**

```bash
rg -c '\[\[wiki/(ai-coding|aigc)/' wiki/ sources/ 2>/dev/null
```

预期：无任何输出（rg 无匹配时 exit 1，stderr 也无内容）。如有输出 → wikilink 重写漏了，回 Task 1 调脚本重跑。

- [ ] **Step 2.5: 硬验证 #4—悬空 wikilink 检测（每个 [[wiki/X]] 必须能解析）**

```bash
python3 - <<'PYEOF'
import os, re, sys
ROOTS = ["wiki", "sources"]
PAT = re.compile(r'\[\[wiki/([^\]\|]+)')
broken = []
for root in ROOTS:
    for dp, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    for m in PAT.finditer(line):
                        target = f"wiki/{m.group(1)}.md"
                        if not os.path.isfile(target):
                            broken.append(f"{path}:{i}: -> {target}")
if broken:
    print("BROKEN wikilinks:")
    print("\n".join(broken))
    sys.exit(1)
print(f"PASS: all [[wiki/X]] links resolve to existing files")
PYEOF
```

预期：`PASS: all [[wiki/X]] links resolve to existing files`

如有 `BROKEN wikilinks:` → 检查输出列表，可能是脚本 mapping 漏了某条或文件名拼写错。修脚本，`git restore .`，回 Task 2.1 重跑。

- [ ] **Step 2.6: 检查 git status 看待提交差异规模**

```bash
git status --short | wc -l
git diff --stat | tail -1
```

预期：约 117 文件 R（rename）+ 较多 M（modified for wikilink rewrite）；总改动数千行。

- [ ] **Step 2.7: 提交 commit 2**

```bash
git add -A
git commit -m "$(cat <<'EOF'
refactor: 重组 wiki/ 目录结构（117 文件 mv + 362 wikilink 重写）

按方案二（重画一级 + 主题下沉）：
- ai-coding/ → agent-engineering/{philosophy,context,workflow,code-review}/
- aigc/ → claude-code/, skills/, retrieval/{rag,browser}/, + 1 to agent-engineering/workflow
- frontend/ → frontend/{web-platform,network,react-patterns,react-native,ui-libraries}/ + business/
- obsidian/, _orphans/ 原地不动

详见 docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md。
EOF
)"
git log --oneline -2
```

预期：commit 落定。git log 显示 commit 1 和 2。

---

## 任务 3: 同步 Schema（Commit 3）

**Files:**
- Modify: `AGENT.md`（line ~11 提及"按 ai-coding / aigc / frontend / obsidian 分类"，line ~42 目录树块）
- Modify: `.claude/commands/ingest.md`（line ~24 一级目录提示）
- Modify: `index.md`（手写 header 块如 `## AI Coding` 重排为新分类）
- Modify: `log.md`（顶部加 reorganize 警告条）

- [ ] **Step 3.1: 改 AGENT.md 的分类描述句（line ~11）**

读 AGENT.md 找到这行：
```
- `wiki/`：精华层，LLM **拥有可改**。从 sources 抽取的概念页面，按 ai-coding / aigc / frontend / obsidian 分类。
```

改为：
```
- `wiki/`：精华层，LLM **拥有可改**。从 sources 抽取的概念页面，按 agent-engineering / claude-code / skills / retrieval / frontend / business / obsidian 分类（部分一级下有二级子目录，详见目录树）。
```

- [ ] **Step 3.2: 改 AGENT.md 的目录树块（line ~42）**

找到：
```
├── wiki/                         # 可改精华
│   ├── ai-coding/ aigc/ frontend/ obsidian/
│   └── _orphans/                 # lint 检测出的孤儿暂存
```

改为：
```
├── wiki/                         # 可改精华
│   ├── agent-engineering/        # philosophy / context / workflow / code-review
│   ├── claude-code/              # Claude Code & 同类 CLI 工具系
│   ├── skills/                   # Agent Skills 生态（跨工具资产）
│   ├── retrieval/                # rag / browser
│   ├── frontend/                 # web-platform / network / react-patterns / react-native / ui-libraries
│   ├── business/                 # 商业模式
│   ├── obsidian/                 # Obsidian 语法/工具/方法论
│   └── _orphans/                 # lint 检测出的孤儿暂存
```

- [ ] **Step 3.3: 改 .claude/commands/ingest.md 的目录提示（line ~24）**

读 .claude/commands/ingest.md 找到：
```
   - 路径：`wiki/<domain>/<kebab-case-标题>.md`，domain 在 ai-coding / aigc / frontend / obsidian 里选
```

改为：
```
   - 路径：`wiki/<domain>/[<sub>/]<kebab-case-标题>.md`。一级 domain 与（如有）二级 sub 选择如下：
     - `agent-engineering/`（4 个二级必选）：`philosophy/`（哲学/范式/思想）、`context/`（上下文与缓存工程）、`workflow/`（工作流与 agent 行为模式）、`code-review/`（CR 与 lint）
     - `claude-code/`（平铺）：Claude Code & 同类 CLI 工具系（hooks、settings、handoff、coordinator-类落地等）
     - `skills/`（平铺）：Agent Skills 规范、编写实践、Skills 集（superpowers/baoyu 等）
     - `retrieval/`（2 个二级必选）：`rag/`（rag/agentic-rag/graph-rag/hybrid-retrieval）、`browser/`（agent-browser/browser-use/cdp）
     - `frontend/`（5 个二级必选）：`web-platform/`（运行时/DOM API）、`network/`（HTTP/QUIC 等协议）、`react-patterns/`（React 状态/effect 模式）、`react-native/`（RN 组件与虚拟列表）、`ui-libraries/`（shadcn/headless-ui/scrollbar 等）
     - `business/`（平铺）：商业模式/盈利模式
     - `obsidian/`（平铺）：Obsidian 语法/工具/方法论
```

- [ ] **Step 3.4: 改 index.md 的分类 header**

策略：保留 index.md 的 frontmatter + 顶部 callout/Bases embed 等"非分类列表"内容；只重写"## AI Coding ... ## Obsidian"那段手写 wikilink 列表。用下面的 helper script 从当前 wiki/ 实际文件 + frontmatter title 生成新分类块的纯净文本，再粘贴进 index.md 替换旧块。

先读 index.md，找到旧分类区段的起止（通常从第一个 `## AI Coding` 开始，到文件结尾或 Bases embed 之前）：

```bash
rg -n '^## ' index.md
```

记下需要替换的行号区间。

然后跑生成器：

```bash
python3 - <<'PYEOF' > /tmp/new-index-section.md
import os, re

TOP_ORDER = [
    ("agent-engineering", "Agent Engineering"),
    ("claude-code", "Claude Code（CLI 工具系）"),
    ("skills", "Skills（生态）"),
    ("retrieval", "Retrieval"),
    ("frontend", "Frontend"),
    ("business", "Business"),
    ("obsidian", "Obsidian"),
]
SUB_ORDER = {
    "agent-engineering": ["philosophy", "context", "workflow", "code-review"],
    "retrieval": ["rag", "browser"],
    "frontend": ["web-platform", "network", "react-patterns", "react-native", "ui-libraries"],
}

bins = {top: ([], {sub: [] for sub in SUB_ORDER.get(top, [])}) for top, _ in TOP_ORDER}

for dp, _, files in os.walk("wiki"):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        path = os.path.join(dp, fn)
        rel = os.path.relpath(path, "wiki")
        if rel.startswith("_orphans/"):
            continue
        rel_no_ext = rel[:-3]
        parts = rel_no_ext.split("/")
        top = parts[0]
        if top not in bins:
            continue
        title = parts[-1]
        with open(path, encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if m:
            title = m.group(1).strip().strip('"\'')
        flat, sub_dict = bins[top]
        if top in SUB_ORDER and len(parts) >= 2 and parts[1] in sub_dict:
            sub_dict[parts[1]].append((rel_no_ext, title))
        else:
            flat.append((rel_no_ext, title))

for top, ttl in TOP_ORDER:
    flat, sub_dict = bins[top]
    if not flat and not any(sub_dict.values()):
        continue
    print(f"## {ttl}\n")
    if top in SUB_ORDER:
        for sub in SUB_ORDER[top]:
            entries = sorted(sub_dict[sub])
            if not entries:
                continue
            print(f"### {sub}\n")
            for p, t in entries:
                print(f"- [[wiki/{p}|{t}]]")
            print()
    else:
        for p, t in sorted(flat):
            print(f"- [[wiki/{p}|{t}]]")
        print()
PYEOF

cat /tmp/new-index-section.md | head -30
wc -l /tmp/new-index-section.md
```

预期：生成约 7 个 `## ` header + 8 个 `### ` sub-header（agent-engineering 4 + retrieval 2 + frontend 5 = 11，但只在有内容的子目录下出现）+ 137 行 wikilink，总行数约 170 行。

然后用 Edit 工具，把 index.md 里从第一个 `## ` header 到分类列表末尾（如有 Bases embed `![[xxx.base...]]`，则到 Bases 块之前）的内容，整块替换成 `/tmp/new-index-section.md` 的内容。

如果 index.md 末尾还有 Bases embed 等非分类内容，确保不被 helper 覆盖——helper 只生成"分类 + wikilink"块，其他内容由你手动保留。

- [ ] **Step 3.5: 在 log.md 顶部加 reorganize 警告条**

读 log.md，在 frontmatter 之后、第一条日志之前插入：

```markdown
> [!warning] 路径迁移
> 2026-04-28 完成 wiki/ 目录重组（详见 docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md）。本日期之前的日志条目里的 wikilink 全路径已过期（仅文件名形式的 `[[xxx]]` 不受影响）。想看历史路径用 `git log -- wiki/<old-path>`。
```

- [ ] **Step 3.6: 验证 schema 改动后整个 vault 没有新的悬空 wikilink**

重跑 Task 2.5 的悬空检测脚本：

```bash
python3 - <<'PYEOF'
import os, re, sys
ROOTS = ["wiki", "sources"]
PAT = re.compile(r'\[\[wiki/([^\]\|]+)')
broken = []
for root in ROOTS:
    for dp, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    for m in PAT.finditer(line):
                        target = f"wiki/{m.group(1)}.md"
                        if not os.path.isfile(target):
                            broken.append(f"{path}:{i}: -> {target}")

# 同时检查 index.md（不在 ROOTS 内但很重要）
for path in ["index.md"]:
    if not os.path.isfile(path):
        continue
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            for m in PAT.finditer(line):
                target = f"wiki/{m.group(1)}.md"
                if not os.path.isfile(target):
                    broken.append(f"{path}:{i}: -> {target}")

if broken:
    print("BROKEN wikilinks:")
    print("\n".join(broken))
    sys.exit(1)
print(f"PASS: all [[wiki/X]] links resolve to existing files")
PYEOF
```

预期：`PASS`

- [ ] **Step 3.7: 提交 commit 3**

```bash
git add AGENT.md .claude/commands/ingest.md index.md log.md
git commit -m "$(cat <<'EOF'
docs: 同步 schema 与索引到新 wiki 目录结构

- AGENT.md：分类描述与目录树重画
- .claude/commands/ingest.md：domain 提示改写为含二级子目录的完整指引
- index.md：手写 header 重排为 7 个新一级分类
- log.md：顶部加 2026-04-28 路径迁移警告
EOF
)"
git log --oneline -3
```

预期：commit 落定。git log 显示 commit 1、2、3。

---

## 任务 4: PR 与合并

- [ ] **Step 4.1: push branch**

```bash
git push -u origin wiki-reorg-2026-04
```

预期：远程分支建立。

- [ ] **Step 4.2: 开 PR**

```bash
gh pr create --title "refactor: 重组 wiki/ 目录结构" --body "$(cat <<'EOF'
## Summary

按 [spec](docs/superpowers/specs/2026-04-28-wiki-reorganization-design.md) 重组 wiki/：

- 一级目录从 4 个改为 8 个（agent-engineering / claude-code / skills / retrieval / frontend / business / obsidian / _orphans）
- ai-coding/ frontend/ retrieval/ 引入二级子目录
- 117 文件 mv + 362 wikilink 重写 + 1 个 sources 反向引用修复 + AGENT.md / ingest.md / index.md / log.md 同步

## 提交结构

- `chore: 准备 wiki 重组脚本` — 添加 scripts/reorg-wiki.py
- `refactor: 重组 wiki/ 目录结构（117 文件 mv + 362 wikilink 重写）` — 跑脚本结果
- `docs: 同步 schema 与索引到新 wiki 目录结构` — schema 文件改动

## Test plan

- [ ] git stat 显示 117 个 R（rename）
- [ ] `find wiki -name '*.md' | wc -l` = 138
- [ ] `rg -c '\[\[wiki/(ai-coding|aigc)/' wiki/ sources/` 无输出
- [ ] 自定义脚本验证所有 [[wiki/X]] 都能解析（见 spec §4）
- [ ] Obsidian graph view 目测新结构图合理
- [ ] 5 个枢纽页（harness-engineering / claude-code / agent-skills / vibe-coding / agentic-coding）链接全部能跳转
EOF
)"
```

预期：返回 PR URL。

- [ ] **Step 4.3: 软验证—Obsidian graph view 目测**

提示用户：

> 请在 Obsidian 里打开本 vault，到 graph view 目测一下：
> 1. 同一二级目录下的页面应该形成聚簇
> 2. 跨二级的连边应集中在合理的"桥梁页"（如 harness-engineering 跨 philosophy/workflow）
> 3. 没有孤立的死链节点
>
> 同时点开 5 个枢纽页（harness-engineering、claude-code、agent-skills、vibe-coding、agentic-coding）确认所有链接能跳。OK 后说 ok 进入 self-merge。

等待用户确认。

- [ ] **Step 4.4: self-merge PR**

```bash
gh pr merge --merge --delete-branch
git checkout main
git pull
```

预期：PR merge 进 main，本地分支清理，main 同步到最新。

- [ ] **Step 4.5: 恢复 stashed plugin state**

```bash
git stash list
git stash pop
git status
```

预期：`.obsidian/plugins/manual-sorting/data.json` 回到 modified 状态。提示用户：plugin 内部排序状态会过期，请在 Obsidian 里重新拖几次让 plugin 重建索引；或直接 commit 该 modified 状态接受当前快照。

---

## 完成标准

- [ ] PR merge 进 main
- [ ] `git log --oneline | head -5` 显示 3 个 reorg commit
- [ ] Obsidian 重启 vault 后 graph view 正常
- [ ] 任意一个 wiki 页面（如 [[wiki/agent-engineering/philosophy/harness-engineering]]）打开后所有出链能跳

## Out of Scope（提醒）

- 仅文件名 wikilink 二义陷阱治理（spec §Out of Scope）
- manual-sorting plugin 排序状态迁移（接受过期）
- AI Code Review / ultrareview（self-merge 即可）

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
                    # Plain forms
                    content = content.replace(f"[[wiki/{old}|", f"[[wiki/{new}|")
                    content = content.replace(f"[[wiki/{old}]]", f"[[wiki/{new}]]")
                    # Obsidian markdown-table form: pipe is escaped as \| inside table cells
                    content = content.replace(f"[[wiki/{old}\\|", f"[[wiki/{new}\\|")
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

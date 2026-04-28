---
title: "youzing/wasc-search-skill"
source: "https://github.com/youzing/wasc-search-skill"
author:
published:
created: 2026-04-28
description: "Contribute to youzing/wasc-search-skill development by creating an account on GitHub."
tags:
  - "clippings"
---
## WASC 低成本高精度搜索 Skill

> 世界AI技能锦标赛 — 2026年4月赛题：低成本高精度搜索

一个基于 **Retrieval-Augmented Generation (RAG)** 范式（ [Lewis et al., NeurIPS 2020](https://arxiv.org/abs/2005.11401) ）的生产级 MCP Skill。通过多源异构检索融合 + LLM 合成，以 **~3,350 tokens/次** 的超低成本（比常规 RAG 方案低 65-75%）返回 **带逐条引用的结构化答案** 。

## 核心能力

| 指标 | 数值 |
| --- | --- |
| 单次查询 token 消耗 | ~3,350（传统 RAG 方案 10,000+） |
| 搜索源 | 3 个异构 API 源（关键词 + 混合检索 + 神经语义） |
| 缓存命中响应 | <5ms |
| 冷启动响应 | ~5-8s |
| 容错机制 | 5 级降级， **永不返回空** |

## 解决了什么问题

传统搜索合成方案面临三大挑战： **token 成本高** （全文输入导致 10K+ tokens/次）、 **信息冗余** （多源结果重复但噪声各异）、 **可靠性差** （单一 LLM 调用容易失败或产生幻觉）。

本 Skill 的解法：

1. **异构多源检索** — 融合关键词搜索（Tavily）、混合检索（LangSearch）和神经语义搜索（Exa）三种不同检索范式，通过 **Reciprocal Rank Fusion** ([Cormack et al., SIGIR 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)) 进行公平的跨源排序融合，避免单一检索模型的偏差
2. **渐进式内容精炼** — URL 归一化去重 → Readability 正文提取 → 关键词相关性过滤 → **BM25 段落选择** ([Robertson & Zaragoza, 2009](https://doi.org/10.1561/1500000019); [Lü et al., arXiv:2407.03618](https://arxiv.org/abs/2407.03618))，逐步将原始网页压缩为与查询高度相关的 ~200 字精华段落
3. **忠实引用合成** — 基于 **Citation Faithfulness** ([Huang et al., arXiv:2412.18004](https://arxiv.org/abs/2412.18004)) 的逐条 `[S#]` 引用机制，每条陈述可溯源验证；借鉴 **FaithfulRAG** ([Li et al., arXiv:2506.08938](https://arxiv.org/abs/2506.08938)) 的冲突检测策略，自动标注多源矛盾
4. **结构化输出** — JSON 格式：答案 + 引用列表 + 置信度 + 冲突标注
5. **5 级容错降级** — 即使所有搜索源失败，也用 LLM 训练知识兜底， **确保永不返回空**

## 快速开始

```
# 安装依赖
npm install && npm run build

# 设置 MiniMax API key（比赛环境由主办方提供）
export MINIMAX_API_KEY=your_key

# 启动 MCP Server（stdio 传输）
node dist/src/index.js
```

### MCP 客户端配置

```
{
  "mcpServers": {
    "wasc-search": {
      "command": "node",
      "args": ["dist/src/index.js"],
      "cwd": "/path/to/wasc-search-skill",
      "env": {
        "MINIMAX_API_KEY": "your_key"
      }
    }
  }
}
```

## 架构

本系统采用经典的 **Retrieve → Rerank → Generate** 三阶段 RAG 架构，在每个阶段引入针对性优化：

```
查询输入
  │
  ▼
L1 精确缓存 (SHA256) ──命中──▶ 直接返回 (<5ms)
  │ 未命中
  ▼
场景感知路由（政策法规 / 行业信息 / 学术文献 / 通用）
  │
  ▼
╔══════════════════════════════════════════════╗
║ Stage 1: 异构多源检索 (Heterogeneous Retrieval) ║
║                                              ║
║ Phase 1: Tavily（关键词检索，LLM 优化摘要）     ║
║   └─ ≥5 条结果？Early-stop 省延迟             ║
║                                              ║
║ Phase 2: LangSearch + Exa（并行）              ║
║   ├─ LangSearch: 混合检索 + 重排序             ║
║   └─ Exa: 神经语义嵌入检索                     ║
║                                              ║
║ 每个源配独立熔断器（Circuit Breaker Pattern）    ║
╚══════════════════════════════════════════════╝
  │
  ▼
╔══════════════════════════════════════════════╗
║ Stage 2: 渐进式精炼 (Progressive Refinement)  ║
║                                              ║
║ URL 归一化去重                                ║
║   ▼                                          ║
║ RRF 跨源排序融合 (k=60)  ← Cormack, SIGIR'09 ║
║   ▼                                          ║
║ Top-10 → Readability 正文提取                  ║
║   ▼                                          ║
║ 关键词相关性过滤                                ║
║   ▼                                          ║
║ BM25 段落选择 (~200字/源) ← Robertson'09      ║
║   ▼                                          ║
║ Token 预算截断 (≤2,200 tokens)                 ║
╚══════════════════════════════════════════════╝
  │
  ▼
╔══════════════════════════════════════════════╗
║ Stage 3: 忠实引用合成 (Faithful Synthesis)     ║
║                                              ║
║ L1: Tool-Call 结构化输出（3次重试+指数退避）     ║
║ L2: 纯文本生成回退（2 次重试）                  ║
║ L3: 最小化 prompt（仅 top-3 源）               ║
║ L4: Snippet 直接拼接（零 LLM 调用）             ║
║ L5: LLM 知识直答（训练知识兜底）                ║
║                                              ║
║ 逐条 [S#] 引用 ← Citation Faithfulness'24    ║
║ 冲突自动检测   ← FaithfulRAG'25              ║
╚══════════════════════════════════════════════╝
  │
  ▼
引用ID验证 → 截断JSON修复 → 缓存写入 → 结构化输出
```

## 测试样例

### 输入

```
{ "query": "2024年大模型行业市场规模" }
```

### 输出

```
{
  "answer": "2024年中国大模型市场规模约215亿元人民币，同比增长120%[S1]。全球市场规模约540亿美元，OpenAI以约35%市场份额领先[S2]。模型推理成本下降约70%，推动企业采用率从15%提升至38%[S2]。国内融资超300亿元，但集中度提高，前10家企业获得80%以上融资额[S4]。",
  "citations": [
    { "id": "S1", "url": "https://www.idc.com/...", "title": "2024年中国大模型市场规模..." },
    { "id": "S2", "url": "https://www.gartner.com/...", "title": "全球大模型市场2024年报告" },
    { "id": "S4", "url": "https://36kr.com/...", "title": "中国大模型融资盘点" }
  ],
  "confidence": "high",
  "conflicts": ""
}
```

## 项目结构

```
wasc-search-skill/
├── src/
│   ├── index.ts                 # MCP Server 入口（stdio）
│   ├── config.ts                # 管道参数配置
│   ├── tools/search.ts          # MCP 工具注册 + 管道编排 + 5 级降级
│   ├── cache/exact.ts           # L1 SHA256 精确缓存
│   ├── sources/
│   │   ├── base.ts              # 两阶段搜索编排 + 熔断器
│   │   ├── tavily.ts            # Tavily Search API（主搜索源）
│   │   ├── langsearch.ts        # LangSearch API（免费无限）
│   │   ├── exa.ts               # Exa 神经语义搜索 API
│   │   └── mock.ts              # 测试用 Mock 数据
│   ├── pipeline/
│   │   ├── url-dedup.ts         # URL 归一化 & 去重
│   │   ├── rrf.ts               # Reciprocal Rank Fusion 融合排序
│   │   ├── extract.ts           # Readability 内容提取
│   │   ├── bm25-select.ts       # BM25 段落选择
│   │   └── token-budget.ts      # Token 预算截断
│   ├── llm/
│   │   ├── minimax.ts           # MiniMax M2.7 客户端（tool-call + 纯文本）
│   │   ├── prompt.ts            # 场景感知 prompt 构建器
│   │   ├── tool-schema.ts       # submit_answer 工具定义
│   │   └── validate.ts          # 引用 & 冲突验证
│   └── router/classify.ts       # 场景分类器
├── tests/                       # 自动化评估框架
├── skill/SKILL.md               # Skill 元数据
├── Dockerfile                   # Ubuntu 24.04 验证环境
├── package.json
└── tsconfig.json
```

## 依赖（6 个核心包，零原生编译）

| 包名 | 用途 |
| --- | --- |
| `@modelcontextprotocol/sdk` | MCP Server 框架 |
| `okapibm25` | BM25 排序 |
| `@mozilla/readability` | 内容提取 |
| `jsdom` | Readability 的 DOM 环境 |
| `opossum` | 熔断器 |
| `undici` | HTTP 连接池 |

## 设计决策与理论依据

**为什么采用异构多源检索而非单一搜索引擎？** 信息检索研究表明，不同检索模型（关键词 vs. 语义嵌入 vs. 混合检索）在不同查询类型上各有优势 ([Thakur et al., NeurIPS 2021 - BEIR Benchmark](https://arxiv.org/abs/2104.08663))。本方案融合三种异构检索范式：Tavily（传统关键词，摘要经 LLM 优化）、LangSearch（混合检索 + 内置重排序）、Exa（基于 Transformer 的神经嵌入检索），通过 RRF 实现公平融合，覆盖更广泛的查询意图。

**为什么选择 RRF 而非 Learning-to-Rank？** [Cormack et al. (SIGIR 2009)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) 证明 RRF 在无需训练数据的条件下优于大多数有监督融合方法，且对异构排序列表天然鲁棒（只依赖排名位置，不依赖分数归一化）。在比赛的零训练数据场景下，RRF 是最优选择。

**为什么用 BM25 段落选择？** 经典的 [BM25 概率检索模型 (Robertson & Zaragoza, 2009)](https://doi.org/10.1561/1500000019) 在短文本段落级检索上仍具有强竞争力。 [BM25S (Lü et al., 2024)](https://arxiv.org/abs/2407.03618) 进一步证实了 BM25 在速度-精度权衡上的优势。本方案用 BM25 从每个网页正文中提取与查询最相关的 ~200 字段落，将 token 输入量降低 75%+ 同时保留核心信息密度。

**为什么 5 级降级而非简单重试？** 借鉴 Nygard 在 *Release It!* 中提出的 **Stability Patterns** （熔断器 + 舱壁隔离 + 降级），结合 RAG 系统的特殊需求设计了 5 级渐进降级。每一级在信息质量和调用成本间取不同平衡点，确保在最极端条件下（所有搜索 API 失败 + LLM Tool-Call 失败）仍能返回有效回答。

**为什么要逐条引用 + 冲突检测？** [Huang et al. (2024)](https://arxiv.org/abs/2412.18004) 指出 RAG 系统中"引用幻觉"是常见问题——模型声称引用了来源但实际内容不匹配。本方案通过 per-claim inline citation 和机械化引用 ID 验证来约束引用忠实度。 [FaithfulRAG (Li et al., 2025)](https://arxiv.org/abs/2506.08938) 的研究进一步启发了冲突检测机制，当多源信息矛盾时自动标注冲突。

## 参考文献

| 论文 | 应用 |
| --- | --- |
| [Lewis et al., "Retrieval-Augmented Generation" (NeurIPS 2020)](https://arxiv.org/abs/2005.11401) | 整体 RAG 架构范式 |
| [Cormack et al., "Reciprocal Rank Fusion" (SIGIR 2009)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 多源排序融合 |
| [Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond" (2009)](https://doi.org/10.1561/1500000019) | 段落级相关性计算 |
| [Lü et al., "BM25S: Efficient BM25 Scoring" (arXiv:2407.03618)](https://arxiv.org/abs/2407.03618) | 高效 BM25 实现 |
| [Thakur et al., "BEIR: A Heterogeneous Benchmark" (NeurIPS 2021)](https://arxiv.org/abs/2104.08663) | 异构检索评估基准 |
| [Huang et al., "Citation Faithfulness in RAG" (arXiv:2412.18004)](https://arxiv.org/abs/2412.18004) | 逐条引用忠实度 |
| [Li et al., "FaithfulRAG" (arXiv:2506.08938)](https://arxiv.org/abs/2506.08938) | 冲突检测策略 |

## 许可证

MIT-0

---

## WASC Low-Cost High-Precision Search Skill

> World AI Skills Championship — April 2026: Low-Cost High-Precision Search

A production-ready MCP Skill built on the **Retrieval-Augmented Generation (RAG)** paradigm ([Lewis et al., NeurIPS 2020](https://arxiv.org/abs/2005.11401)). Delivers **structured, faithfully-cited answers** at **~3,350 tokens per query** — 65-75% less than typical RAG approaches — with 5-level fault tolerance that **never returns empty**.

## Key Contributions

- **Heterogeneous Multi-Source Retrieval**: Fuses keyword (Tavily), hybrid (LangSearch), and neural embedding (Exa) retrieval paradigms — inspired by the [BEIR benchmark (Thakur et al., NeurIPS 2021)](https://arxiv.org/abs/2104.08663) findings on retrieval diversity
- **Reciprocal Rank Fusion**: Training-free cross-source ranking via [RRF (Cormack et al., SIGIR 2009)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- **BM25 Passage Selection**: Sub-document retrieval using [BM25 (Robertson & Zaragoza, 2009)](https://doi.org/10.1561/1500000019) for 75%+ token reduction
- **Faithful Citation Synthesis**: Per-claim `[S#]` inline citations with mechanical ID validation, following [Citation Faithfulness (Huang et al., 2024)](https://arxiv.org/abs/2412.18004)
- **Conflict Detection**: Automatic multi-source contradiction labeling inspired by [FaithfulRAG (Li et al., 2025)](https://arxiv.org/abs/2506.08938)
- **5-Level Graceful Degradation**: tool-call → plain-text → mini-prompt → snippet assembly → direct LLM knowledge

## Quick Start

```
npm install && npm run build
export MINIMAX_API_KEY=your_key
node dist/src/index.js
```

## License

MIT-0
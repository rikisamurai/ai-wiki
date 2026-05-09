---
title: RRF（Reciprocal Rank Fusion）
tags: [rag, retrieval, ranking]
date: 2026-05-09
sources:
  - "[[sources/clippings/youzingwasc-search-skill]]"
last-ingested: 2026-05-09
status: draft
---

RRF（互惠排名融合）是把多个异构排序列表合并成一个全局排序的简单算法：每个文档在第 q 路结果中排第 `rank_q(d)` 位时贡献 `1 / (k + rank_q(d))`，把所有路加起来再排序。`k` 通常取 60。它最大的卖点是**完全不需要训练数据，也不依赖各路打分的归一化**——这让它成为 [[hybrid-retrieval|混合检索]]和多源 [[rag|RAG]] 系统里最常被默认选用的融合方法。

> [!important] 公式 + 默认参数
> ```
> RRF_score(d) = Σ_q  1 / (k + rank_q(d))
> ```
> - `q` 遍历所有"路"（每个搜索源 / 每条改写后的查询 / 每个检索模型）
> - `rank_q(d)` 是文档 `d` 在第 q 路里的排名（1-based；没出现则该项为 0）
> - `k = 60` 是 [Cormack et al. SIGIR 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) 原论文给的经验值，2026 年依然是事实默认

## 为什么是 RRF 而不是别的

> [!compare] RRF vs Learning-to-Rank vs 分数加权融合
> | 方案 | 训练数据 | 异构源鲁棒性 | 实现复杂度 |
> |---|---|---|---|
> | **RRF** | 不需要 | 强（只看排名） | ~10 行 |
> | Learning-to-Rank | 需要标注 | 取决于训练分布 | 中-高 |
> | 分数加权（`α·s1 + β·s2`） | 经验调参 | 弱（分数尺度不同） | 低，但调参痛苦 |

Cormack et al. 的核心结论：**在零训练数据的场景下，RRF 优于绝大多数有监督融合**。这一点在 [[wiki/skills/wasc-search-skill|wasc-search-skill]] 这种比赛 / 冷启动项目里尤其关键——没人给你标注 query-doc 相关性对。

## 两种典型用法

> [!example] 用法 1：多源融合（典型 [[hybrid-retrieval|Hybrid Retrieval]]）
> 把 BM25 召回、向量召回、神经语义召回各自的 top-N 通过 RRF 融合：
>
> ```
> Tavily(关键词) ─top10─┐
> LangSearch(混合) ─top10─┼─→ RRF(k=60) → 融合 top-10 → 进入精排
> Exa(神经) ─top10─┘
> ```
> [[wiki/skills/wasc-search-skill|wasc-search-skill]] 用的就是这种 3 路融合。

> [!example] 用法 2：RAG-Fusion（多查询融合）
> 把同一个用户查询用 LLM 改写成 N 个变体，每个独立检索，再用 RRF 合并——参见 [[hybrid-retrieval|混合检索]]里的"RAG Fusion"段落。这种用法解决的不是源异构，而是查询表达的不确定性。

## 几个常被踩的坑

> [!warning] 把分数当排名喂进 RRF
> RRF 接受的是**排名**（rank），不是分数（score）。如果直接把"BM25 分 12.4 / 向量余弦 0.81"扔进公式，结果毫无意义。先按各自分数排序得到 rank，再代入 RRF。

> [!warning] k 太小或太大都会塌
> - `k = 0`：第 1 名独大（`1/1 = 1.0`），第 10 名几乎没贡献——退化成"只看第一名"。
> - `k = 1000`：所有排名差异被抹平——退化成均匀加权。
>
> 60 是经验上"差异保留 + 长尾不被忽略"的甜点。除非有强理由，不要动。

> [!warning] 不要试图用 RRF 跨"召回阶段"和"精排阶段"
> RRF 是同质排序列表的融合器。把 bi-encoder 召回 top-100 和 cross-encoder 精排 top-10 用 RRF 合并是对它的滥用——精排已经用了更强信号，融合会污染结果。正确做法是**召回阶段并行 N 路 → RRF → 精排单路**。

## 关联

[[hybrid-retrieval|Hybrid Retrieval]] / [[rag|RAG]] / [[agentic-rag|Agentic RAG]] / [[wiki/skills/wasc-search-skill|wasc-search-skill]]

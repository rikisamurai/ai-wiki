---
title: 混合检索（Hybrid Retrieval）
tags: [rag, retrieval, ranking]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/rag/intro]]"
last-ingested: 2026-04-23
status: draft
---

混合检索是 [[rag|RAG]] 里"花最少工程换最多召回质量"的招数——**语义搜索 + 词汇搜索（BM25）的组合永远比单独语义搜索好**。再叠加 cross-encoder 重排序，就能把检索质量推到接近天花板。

> [!important] 为什么"语义 + BM25"互补
> | 检索方式 | 强项 | 弱点 |
> |---|---|---|
> | **语义搜索（向量）** | 同义词、改写、跨语种 | 罕见词、专有名词、精确编号 |
> | **BM25（词汇）** | 精确匹配、专有名词、罕见词 | 同义改写、语义关系 |
>
> 用户查询"2024 年 Q3 营收增长率"时，BM25 能精准命中"Q3"，向量搜索容易把它当成"季度数据"的一类。两个一起用就两边都对。

**三段式检索流水线（事实标准）**

```
查询
  ↓
┌─────────┬─────────┐
│ BM25    │ 向量    │   并行召回 100-200 个候选
└────┬────┴────┬────┘
     ↓         ↓
   合并去重（RRF / 分数融合）
     ↓
   Cross-Encoder 重排序（按真实相关性）
     ↓
   Top-K（通常 K=3-10）→ LLM
```

> [!example] 为什么需要 Cross-Encoder 重排
> 检索阶段用的是 **bi-encoder**——查询和文档分别编码，方便预算向量库索引。速度快但精度有上限。
>
> Cross-Encoder（如 `cross-encoder/ms-marco-MiniLM-L-6-v2`）把"查询 + 文档"一起喂给模型打分——慢得多，但**真实相关性判断好得多**。所以策略是：**bi-encoder 召回 100-200 → cross-encoder 精排 Top-K**。
>
> 这也是 [[claude-code-memory|Claude Code Memory 体系]]里 Sonnet top-5 检索的同样思路——召回宽，精排准。

**RAG Fusion：多查询 + RRF**

把同一个用户查询用 LLM 改写成 N 个变体，每个独立检索，最后用**互惠排名融合（Reciprocal Rank Fusion）**合并：

```
RRF_score(d) = Σ_q  1 / (k + rank_q(d))
```

其中 `k` 通常取 60。**核心收益**：模糊查询（"告诉我合同的事"）能被 LLM 拆成具体术语（"服务等级协议"、"付款条款"、"终止条款"），覆盖面比单查询大得多。

> [!example] HyDE（假设文档嵌入）
> 模糊查询的另一种解法：
>
> ```
> 用户查询很模糊 → LLM 生成"假设性答案"（hypothetical doc）
>                ↓
>          用假设答案的 embedding 去检索真实文档
>                ↓
>          基于真实文档生成最终答案
> ```
>
> 关键洞察：**embedding 空间里，"答案 ↔ 文档"的距离比"问题 ↔ 文档"近**。生成假答案是为了把 query 拉到答案的语义空间。

**生成式结构化搜索**

不是所有数据都能塞进向量库——私有 API、企业数据库、SaaS 后台。这时让 LLM 直接生成 SQL / API 调用，作为检索的另一条腿：

```
用户查询 → LLM → SQL/API → 结构化结果 + 向量召回结果 → 合并 → LLM 答
```

适合财报数据、客户记录、订单系统这类**有 schema 的数据**——硬塞进向量库反而损失结构信息。

**精细化分块（Chunking）**

朴素 RAG 用固定 token 数切块——这会**割裂语义**。生产实践通常用：

- **递归字符切分**（`RecursiveCharacterTextSplitter`）：先按段落 → 再按句子 → 再按字符，保留尽可能大的语义单元
- **基于语义切分**：embedding 相邻片段，相似度突变处切（更慢但更准）
- **结构化切分**：按 markdown header / HTML section / 代码函数边界切

> [!tip] 嵌入模型微调：领域 RAG 的天花板突破口
> 通用 embedding 在领域专用查询上往往表现一般——例如约会应用里"喜欢咖啡"和"讨厌咖啡"在通用 embedding 空间里距离很近，但产品语义里它们要拉远。
>
> 微调自己的 embedding（用领域内的"相似/不相似"对训练）可以**显著提升检索精度**——是花小成本撬动大效果的杠杆。

> [!warning] 不要无脑叠加技术
> 全套技术叠满（Hybrid + Rerank + Fusion + HyDE + 微调 embedding）听起来很美，但**每多一层都增加延迟和复杂度**。实操路径：
>
> 1. 朴素 RAG 跑通基线
> 2. 加 RAGAS 量化检索精度和回答忠实度
> 3. 哪一步最弱补哪一步——通常是 Hybrid + Cross-Encoder Rerank 性价比最高
> 4. 还不够才上 Fusion / HyDE / 微调

**关联**：[[rag|RAG]] / [[agentic-rag|Agentic RAG]] / [[graph-rag|GraphRAG]] / [[claude-code-memory|Claude Code Memory]] / [[wiki/ai-coding/cache-命中率|Cache 命中率]]

---
title: GraphRAG
tags: [rag, graph, llm]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/rag/intro]]"
last-ingested: 2026-04-23
status: stable
---

GraphRAG 用知识图谱补 [[rag|RAG]] 的最大短板——**关系型查询**。向量搜索擅长"找语义相似的文本"，但回答不了"CEO 上一家创业公司如何影响了当前产品架构"这种需要追踪实体关系的问题。GraphRAG 把实体和关系作为一等公民。

> [!important] 向量搜索 vs 图搜索的本质差异
> 向量搜索的相似度是"语义距离"——它能找到"提到 CEO 的段落"和"提到产品架构的段落"，**但无法连接两者**。
>
> 图搜索是"关系遍历"——`(CEO)-[创办过]->(前公司)-[失败原因]->(技术债)-[影响]->(当前架构)`，每一跳都是显式的关系边。多跳查询（multi-hop reasoning）正是 GraphRAG 的主场。

**典型架构**

```
原始文档
   ↓ (实体抽取 + 关系抽取，通常 LLM 完成)
知识图谱（Neo4j / Memgraph / NetworkX）
   ↓ (查询时)
向量召回 ∪ 图遍历 → LLM 合成
```

> [!compare] GraphRAG 适合 vs 不适合
> | 场景 | 为什么 |
> |---|---|
> | ✅ 多跳推理 | "X 间接影响 Y" 需要遍历 N 跳 |
> | ✅ 追溯路径 | 可以告诉用户"答案是怎么推出来的" |
> | ✅ 可审计性 | 每一步关系都能查证 |
> | ✅ 关系密集型领域 | 公司组织、医疗诊断、法律案例 |
> | ❌ 纯语义检索 | "找类似主题的文档"用向量更快更准 |
> | ❌ 文档结构性弱 | 实体抽取困难 → 图质量差 → 检索差 |

> [!example] 量化收益
> 结合向量搜索 + 结构化分类法/本体论时，某些场景检索精度可达 **99%**——朴素 RAG 通常 60%-80%。但代价是：图构建期需要可靠的实体抽取（LLM 调用 + 人工 review），构建成本远高于"切块 + embedding"。

**与 Obsidian 知识图谱的呼应**

[[knowledge-graph|Obsidian 的知识图谱]]是人类手工维护的同类结构——`[[wikilink]]` 就是边、笔记就是节点。GraphRAG 是同样的范式被 LLM 自动化：

| 系统 | 节点 | 边 | 维护者 |
|---|---|---|---|
| Obsidian | 笔记 | wikilink | 人 |
| GraphRAG | 实体 | 关系 | LLM 抽取 + 人审核 |
| MOC（[[moc-索引笔记\|Maps of Content]]） | 主题聚合 | embed | 人 |

启示：如果你已经在用 Obsidian 维护 wiki，把它喂给 GraphRAG 可以**省掉实体抽取这一步最贵的环节**——你已经手工标注好了。

**典型工具栈**

- **Neo4j**：业界事实标准的图数据库，社区版免费
- **Memgraph**：高性能内存图，适合实时查询
- **NetworkX**：Python 原生图库，适合小规模 / 原型
- **LangChain GraphCypherQAChain**：从自然语言生成 Cypher 查询的成熟链路

> [!warning] GraphRAG 的成本陷阱
> - **图构建慢且贵**：N 篇文档需要 N×K 次 LLM 调用做实体/关系抽取
> - **schema 设计是产品决策**：哪些算实体、哪些算关系，决定图能回答什么——这是工程师 + 领域专家的活，不是 AI 能完全代劳
> - **更新困难**：文档更新后图也要增量更新，但实体合并/去重是 hard problem
>
> 实操建议：先做朴素 RAG → 发现"关系型问题答得差" → 再投资 GraphRAG，不要一上来就建图。

**关联**：[[rag|RAG]] / [[agentic-rag|Agentic RAG]] / [[hybrid-retrieval|混合检索]] / [[knowledge-graph|Obsidian 知识图谱]] / [[moc-索引笔记|MOC 索引笔记]]

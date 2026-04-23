---
title: RAG（检索增强生成）
tags: [rag, retrieval, llm]
date: 2026-04-23
sources:
  - "[[sources/posts/aigc/rag/intro]]"
last-ingested: 2026-04-23
status: draft
---

RAG（Retrieval-Augmented Generation）的本质是把"记住事实"和"推理事实"分离——文档存进向量库，查询时把相关片段连同问题一起喂给 LLM。**更新文档后 AI 立刻能用新信息，无需重训**。这一句话解释了为什么所有企业都把 RAG 列为 LLM 落地的第一站。

> [!important] 范式转变：朴素 RAG 已经不够用
> 早期"512-token 切块 + 向量检索 + 拼 prompt"的朴素 RAG 在多跳推理 / 关系型查询 / 细粒度检索上表现差，**生产级应用基本淘汰**。2025-2026 的主流是把六种增强叠加使用——见下面的 6 大方向。

**朴素 RAG 流程（基线）**

```
离线：文档 → 切分 → embedding → 向量库
在线：查询 → 向量化 → Top-K 检索 → prompt 拼装 → LLM 生成 + 引用
```

> [!example] 50 行起步的最小 RAG
> ```python
> docs = PyPDFLoader("my_doc.pdf").load()
> chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
> vectorstore = FAISS.from_documents(chunks, HuggingFaceEmbeddings())
> retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
> ```
> Python + LangChain + FAISS + 本地 Ollama 模型——0 成本。这是每个 RAG 入门者的第一关。

**关键组件选型**

| 类别 | 主流选项 |
|---|---|
| **框架** | LangChain、LlamaIndex |
| **向量数据库** | FAISS（本地）、Pinecone、Weaviate、Chroma、Milvus |
| **Embedding** | OpenAI text-embedding-3、BGE、sentence-transformers |
| **LLM** | GPT-4o / Claude / Llama 3 / Qwen（Ollama 本地） |

**六大增强方向（从朴素 → 生产级）**

> [!compare] 六种方向 × 解决问题
> | 方向 | 解决什么 | 代表概念 |
> |---|---|---|
> | [[agentic-rag\|Agentic RAG]] | 单轮检索不够 | LLM 当 reasoning engine + 循环 |
> | [[graph-rag\|GraphRAG]] | 关系型查询 | 实体+关系作为 first-class |
> | [[hybrid-retrieval\|混合检索 + Rerank]] | 召回质量 | BM25 + 语义 + cross-encoder |
> | **多模态 RAG（Vision RAG）** | 图表/视频 | Qwen3-VL-Embedding/Reranker |
> | **模块化 RAG** | 工程可演进性 | 把流程拆成可替换模块 |
> | **工程优化** | 召回 + 准确 | HyDE、查询重写、RAG Fusion |
>
> 实际系统通常**叠加多个方向**——例如 Agentic 循环里嵌入 Hybrid 检索 + 重排序，再加 GraphRAG 处理关系问题。

**多模态 RAG（Vision RAG）**

2026 年初 **Qwen3-VL-Embedding / Qwen3-VL-Reranker** 把文本/图像/视频映射到统一语义空间——从"OCR 找关键字"进化到"语义理解视觉数据"。金融图表、多媒体内容、产品截图等场景的核心解。

**模块化 RAG**

把整条流水线拆成可替换模块：查询处理 / 专用检索 / 重排序与过滤 / 推理生成。每个模块独立演进——和 [[wiki/ai-coding/harness-engineering|Harness Engineering]] 思路同源：**别建大单体，建可换的小件**。

**学习路径（6 级渐进）**

> [!tip] 由浅入深的 6 个项目
> 1. 🟢 **基础 PDF 问答**：LangChain + FAISS + Ollama，2 小时上手
> 2. 🟡 **多模态 RAG**：Unstructured 处理图表 + 多模态 LLM
> 3. 🟡 **混合检索 + Rerank**：BM25 + 语义召回 100-200 → cross-encoder 重排（参考 [[hybrid-retrieval|混合检索]]）
> 4. 🟡 **查询变换 + RAG Fusion**：模糊查询 → N 个具体 query → RRF 合并
> 5. 🔴 **Agentic RAG**：LangGraph 智能体循环（参考 [[agentic-rag|Agentic RAG]]）
> 6. 🔴 **GraphRAG**：Neo4j 实体+关系（参考 [[graph-rag|GraphRAG]]）
>
> 实操建议：先 2 小时搭基线 → 加 RAGAS 评估 → 逐步加料 → 上 LangSmith 做可观测性。

> [!warning] RAG 不是银弹
> - **检索质量决定一切**：Top-K 错了，后面 LLM 无法补救
> - **embedding 不微调天花板很低**：通用 embedding 区分不开"喜欢咖啡"和"讨厌咖啡"
> - **拒答能力**：检索不到相关文档时让 LLM 老实说"不知道"，不要瞎编
> - **多文档合成**：跨文档矛盾或互补信息的处理是工程重点

**关联**：[[agentic-rag|Agentic RAG]] / [[graph-rag|GraphRAG]] / [[hybrid-retrieval|混合检索]] / [[claude-code-memory|Claude Code Memory]] / [[knowledge-graph|知识图谱]]

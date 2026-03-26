

## 2026


### **从"朴素 RAG"到"高级 RAG"的核心演进**

早期 RAG 的典型做法是把文档切成 512-token 的块，用 embedding 模型编码后存入向量数据库，查询时做相似性检索然后丢给 LLM 生成回答。 [# The State of RAG 2026: From “Vibe Checking” to Reasoning](https://medium.com/aiguys/the-state-of-rag-2026-from-vibe-checking-to-reasoning-cee536ae3f02)这种方式在多跳推理、关系型问题、以及细粒度检索上表现很差。这种"朴素 RAG"在生产级应用中已经基本被淘汰了。 [# The Evolution of RAG and AI Technology Trends for 2026](https://explore.n1n.ai/blog/evolution-of-rag-and-ai-trends-2026-2026-03-10)

目前最前沿的做法主要集中在以下几个方向：

**1. Agentic RAG（智能体驱动的 RAG）**

这是 2025–2026 年最大的范式转变。与传统 RAG 的线性管道不同，Agentic RAG 是一个循环结构——LLM 充当推理引擎，自主决定检索策略；如果首轮检索不够，智能体会重新构造查询并再次检索。 [N1n](https://explore.n1n.ai/blog/evolution-of-rag-and-ai-trends-2026-2026-03-10)

Agentic RAG 将自主 AI 智能体嵌入 RAG 流程，利用反思（reflection）、规划（planning）、工具调用（tool use）和多智能体协作等设计模式，动态管理检索策略并迭代精炼上下文理解。 [arXiv](https://arxiv.org/abs/2501.09136)

具体实现模式包括：

- **ReAct 风格推理**：智能体执行"思考 → 行动（如搜索）→ 观察 → 再思考"的循环，适用于单次检索不够的场景。 [Data Nucleus](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026)
- **多智能体并行**：多个智能体并行在不同系统中搜索，最后由一个聚合器汇总分析原始结果。 [Langwatch](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)类似 Deep Research 的做法。
- **Self-RAG**：让模型自己决定何时需要检索，并对自身输出进行批判性评估，从而提高事实准确性。 [Data Nucleus](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026)
- **层级化 Agentic RAG**：将关键词搜索、语义搜索、块级阅读等多粒度检索接口暴露给模型，让它动态选择检索策略。在 HotpotQA 上达到 94.5% 准确率。 [GitHub](https://github.com/aishwaryanr/awesome-generative-ai-guide/blob/main/research_updates/rag_research_table.md)



**2. GraphRAG（图增强 RAG）**

标准向量搜索擅长找相似文本，但在关系型数据上力不从心。例如"CEO 上一家创业公司如何影响了当前产品架构"这类问题，向量搜索可能分别找到关于 CEO 和架构的文档，但无法把"影响"这层关系连接起来。GraphRAG 通过将实体和关系映射到知识图谱来解决这个问题。 [N1n](https://explore.n1n.ai/blog/evolution-of-rag-and-ai-trends-2026-2026-03-10)

GraphRAG 将实体和关系作为一等公民，支持多跳查询，能精确追踪答案的推导路径，增强了可解释性和可审计性。 [Neo4j](https://neo4j.com/blog/developer/graphrag-and-agentic-architecture-with-neoconverse/)结合向量搜索和结构化分类法/本体论，在某些场景下检索精度可达 99%。 [Squirro](https://squirro.com/squirro-blog/state-of-rag-genai)


**3. 混合检索（Hybrid Retrieval）**

实践证明，语义搜索和词汇搜索（BM25）的混合使用效果优于单独的语义搜索。 [Langwatch](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)先用混合检索获取候选，再用交叉编码器（cross-encoder）重排序，按真实相关性排序。 [Data Nucleus](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026)

此外还有生成式结构化搜索——用 AI 生成 API 调用参数或 SQL 查询来探索数据，适合处理无法放入向量数据库的私有 API 或企业数据。 [Langwatch](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)



**4. 多模态 RAG（Vision RAG）**

2026 年初，Qwen3-VL-Embedding 和 Qwen3-VL-Reranker 系列的发布推动了多模态 RAG 的突破，将文本、图像、视频映射到统一的语义空间，从简单的 OCR 检索进化到对视觉数据的真正语义理解。 [Towards AI](https://pub.towardsai.net/building-state-of-the-art-vision-enabled-rag-pipelines-2026-725ab2089595)这对于金融文档中的图表分析、多媒体内容检索等场景尤为关键。



**5. 模块化 RAG（Modular RAG）**

模块化 RAG 将整个流程拆解为可替换的专业模块：查询处理模块（查询重写、分类、扩展）、专用检索模块（混合检索、知识图谱集成）、重排序与过滤模块（基于证据的评分、可信度评估）、以及具有专门推理能力的生成模块（链式思维提示、证据整合）。 [Springer](https://link.springer.com/article/10.1007/s00521-025-11666-9)


**6. 关键的工程优化手段**

在上述架构之上，还有一系列重要的工程技术：

- **HyDE（假设文档嵌入）**：对于模糊查询，先让 LLM 生成一个"假设性答案"来引导检索，再基于真实文档进行验证。 [Data Nucleus](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026)
- **查询重写与扩展**：将用户查询改写或扩展为多个变体，提高召回率。 [Prompt Engineering Guide](https://www.promptingguide.ai/research/rag)
- **RAG Fusion**：将 RAG 与互惠排名融合（RRF）结合，把来自多个检索源或不同查询变体的排名统一成单一排名。 [Medium](https://medium.com/data-science-collective/advanced-rag-techniques-concepts-e0b67366c5cf)
- **精细化分块策略**：基于语义而非固定 token 数进行切分，保留文档上下文。
- **嵌入模型微调**：在特定领域（如约会应用中让"喜欢咖啡"和"讨厌咖啡"在嵌入空间中拉远距离），微调自己的嵌入模型可以显著提升效果。 [Langwatch](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)




### 小白学 RAG


**一、RAG 的核心流程（怎么做）**

RAG 的本质是：与其让 LLM 凭记忆回答（容易产生幻觉），不如先把你的文档存入一个能理解语义的向量数据库，当用户提问时检索相关文档，再把文档和问题一起交给 LLM 生成回答。这就把"记住事实"和"推理事实"分离了——更新文档后 AI 立刻就能获取新信息，无需重新训练。 [DEV Community](https://dev.to/gautamvhavle/building-production-rag-systems-from-zero-to-hero-2f1i)

一个典型的 RAG 流程包含以下阶段：

**阶段一：数据准备（离线）**

文档加载与元数据提取 → 文本切分与分块策略（设定块大小、重叠量）→ 用 embedding 模型生成向量 → 将向量和元数据存入向量数据库。 [DEV Community](https://dev.to/pavanbelagatti/learn-how-to-build-reliable-rag-applications-in-2026-1b7p)

**阶段二：查询与生成（在线）**

将用户查询向量化 → 在向量库中做相似性检索（Top-K）→ 用检索到的上下文和用户查询构造 prompt → LLM 生成回答并附上来源。 [DEV Community](https://dev.to/pavanbelagatti/learn-how-to-build-reliable-rag-applications-in-2026-1b7p)

**关键组件选型：**

- **框架**：LangChain、LlamaIndex 是最主流的两个
- **向量数据库**：FAISS（本地免费）、Pinecone、Weaviate、Chroma、Milvus
- **Embedding 模型**：OpenAI text-embedding-3、BGE、sentence-transformers（本地免费）
- **LLM**：GPT-4o / Claude / 本地模型（Llama 3、Qwen 等通过 Ollama 运行）

最小可行的 RAG 系统只需要大约 50 行 Python 代码、一个免费的 embedding 模型和 FAISS，启动成本为零。 [DEV Community](https://dev.to/gautamvhavle/building-production-rag-systems-from-zero-to-hero-2f1i)


**二、推荐的上手项目（由浅入深）**

🟢 Level 1：基础 RAG — 与 PDF 对话

用 Ollama 在本地运行 Llama 模型，用 LangChain 的 PyPDF 加载并切分 PDF，创建 embedding 并存入内存向量库（如 DocArray），然后搭建检索链来获取相关片段并生成回答。 [KDnuggets](https://www.kdnuggets.com/5-fun-rag-projects-for-absolute-beginners)这是每个初学者的第一个项目，能帮你理解整个 pipeline 的基本逻辑。

**你需要的技术栈：** Python + LangChain + Ollama + FAISS/Chroma

**示意代码骨架：**

python

```python
# 1. 加载文档
from langchain.document_loaders import PyPDFLoader
docs = PyPDFLoader("my_doc.pdf").load()

# 2. 切分
from langchain.text_splitter import RecursiveCharacterTextSplitter
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)

# 3. 向量化 + 存储
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
vectorstore = FAISS.from_documents(chunks, HuggingFaceEmbeddings())

# 4. 构建检索链
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. 接入 LLM 生成回答
# ... 用 retriever + LLM + prompt template 组合即可
```


🟡 Level 2：多模态 RAG — 处理图表和图片

用 LangChain 和 Unstructured 库处理 PDF 中的混合内容（文本、图片、表格），将它们嵌入统一向量空间，然后用多模态 LLM 回答类似"解释第 5 页的图表"这样的问题。 [KDnuggets](https://www.kdnuggets.com/5-fun-rag-projects-for-absolute-beginners)

---

🟡 Level 3：混合检索 + 重排序

先用混合搜索（语义 + 关键词 BM25）检索 100-200 个候选文档，再加载 cross-encoder 重排序模型（如 `cross-encoder/ms-marco-MiniLM-L-6-v2`）对查询-文档对打分，按真实相关性排列。 [Dextra Labs](https://dextralabs.com/blog/rag-projects-retrieval/)这个项目能让你深刻理解为什么"检索质量决定一切"。

---

🟡 Level 4：查询变换与 RAG Fusion

用户查询往往是模糊的（比如"告诉我合同的事"）。查询变换可以把它扩展为具体的术语："服务等级协议""付款条款""终止条款"。 [Dextra Labs](https://dextralabs.com/blog/rag-projects-retrieval/)结合 RAG Fusion（用 RRF 合并多查询的排名结果），显著提升召回率。

---

🔴 Level 5：Agentic RAG — 智能体驱动

构建一个基于 LangGraph 的 RAG 管道：用户提问 → 智能体先判断已有知识能否回答 → 不能的话路由到本地文档或互联网搜索 → 检索后评估答案质量 → 不够好则重新构造查询再检索。 [DataCamp](https://www.datacamp.com/tutorial/agentic-rag-tutorial)这是目前生产级 RAG 的主流架构。

**推荐工具：** LangGraph（构建智能体工作流）+ LangSmith（调试和监控）

---

🔴 Level 6：GraphRAG — 知识图谱增强

用 Neo4j 构建知识图谱，把实体和关系作为检索的一等公民。课程通常会引导你构建一个电影知识图谱，但这些技术可以应用到任何关系型数据场景——公司组织结构、医疗诊断等。 [Class Central](https://www.classcentral.com/report/best-rag-courses/)


三、推荐的学习资源

|资源|适合人群|特点|
|---|---|---|
|DEV.to "Building RAG Systems: From Zero to Hero" [DEV Community](https://dev.to/gautamvhavle/building-production-rag-systems-from-zero-to-hero-2f1i)|完全初学者|免费，50 行代码起步|
|KDnuggets "5 Fun RAG Projects for Absolute Beginners" [KDnuggets](https://www.kdnuggets.com/5-fun-rag-projects-for-absolute-beginners)|初学者|5 个渐进式项目|
|DataCamp "Agentic RAG: Step-by-Step Tutorial" [DataCamp](https://www.datacamp.com/tutorial/agentic-rag-tutorial)|中级|含完整 LangGraph demo|
|Dextra Labs "10 RAG Projects That Actually Teach You Retrieval" [Dextra Labs](https://dextralabs.com/blog/rag-projects-retrieval/)|中高级|从向量搜索到生产级架构|
|DEV.to "Learn How to Build Reliable RAG Applications in 2026" [DEV Community](https://dev.to/pavanbelagatti/learn-how-to-build-reliable-rag-applications-in-2026-1b7p)|中级|LangChain + SingleStore 实战|

四、一个实用建议

如果你是第一次接触 RAG，我推荐的路径是：

1. **先花 2 小时**：用 LangChain + FAISS + 本地模型（Ollama）搭一个最简单的 PDF 问答系统
2. **加上评估**：用 RAGAS 框架评估你的检索精度和回答忠实度，这样你能量化改进效果
3. **逐步加料**：混合检索 → 重排序 → 查询变换 → Agentic 循环
4. **面向生产**：加入 LangSmith 做可观测性，处理边界情况（无相关文档时的拒答、多文档合成等）

每一步都有对应的开源模板可以参考

https://claude.ai/public/artifacts/a60d7b29-1d38-4e1d-aa17-0291a8e8ade1

<iframe src="https://claude.site/public/artifacts/a60d7b29-1d38-4e1d-aa17-0291a8e8ade1/embed" title="Claude Artifact" width="100%" height="600" frameborder="0" allow="clipboard-write" allowfullscreen></iframe>
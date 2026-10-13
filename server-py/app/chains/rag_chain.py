import os
import re

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.db.postgres import PG_CONNECTION_STRING
from app.models.deepseek import create_model, create_model_from_config
from app.models.embedding import embeddings

COLLECTION_NAME = "knowledge_embeddings"

_KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge")
_KNOWLEDGE_FILES = ["products.md", "policies.md"]

_retriever = None
_vector_store_error = None


class _KeywordRetriever:
    """无 Embedding / 向量库不可用时的本地降级检索。

    使用中文 bigram 与英文数字 token 的重叠度打分，取相似度最高的前 k 个片段。
    对商品名、型号（如 KFR-72LW/G888J-X1）这类精确词匹配效果良好。
    """

    def __init__(self, k: int = 4):
        self.k = k
        self._docs = self._load_docs()

    @staticmethod
    def _load_docs():
        docs = []
        for file in _KNOWLEDGE_FILES:
            path = os.path.join(_KNOWLEDGE_DIR, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                continue
            docs.append(Document(page_content=content, metadata={"source": file}))
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(docs)

    @staticmethod
    def _tokens(text: str) -> set:
        text = (text or "").lower()
        tokens = {text[i : i + 2] for i in range(len(text) - 1) if text[i : i + 2].strip()}
        tokens.update(re.findall(r"[a-z0-9]+", text))
        return tokens

    def invoke(self, query: str):
        query_tokens = self._tokens(query)
        if not query_tokens:
            return self._docs[: self.k]
        scored = []
        for doc in self._docs:
            score = len(query_tokens & self._tokens(doc.page_content))
            scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        results = [doc for score, doc in scored[: self.k] if score > 0]
        return results or self._docs[: self.k]


def _get_retriever():
    """惰性初始化检索器：优先向量库，未配置 Embedding 或库不可用时降级为本地关键词检索。"""
    global _retriever, _vector_store_error
    if _retriever is not None:
        return _retriever

    if embeddings is not None:
        try:
            vector_store = PGVector(
                embeddings=embeddings,
                collection_name=COLLECTION_NAME,
                connection=PG_CONNECTION_STRING,
                use_jsonb=True,
            )
            _retriever = vector_store.as_retriever(search_kwargs={"k": 4})
            return _retriever
        except Exception as err:
            _vector_store_error = err
            print(f"[rag_chain] 向量库初始化失败，降级为本地关键词检索: {err}")
    else:
        print("[rag_chain] 未配置 Embedding Key，使用本地关键词检索")

    _retriever = _KeywordRetriever(k=4)
    return _retriever

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是服满海电商平台的专业客服助手小购，同时也是用户的贴心购物顾问。

【服务心态】
1. 语气温和、耐心、亲切、有同理心，称呼用户为"亲"
2. 实事求是，只依据下面知识库内容作答；知识库没有的内容如实告知，绝不编造
3. 学会共情：根据用户语气揣摩其真实想法与期待，给予贴心回应

【回答要求】
4. 简洁直接，先给结论再补充；商品咨询按「型号 / 价格 / 核心卖点」要点作答，条理清晰
5. 默认回答控制在 150 字以内，用户追问细节时再展开
6. 若有购买意向，可简要推荐并提供关键信息，帮助用户快速决策

知识库内容：
{context}""",
        ),
        ("human", "{question}"),
    ]
)


def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


_model = create_model(temperature=0)

# 标准 RAG Chain
rag_chain = (
    {
        "context": lambda input: format_docs(_get_retriever().invoke(input["question"])),
        "question": lambda input: input["question"],
    }
    | rag_prompt
    | _model
    | StrOutputParser()
)


def _build_answer_chain(model_config=None, streaming=False):
    model = create_model_from_config(model_config, temperature=0, streaming=streaming)
    return (
        (lambda input: {"context": format_docs(input["docs"]), "question": input["question"]})
        | rag_prompt
        | model
        | StrOutputParser()
    )


_answer_chain = _build_answer_chain()


def _sources_of(question: str):
    docs = _get_retriever().invoke(question)
    sources = [
        {"content": doc.page_content[:100] + "...", "source": doc.metadata.get("source")}
        for doc in docs
    ]
    return docs, sources


def _with_sources(input, model_config=None):
    docs, sources = _sources_of(input["question"])
    chain = _build_answer_chain(model_config)
    answer = chain.invoke({"docs": docs, "question": input["question"]})
    return {"answer": answer, "sources": sources}


class _RagChainWithSources:
    """带来源信息的 RAG Chain"""

    def invoke(self, input: dict) -> dict:
        return _with_sources(input, input.get("model"))


ragChainWithSources = _RagChainWithSources()
rag_chain_with_sources = ragChainWithSources

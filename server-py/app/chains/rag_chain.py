from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector

from app.db.postgres import PG_CONNECTION_STRING
from app.models.deepseek import create_model, create_model_from_config
from app.models.embedding import embeddings

COLLECTION_NAME = "knowledge_embeddings"

_retriever = None
_vector_store_error = None


def _get_retriever():
    """惰性初始化向量库，PostgreSQL 不可用时 RAG 功能降级。"""
    global _retriever, _vector_store_error
    if _retriever is not None or _vector_store_error is not None:
        if _retriever is None:
            raise RuntimeError("知识库未就绪（PostgreSQL 不可用）")
        return _retriever
    try:
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=PG_CONNECTION_STRING,
            use_jsonb=True,
        )
        _retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    except Exception as err:
        _vector_store_error = err
        print(f"[rag_chain] 知识库初始化失败，RAG 功能暂不可用: {err}")
        raise RuntimeError("知识库未就绪（PostgreSQL 不可用）") from err
    return _retriever

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是极速购电商平台的专业客服助手小购，同时也是用户的贴心购物顾问。

【服务心态】
1. 语气温和、耐心、亲切、有同理心，称呼用户为"亲"
2. 实事求是，只依据下面知识库内容作答；知识库没有的内容如实告知，绝不编造
3. 学会共情：根据用户语气揣摩其真实想法与期待，给予贴心回应

【产品推荐】
4. 若用户在咨询或流露出购买意向，主动、热情地推荐商品
5. 推荐产品时必须细致讲解：具体型号、核心卖点、价格、适用场景与人群，帮用户做出明智选择
6. 结合用户需求（预算、家庭人数、使用习惯、生活方式等）个性化推荐，给用户带来最高的情绪价值

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


def _build_answer_chain(model_config=None):
    model = create_model_from_config(model_config, temperature=0)
    return (
        (lambda input: {"context": format_docs(input["docs"]), "question": input["question"]})
        | rag_prompt
        | model
        | StrOutputParser()
    )


_answer_chain = _build_answer_chain()


def _with_sources(input, model_config=None):
    docs = _get_retriever().invoke(input["question"])
    chain = _build_answer_chain(model_config)
    answer = chain.invoke({"docs": docs, "question": input["question"]})
    sources = [
        {"content": doc.page_content[:100] + "...", "source": doc.metadata.get("source")}
        for doc in docs
    ]
    return {"answer": answer, "sources": sources}


class _RagChainWithSources:
    """带来源信息的 RAG Chain"""

    def invoke(self, input: dict) -> dict:
        return _with_sources(input, input.get("model"))


ragChainWithSources = _RagChainWithSources()
rag_chain_with_sources = ragChainWithSources

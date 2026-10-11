from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector

from app.db.postgres import PG_CONNECTION_STRING
from app.models.deepseek import create_model
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
            """你是极速购电商平台的专业客服助手小购。

请根据以下知识库内容回答用户的问题。
如果知识库中没有相关内容，请如实告知用户，不要编造信息。
回答语气友好，称呼用户为"亲"，回复简洁清晰。

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


def _build_answer_chain():
    return (
        (lambda input: {"context": format_docs(input["docs"]), "question": input["question"]})
        | rag_prompt
        | _model
        | StrOutputParser()
    )


_answer_chain = _build_answer_chain()


def _with_sources(input):
    docs = _get_retriever().invoke(input["question"])
    answer = _answer_chain.invoke({"docs": docs, "question": input["question"]})
    sources = [
        {"content": doc.page_content[:100] + "...", "source": doc.metadata.get("source")}
        for doc in docs
    ]
    return {"answer": answer, "sources": sources}


class _RagChainWithSources:
    """带来源信息的 RAG Chain"""

    def invoke(self, input: dict) -> dict:
        return _with_sources(input)


ragChainWithSources = _RagChainWithSources()
rag_chain_with_sources = ragChainWithSources

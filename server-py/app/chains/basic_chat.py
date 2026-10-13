"""
Chain 链式调用
使用 LCEL（LangChain Expression Language）管道语法
将 Prompt → Model → OutputParser 串联
"""
from langchain_core.output_parsers import StrOutputParser

from app.models.deepseek import create_model, create_model_from_config
from app.prompts.customer_service import customer_service_prompt, general_chat_prompt

# ─── 服满海客服 Chain（非流式）───────────────────────────────────
_model = create_model(temperature=0.5)
_parser = StrOutputParser()

customer_service_chain = customer_service_prompt | _model | _parser

# ─── 服满海客服 Chain（流式）────────────────────────────────────
_streaming_model = create_model(temperature=0.5, streaming=True)

customer_service_stream_chain = customer_service_prompt | _streaming_model | _parser

# ─── 通用对话 Chain（演示用）────────────────────────────────────
general_chat_chain = general_chat_prompt | _model | _parser


def build_customer_service_chain(model_config=None):
    """按前端传入的大模型配置动态构建客服链（无配置时回落默认模型）"""
    m = create_model_from_config(model_config, temperature=0.5)
    return customer_service_prompt | m | _parser


def build_customer_service_stream_chain(model_config=None):
    """按前端传入的大模型配置动态构建流式客服链"""
    m = create_model_from_config(model_config, temperature=0.5, streaming=True)
    return customer_service_prompt | m | _parser


def format_history(history=None):
    """将前端传来的 { role, content } 数组转换为 LangChain 消息格式"""
    history = history or []
    result = []
    for msg in history:
        if msg.get("role") == "user":
            result.append(("human", msg.get("content")))
        elif msg.get("role") == "assistant":
            result.append(("assistant", msg.get("content")))
    return result

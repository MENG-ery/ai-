"""
模型封装
将 DeepSeek 封装为 LangChain ChatModel
DeepSeek 兼容 OpenAI 协议，使用 ChatOpenAI 并替换 base_url 即可
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# .env.example 中的占位符视为"未配置"，避免覆盖平台内置模型
_PLACEHOLDERS = {
    "",
    "换成你的DeepSeek API Key",
    "换成你的sk",
    "你的百炼APIKey",
}


def _clean(value) -> str:
    text = (value or "").strip()
    return "" if text in _PLACEHOLDERS else text


def _pick(*names: str, default: str = "") -> str:
    """按顺序取第一个有效（非空且非占位符）的环境变量值。"""
    for name in names:
        value = _clean(os.getenv(name))
        if value:
            return value
    return default


# 优先级：显式 DEEPSEEK_* 配置 > 运行环境内置的大模型网关（MCAI_LLM_*）> 官方默认
DEEPSEEK_API_KEY = _pick("DEEPSEEK_API_KEY", "MCAI_LLM_API_KEY")
DEEPSEEK_BASE_URL = _pick(
    "DEEPSEEK_BASE_URL", "MCAI_LLM_BASE_URL", default="https://api.deepseek.com/v1"
)
MODEL_NAME = _pick("MODEL_NAME", "MCAI_LLM_MODEL", default="deepseek-chat")

# 推理模型默认关闭"思考"以降低首字延迟（客服场景更看重响应速度）。
# 设为空字符串可恢复模型默认的思考行为，例如 MODEL_REASONING_EFFORT=。
REASONING_EFFORT = (os.getenv("MODEL_REASONING_EFFORT") or "none").strip()


def _base_params(model: str, api_key: str, base_url: str) -> dict:
    params = {
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "temperature": 0.7,
        "streaming": False,
        # 该网关在带上 stream_options.include_usage 时会缓冲整个流，关闭后首字显著变快
        "stream_usage": False,
    }
    if REASONING_EFFORT:
        params["reasoning_effort"] = REASONING_EFFORT
    return params


def create_model(**overrides) -> ChatOpenAI:
    """创建 DeepSeek 模型实例，可通过 overrides 覆盖默认参数，如 temperature=0, streaming=True"""
    params = _base_params(MODEL_NAME, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL)
    params.update(overrides)
    return ChatOpenAI(**params)


def create_model_from_config(config: dict | None = None, **overrides) -> ChatOpenAI:
    """根据前端传入的模型配置创建实例，未配置的字段回落到 .env 默认值。
    config 形如 {"apiKey": "...", "baseUrl": "...", "model": "..."}。
    """
    if not config:
        return create_model(**overrides)
    params = _base_params(
        _clean(config.get("model")) or MODEL_NAME,
        _clean(config.get("apiKey")) or DEEPSEEK_API_KEY,
        _clean(config.get("baseUrl")) or DEEPSEEK_BASE_URL,
    )
    params.update(overrides)
    return ChatOpenAI(**params)


# 默认导出一个标准实例（非流式）
model = create_model()

# 流式实例，用于 SSE 接口
streaming_model = create_model(streaming=True)

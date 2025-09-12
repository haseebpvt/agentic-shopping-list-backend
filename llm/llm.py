from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

load_dotenv()

ModelSize = Literal["nano", "mini", "large"]

MODEL_MAP: dict[ModelSize | None, str] = {
    "nano": "gpt-5-nano-2025-08-07",
    "mini": "gpt-5-mini-2025-08-07",
    "large": "gpt-5-2025-08-07",
    None: "gpt-5-2025-08-07",
}


def get_llm(model_size: Optional[ModelSize] = None) -> BaseChatModel:
    """
    Returns the right LLM model based on specified model_size or provides default model.
    :param model_size: Model size based on task complexity. Available options (nano, mini, large)
    :return: LangChain's BaseChatModel
    """
    model_name = MODEL_MAP.get(model_size, "gpt-5-2025-08-07")
    return ChatOpenAI(model=model_name)

from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

load_dotenv()

ModelSize = Literal["nano", "mini", "large"]

MODEL_MAP: dict[ModelSize | None, str] = {
    "nano": "gpt-4.1-nano-2025-04-14",
    "mini": "gpt-4.1-mini-2025-04-14",
    "large": "gpt-4.1-2025-04-14",
    None: "gpt-4.1-2025-04-14",
}


def get_llm(model_size: Optional[ModelSize] = None) -> BaseChatModel:
    """
    Returns the right LLM model based on specified model_size or provides default model.
    :param model_size: Model size based on task complexity. Available options (nano, mini, large)
    :return: LangChain's BaseChatModel
    """
    model_name = MODEL_MAP.get(model_size, "gpt-4.1-2025-04-14")
    return ChatOpenAI(model=model_name)

import json
from typing import Union

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel


def custom_structured_output(
        model: Union[type[BaseModel], dict],
        llm: BaseChatModel,
        prompt: str,
):
    # Generate unstructured response
    explanation = llm.invoke(input=prompt)

    output = llm.with_structured_output(model).invoke(explanation.content)

    return output.content

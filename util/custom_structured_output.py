from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel


def custom_structured_output(
        model: type[BaseModel],
        llm: BaseChatModel,
        prompt: str,
):
    parser = PydanticOutputParser(pydantic_object=model)

    chain = llm | parser
    return chain.invoke(prompt)

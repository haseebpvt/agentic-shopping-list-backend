from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from pydantic.v1.main import ModelMetaclass

from graph.type import Product
from llm.llm import get_llm

x = Product
print(type(x))

def custom_structured_output(
        model: ModelMetaclass,
        llm: BaseChatModel,
        prompt: str,
):
    llm_with_structured_output = llm.with_structured_output(model)
    chain = llm | llm_with_structured_output
    return chain.invoke(prompt)


if __name__ == '__main__':
    data = '''
    Product list:
    - Lux: Dishwasher
    - Lays: The tasty chip
    '''

    result = custom_structured_output(Product, get_llm(), "Extract the producst")

    print(result)
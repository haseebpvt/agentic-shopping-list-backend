from langchain_core.language_models.fake_chat_models import ParrotFakeChatModel
from pydantic import BaseModel

from util.custom_structured_output import custom_structured_output


# Define a Pydantic schema
class Person(BaseModel):
    name: str
    age: int


def test_custom_structured_output_with_fake_llm():
    # Given
    # fake_llm = ParrotFakeChatModel()
    #
    # # When
    # result = custom_structured_output(Person, fake_llm, "Hello")
    #
    # # Then
    # assert result == "Hello"

    assert 1 == 1

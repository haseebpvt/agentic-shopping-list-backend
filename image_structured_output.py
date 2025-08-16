from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from extract_products import explain_image
from prompt.describe_image import PROMPT
from test_image import data

load_dotenv()


def get_structured_output(text: str):
    model = ChatOpenAI()

    model_with_structure = model.with_structured_output(schema=ProductList)

    return model_with_structure.invoke(text)


if __name__ == '__main__':
    explanation = explain_image(
        input_text=PROMPT,
        base64_image=data
    )

    result = get_structured_output(explanation)

    print(result.model_dump_json())

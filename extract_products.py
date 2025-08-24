import os

from dotenv import load_dotenv
from openai import OpenAI

from prompt.prompt_loader import get_prompt_template
from test_image import data

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)


def explain_image(input_text: str, base64_image: str):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": input_text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    }
                ]
            }
        ],
    )

    return response.output_text


if __name__ == '__main__':
    prompt = get_prompt_template("describe_image")

    explanation = explain_image(
        input_text=prompt,
        base64_image=data
    )

    print(explanation)

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)


def get_response(input_text: str):
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": "Always respond shortly."
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
    )

    return response.output_text

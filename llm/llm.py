from dotenv import load_dotenv
from langchain_openai import OpenAI

load_dotenv()


def get_llm():
    llm = OpenAI()

    return llm

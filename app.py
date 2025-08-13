import uvicorn
from fastapi import FastAPI

import llm

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World x"}


@app.get("/{input_text}")
def get_response(input_text: str):
    response = llm.get_response(input_text)
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")

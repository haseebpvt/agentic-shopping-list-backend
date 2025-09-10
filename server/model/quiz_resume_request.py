from typing import List

from pydantic import BaseModel


class QuizResumeRequest(BaseModel):
    thread_id: str
    question_and_answers: List[str]
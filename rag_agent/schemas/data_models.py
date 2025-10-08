# schemas/data_models.py

from pydantic import BaseModel, Field
from typing import List, Literal


# ----------------------------
#  QUIZ GENERATOR OUTPUT
# ----------------------------
class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


class QuizOutput(BaseModel):
    lesson_id: str
    questions: List[QuizQuestion]
    total_questions: int


# ----------------------------
#  SUMMARIZER OUTPUT
# ----------------------------
class LessonSummary(BaseModel):
    lesson_id: str
    summary_text: str
    summary_length: int


# ----------------------------
#  RAG RETRIEVE OUTPUT
# ----------------------------
class RAGResult(BaseModel):
    lesson_id: str
    query: str
    results: List[dict]  # hoặc bạn có thể định nghĩa class riêng cho document
    results_count: int


# ----------------------------
#  ROUTER OUTPUT (KẾT HỢP)
# ----------------------------
class RouterOutput(BaseModel):
    lesson_id: str
    executed_agents: List[str]
    outputs: dict  # mapping: agent_name -> output json
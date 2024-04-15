from typing import Annotated, Optional

from fastapi import APIRouter, Query

# pylint: disable=import-error
from src.controller.Quiz.schema.query_Quiz import QueryQuiz
from src.controller.langchain.schema.question_solution import QuestionSolution
from src.service.langchain_service import LangChainService

service = LangChainService()

GPT_router = APIRouter(
    prefix="/gpt",
    tags=["GPT"],
)


@GPT_router.get(path="/solve", response_model=QuestionSolution)
def query_Quiz(
    question: Annotated[str, Query(example="One plus one equals to?")],
    lang: Annotated[Optional[str], Query(example="zh-TW / en")],
):
    """
    詢問數學問題
    """
    return service.reply(question, lang)

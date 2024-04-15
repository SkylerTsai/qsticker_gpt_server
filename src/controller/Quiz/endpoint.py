from typing import Annotated

from fastapi import APIRouter, Query, status

# pylint: disable=import-error
from src.controller.Quiz.schema.query_Quiz import QueryQuiz
from src.controller.Quiz.schema.query_Quiz_image import QueryQuizImage
from src.service.Quiz_service import QuizService

service = QuizService()

Quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)


@Quiz_router.get(path="/", response_model=QueryQuiz)
def query_Quiz(
    uuid: Annotated[str, Query(example="144a68b9-38a9-469d-8550-f0eab53eacb9")],
):
    """
    以 Quiz uuid 取得 Quiz
    """
    return service.get_quiz(uuid)


@Quiz_router.get(path="/images", response_model=QueryQuizImage)
def query_Quiz_image(
    uuid: Annotated[str, Query(example="144a68b9-38a9-469d-8550-f0eab53eacb9")],
):
    """
    以 Quiz uuid 取得 Quiz 題目及選項的圖片
    """
    return service.get_quiz_image(uuid)

# pylint: disable=import-error
import collections
from fastapi import HTTPException
from src.controller.Quiz.schema.query_Quiz import QueryQuiz
from src.controller.Quiz.schema.query_Quiz_image import QueryQuizImage
from src.entity.Quiz_entity import Quiz
from src.infra.repo.Quiz import QuizRepo


class QuizService:
    def __init__(self) -> None:
        self.repo = QuizRepo()

    def get_quiz(self, uuid: str) -> QueryQuiz:
        entity_list = self.repo.get_quiz(uuid)
        if not entity_list:
            raise HTTPException(status_code=404, detail="Quiz not found")

        quiz = entity_list[0]
        return QueryQuiz(
            _id=quiz._id,
            difficulty=quiz.difficulty,
            score=quiz.score,
            multipleSelect=quiz.multipleSelect,
            answerSet=quiz.answerSet,
            enableSolution=quiz.enableSolution,
            solution=quiz.solution,
            isBlankFill=quiz.isBlankFill,
            clickAreas=[ca.dict() for ca in quiz.clickAreas],
        )

    def get_quiz_image(self, uuid):
        entity_list = self.repo.get_quiz(uuid)
        if not entity_list:
            raise HTTPException(status_code=404, detail="Quiz not found")

        quiz = entity_list[0]
        images = {"Title": None, "A": None, "B": None, "C": None, "D": None, "E": None}
        for ca in quiz.clickAreas:
            images[ca.label] = ca.get_image()

        return QueryQuizImage(
            Title=images["Title"],
            A=images["A"],
            B=images["B"],
            C=images["C"],
            D=images["D"],
            E=images["E"],
        )

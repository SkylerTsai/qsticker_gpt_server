from src.entity.Quiz_entity import Quiz
from src.infra.mongo_db import MongoDB


class QuizRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "Quiz"

    def get_quiz(self, uuid: str) -> list[Quiz]:
        query_result = self.db.find(
            self.collection_name,
            {"_id": uuid},
        )

        return [Quiz(item) for item in query_result]

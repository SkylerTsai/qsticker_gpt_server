from src.entity.WorkspaceQuizGroup_entity import WorkspaceQuizGroup
from src.infra.mongo_db import MongoDB


class WorkspaceQuizGroupRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "WorkspaceObject"

    def get_quizGroup(self, uuid: str) -> list[str]:
        query_result = self.db.find(
            self.collection_name,
            {"_id": uuid, "className": "questionnaire.db.schema.WorkspaceQuizGroup"},
        )
        return [WorkspaceQuizGroup(item) for item in query_result]

# pylint: disable=import-error
from fastapi import HTTPException
from src.controller.WorkspaceQuizGroup.schema.query_WorkspaceQuizGroup import (
    QueryWorkspaceQuizGroup,
)
from src.entity.WorkspaceQuizGroup_entity import WorkspaceQuizGroup
from src.infra.repo.WorkspaceQuizGroupRepo import WorkspaceQuizGroupRepo


class WorkspaceQuizGroupService:
    def __init__(self) -> None:
        self.repo = WorkspaceQuizGroupRepo()

    def get_quizGroup(self, uuid: str) -> QueryWorkspaceQuizGroup:
        entity_list = self.repo.get_quizGroup(uuid)
        if not entity_list:
            raise HTTPException(status_code=404, detail="QuizGroup not found")
        quizGroup = entity_list[0]
        return QueryWorkspaceQuizGroup(
            _id=quizGroup._id,
            className=quizGroup.className,
            quizList=quizGroup.quizList,
            totalScore=quizGroup.totalScore,
            name=quizGroup.name,
            owner=quizGroup.owner,
            parent=quizGroup.parent,
        )

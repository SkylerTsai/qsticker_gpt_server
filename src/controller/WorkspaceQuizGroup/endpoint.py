from typing import Annotated

from fastapi import APIRouter, Query

# pylint: disable=import-error
from src.controller.WorkspaceQuizGroup.schema.query_WorkspaceQuizGroup import (
    QueryWorkspaceQuizGroup,
)
from src.service.WorkspaceQuizGroup_service import WorkspaceQuizGroupService

service = WorkspaceQuizGroupService()

WorkspaceQuizGroup_router = APIRouter(
    prefix="/quizgroup",
    tags=["Quiz Group"],
)


@WorkspaceQuizGroup_router.get(path="/", response_model=QueryWorkspaceQuizGroup)
def query_WorkspaceQuizGroup(
    uuid: Annotated[str, Query(example="b78d64e1-065e-435a-936d-3de0991860cc")],
):
    """
    以 WorkspaceQuizGroup uuid 取得 WorkspaceQuizGroup
    """
    return service.get_quizGroup(uuid).dict()

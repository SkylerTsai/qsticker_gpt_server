from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase
from typing import List, Dict


class QueryWorkspaceQuizGroup(CamelBase):
    _id: str
    className: str
    quizList: List[Dict]
    totalScore: float
    name: str
    owner: Dict
    parent: Dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "_id": "quiz-group-id",
                        "className": "questionnaire.db.schema.WorkspaceQuizGroup",
                        "quizList": [
                            {"collection": "Quiz", "_id": "quiz-id"},
                        ],
                        "totalScore": 1,
                        "name": "quiz group name",
                        "owner": {"collection": "Account", "_id": "account-id"},
                        "parent": {"collection": "WorkspaceObject", "_id": "folder-id"},
                    }
                )
            ]
        }
    }

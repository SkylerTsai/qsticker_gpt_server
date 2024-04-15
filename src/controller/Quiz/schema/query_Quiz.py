from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase
from typing import List, Dict, Set


class QueryQuiz(CamelBase):
    _id: str
    difficulty: str
    score: int
    multipleSelect: bool
    answerSet: List[str]
    enableSolution: bool
    solution: str
    isBlankFill: bool
    clickAreas: List[Dict]

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "_id": "quiz-id",
                        "multipleSelect": False,
                        "enableSolution": False,
                        "isBlankFill": False,
                        "difficulty": "EASY",
                        "score": 1,
                        "answerSet": ["B"],
                        "clickAreas": [
                            {
                                "label": "Title",
                                "content": {
                                    "imageField": {
                                        "enabled": True,
                                        "url": "https://question",
                                    },
                                    "textField": {"enabled": False, "text": "question"},
                                },
                            },
                            {
                                "label": "A",
                                "content": {
                                    "imageField": {
                                        "enabled": True,
                                        "url": "https://option1",
                                    },
                                    "textField": {"enabled": False, "url": "option1"},
                                },
                            },
                            {
                                "label": "B",
                                "content": {
                                    "imageField": {
                                        "enabled": True,
                                        "url": "https://option2",
                                    },
                                    "textField": {
                                        "enabled": False,
                                        "text": "https://option2",
                                    },
                                },
                            },
                            {
                                "label": "C",
                                "content": {
                                    "imageField": {
                                        "enabled": True,
                                        "url": "https://option3",
                                    },
                                    "textField": {"enabled": False, "url": "option3"},
                                },
                            },
                            {
                                "label": "D",
                                "content": {
                                    "imageField": {
                                        "enabled": True,
                                        "url": "https://option4I",
                                    },
                                    "textField": {"enabled": False, "text": "option4"},
                                },
                            },
                        ],
                    }
                )
            ]
        }
    }

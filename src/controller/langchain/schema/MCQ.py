from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase
from typing import Optional


class PostMCQRequestBody(CamelBase):
    question: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    option_5: Optional[str]
    solution: Optional[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "question": "己知甲、乙、丙三人各有一些錢,若甲的錢是乙的3倍,乙的錢比丙少12元,丙的錢比甲少20元,則甲和丙兩人共有多少元?",
                        "option_1": "68",
                        "option_2": "72",
                        "option_3": "76",
                        "option_4": "80",
                        "option_5": "",
                        "solution": "",
                    }
                )
            ]
        }
    }


class PostMCQResponseBody(CamelBase):
    answer: int
    solution: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "answer": 3,
                        "solution": "",
                    }
                )
            ]
        }
    }

from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QuestionSolution(CamelBase):
    solution: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "solution": "The answer is 2",
                    }
                )
            ]
        }
    }

from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase
from typing import Optional


class QueryQuizImage(CamelBase):
    Title: Optional[str]
    A: Optional[str]
    B: Optional[str]
    C: Optional[str]
    D: Optional[str]
    E: Optional[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "question": "http://question",
                        "option_1": "http://option_1",
                        "option_2": "http://option_2",
                        "option_3": "http://option_3",
                        "option_4": "http://option_4",
                    }
                )
            ]
        }
    }

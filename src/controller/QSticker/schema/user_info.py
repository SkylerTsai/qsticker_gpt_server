from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase

class UserInfoRequestBody(CamelBase):
    account: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "account": "testdemo",
                        "password": "Dofish1024",
                    }
                )
            ]
        }
    }

class UserInfoResponseBody(CamelBase):
    username: str
    token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "username": "username",
                        "token": "token",
                    }
                )
            ]
        }
    }

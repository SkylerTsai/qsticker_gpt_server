from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.results import DeleteResult

# pylint: disable=import-error
from src.dependencies.settings import get_settings


class MongoDB(object):
    def __new__(cls) -> Any:
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        setting = get_settings()
        self.__client = MongoClient(setting.db_host, setting.db_port)
        self.db = self.__client[setting.database]
        self.__client.server_info()

    def find(self, collection: str, document: dict) -> list:
        return list(self.db[collection].find(document))

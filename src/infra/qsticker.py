import requests
from typing import Any
from fastapi import HTTPException

from src.dependencies.settings import get_settings

class QSticker(object):
    def __new__(cls) -> Any:
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance
        
    def __init__(self) -> None:
        self.server_url = "https://{qsticker_server}/service/v1".format(qsticker_server=get_settings().backend_server)
    
    def get(self, api, authorization=None):
        headers = {'Authorization': authorization}
        response = requests.get(
            url=self.server_url + api,
            headers=headers,
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.content

    def post(self, api, authorization=None, body=None):
        headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json',
        }
        response = requests.post(
            url=self.server_url + api,
            headers=headers,
            json=body,
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

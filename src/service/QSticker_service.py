# pylint: disable=import-error
from src.infra.qsticker import QSticker
from src.controller.QSticker.schema.user_info import UserInfoRequestBody, UserInfoResponseBody

class QStickerService:
    def __init__(self) -> None:
        self.qsticker = QSticker()

    def login(self, body: UserInfoRequestBody) -> UserInfoResponseBody:
        api = "/account/login"
        data = {"identifier": body.account, "password": body.password}
        res = self.qsticker.post(api=api, body=data)
        
        return UserInfoResponseBody(
            username = res['profile']['username'],
            token = res['auth']['token'],
        )

# pylint: disable=import-error
from fastapi import APIRouter

from src.controller.QSticker.schema.user_info import UserInfoRequestBody, UserInfoResponseBody
from src.service.QSticker_service import QStickerService

service = QStickerService()

QSticker_router = APIRouter(
    prefix="/qsticker",
    tags=["QSticker"],
)


@QSticker_router.post(path="/login", response_model=UserInfoResponseBody)
def login(
    body: UserInfoRequestBody,
):
    """
    登入帳號，獲得 user_name 跟 token
    """
    return service.login(body)
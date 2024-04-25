from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# pylint: disable=import-error
from src.config.config import Settings
from src.dependencies.settings import get_settings
from src.controller.WorkspaceQuizGroup.endpoint import WorkspaceQuizGroup_router
from src.controller.Quiz.endpoint import Quiz_router
from src.controller.langchain.endpoint import GPT_router
from src.controller.QSticker.endpoint import QSticker_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(WorkspaceQuizGroup_router)
app.include_router(Quiz_router)
app.include_router(GPT_router)
app.include_router(QSticker_router)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/envSettings")
def get_env_settings(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db_host": settings.db_host, "db_port": settings.db_port}
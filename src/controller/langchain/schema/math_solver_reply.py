from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class AnswerAndSolution(BaseModel):
    """The answer and solution of the given question."""
    answer: str = Field(description="The bried answer only.")
    solution: str = Field(description="The step it takes to solve the question.")
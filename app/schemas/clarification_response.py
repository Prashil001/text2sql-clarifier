from typing import Literal

from pydantic import BaseModel

class ClarificationResponse(BaseModel):
    type: Literal["clarification"] = "clarification"
    question: str
    options: list[str]
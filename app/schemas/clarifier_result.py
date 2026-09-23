from typing import Literal

from pydantic import BaseModel

class ClarifierResult(BaseModel):
    status: Literal["AMBIGUOUS", "CLEAR"]
    question: str | None = None
    options: list[str] = []
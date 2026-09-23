from typing import Literal
from pydantic import BaseModel, Field


class ClarifierResult(BaseModel):
    status: Literal["AMBIGUOUS", "CLEAR"] = Field(
        description="Must be 'AMBIGUOUS' if the user's request is ambiguous, vague, or could refer to multiple metrics (e.g. 'Show sales', 'Best customer', 'Revenue', 'Top products'). Must be 'CLEAR' only if the request has specific filters, columns, or explicit metrics."
    )
    question: str | None = Field(
        default=None,
        description="The follow-up clarification question to ask the user if status is AMBIGUOUS. None if CLEAR."
    )
    options: list[str] = Field(
        default_factory=list,
        description="2 to 4 concise options for the user to choose from if status is AMBIGUOUS. Empty list if CLEAR."
    )
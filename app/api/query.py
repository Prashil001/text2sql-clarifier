from fastapi import APIRouter

from typing import Union

from app.schemas.sql_response import SqlResponse
from app.schemas.query_request import QueryRequest
from app.services.sql_generator import generate_sql
from app.services.clarifier import detect_ambiguity
from app.schemas.clarification_response import ClarificationResponse

router = APIRouter(prefix="/query", tags=["text-to-sql"])

@router.post("", response_model=Union[SqlResponse, ClarificationResponse])
def query_database(request: QueryRequest):

    clarification = detect_ambiguity(request.question)
    if clarification.status == "AMBIGUOUS":
        return ClarificationResponse(
            question=clarification.question,
            options=clarification.options
        )

    return generate_sql(request.question)
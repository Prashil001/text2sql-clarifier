from typing import Union

from fastapi import APIRouter, HTTPException

from app.schemas.query_request import QueryRequest
from app.schemas.sql_response import SqlResponse
from app.schemas.clarification_response import ClarificationResponse
from app.schemas.query_result import QueryResult

from app.services.clarifier import detect_ambiguity
from app.services.sql_generator import generate_sql
from app.services.sql_validator import validate_sql
from app.services.query_executor import execute_query

router = APIRouter(prefix="/query", tags=["text-to-sql"])


@router.post(
    "",
    response_model=Union[QueryResult, ClarificationResponse]
)
def query_database(request: QueryRequest):
    """
    End-to-end Text-to-SQL pipeline.

    Flow:
    User Question
        ↓
    Clarifier
        ↓
    SQL Generator
        ↓
    SQL Validator
        ↓
    Query Executor
        ↓
    Database Results
    """

    # Step 1: Check if clarification is needed
    clarification = detect_ambiguity(request.question)

    if clarification.status == "AMBIGUOUS":
        return ClarificationResponse(
            question=clarification.question,
            options=clarification.options
        )

    # Step 2: Generate SQL
    sql_response: SqlResponse = generate_sql(request.question)

    # Step 3: Validate generated SQL
    valid, result = validate_sql(sql_response.sql)

    if not valid:
        raise HTTPException(
            status_code=400,
            detail=result
        )

    # Step 4: Execute validated SQL
    validated_sql = result.sql(dialect="postgres")
    data = execute_query(validated_sql)

    # Step 5: Return final response
    return QueryResult(
        sql=validated_sql,
        reason=sql_response.reason,
        rows_returned=len(data),
        data=data
    )
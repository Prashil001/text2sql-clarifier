from fastapi import APIRouter

from app.schemas.sql_response import SqlResponse
from app.schemas.query_request import QueryRequest
from app.services.sql_generator import generate_sql

router = APIRouter(prefix="/query", tags=["text-to-sql"])

@router.post("", response_model=SqlResponse)
def query_database(request: QueryRequest):
    return generate_sql(request.question)
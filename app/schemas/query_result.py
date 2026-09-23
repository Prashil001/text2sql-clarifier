from pydantic import BaseModel

class QueryResult(BaseModel):
    sql: str
    reason: str
    rows_returned: int
    data: list[dict]
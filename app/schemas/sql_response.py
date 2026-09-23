from pydantic import BaseModel

class SqlResponse(BaseModel):
    sql:str
    reason:str


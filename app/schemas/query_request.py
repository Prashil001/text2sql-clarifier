from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, description="Natural language question about the database")

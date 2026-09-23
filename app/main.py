from fastapi import FastAPI

from app.api.query import router as query_router

app = FastAPI(
    title="Text-to-SQL Clarifier",
    version="1.0.0"
)


app.include_router(query_router)


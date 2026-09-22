from fastapi import FastAPI

app = FastAPI(
    title="Text-to-SQL Clarifier",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Text-to-SQL API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
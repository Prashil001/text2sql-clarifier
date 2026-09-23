from app.services.schema_loader import load_schema, format_schema
from app.schemas.sql_response import SqlResponse
from app.services.llm import llm
from app.prompts.sql_prompt import SQL_SYSTEM_PROMPT


structured_llm = llm.with_structured_output(SqlResponse)

import time

def generate_sql(question: str):
    start = time.time()

    print("Loading schema...")
    schema = format_schema(load_schema())
    print(f"Schema loaded in {time.time()-start:.2f}s")

    prompt = f"""
    {SQL_SYSTEM_PROMPT}

    database schema:
    {schema}

    user question:
    {question}
    """

    print("Calling Ollama...")
    result = structured_llm.invoke(prompt)
    print(f"Ollama finished in {time.time()-start:.2f}s")

    return result




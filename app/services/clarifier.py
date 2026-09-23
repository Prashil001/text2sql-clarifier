from app.prompts.clarifier_prompt import CLARIFIER_SYSTEM_PROMPT
from app.schemas.clarifier_result import ClarifierResult
from app.services.llm import llm
from app.services.schema_loader import load_schema, format_schema

structured_clarifier = llm.with_structured_output(ClarifierResult)

def detect_ambiguity(question:str):
    schema = format_schema(load_schema())

    prompt = f"""
    {CLARIFIER_SYSTEM_PROMPT}

    database schema:
    {schema}

    user question:
    {question}
    """

    return structured_clarifier.invoke(prompt)


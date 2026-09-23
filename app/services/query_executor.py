from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import SessionLocal
from app.utils.serializer import serialize_rows


def execute_query(sql: str):
    """
    Execute a validated SQL query against PostgreSQL.

    Args:
        sql (str): Validated SQL query (SELECT only).

    Returns:
        list[dict]: Query results as a list of dictionaries.

    Raises:
        RuntimeError: If query execution fails.
    """

    db = SessionLocal()

    try:
        result = db.execute(text(sql))

        # Convert rows into dictionaries
        rows = result.mappings().all()

        return serialize_rows([dict(row) for row in rows])

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database execution failed: {str(e)}")

    finally:
        db.close()
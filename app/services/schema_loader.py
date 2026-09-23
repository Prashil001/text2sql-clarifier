from collections import defaultdict
from sqlalchemy import text

from app.database.session import SessionLocal

def load_schema():
    db = SessionLocal()

    query = text("""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema='public'
    ORDER BY table_name, ordinal_position;
    """)

    result = db.execute(query).fetchall()

    db.close()

    schema = defaultdict(list)

    for table, column in result:
        schema[table].append(column)

    return schema


def format_schema(schema):
    output = []

    for table, columns in schema.items():
        output.append(f"Table: {table}")

        for column in columns:
            output.append(f"  - {column}")

        output.append("")

    return "\n".join(output)


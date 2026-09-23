from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


def serialize_value(value):
    """
    Convert a Python/SQLAlchemy value into a JSON-serializable value.
    """

    if value is None:
        return None

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, UUID):
        return str(value)

    if isinstance(value, list):
        return [serialize_value(item) for item in value]

    if isinstance(value, dict):
        return {
            key: serialize_value(val)
            for key, val in value.items()
        }

    return value


def serialize_rows(rows):
    """
    Convert a list of SQLAlchemy RowMapping dictionaries into
    JSON-serializable dictionaries.

    Example:
        Input:
        [
            {"id": 1, "price": Decimal("99.99")},
            {"id": 2, "created_at": datetime(...)}
        ]

        Output:
        [
            {"id": 1, "price": 99.99},
            {"id": 2, "created_at": "2026-09-23T18:32:10"}
        ]
    """

    return [
        {
            key: serialize_value(value)
            for key, value in row.items()
        }
        for row in rows
    ]
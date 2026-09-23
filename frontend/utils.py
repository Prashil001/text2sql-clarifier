"""Utility functions for the Text2SQL Clarifier frontend."""

import csv
import io
from datetime import datetime
from typing import Any


def get_timestamp() -> str:
    """Get the current timestamp formatted for display.
    
    Returns:
        Formatted timestamp string like '2:30 PM'.
    """
    return datetime.now().strftime("%I:%M %p")


def format_sql(sql: str) -> str:
    """Format SQL for display with basic prettification.
    
    Args:
        sql: Raw SQL string from the backend.
        
    Returns:
        Formatted SQL string.
    """
    keywords = [
        "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN",
        "INNER JOIN", "ORDER BY", "GROUP BY", "HAVING", "LIMIT",
        "OFFSET", "UNION", "INSERT", "UPDATE", "DELETE", "ON",
        "AND", "OR", "AS", "IN", "NOT", "BETWEEN", "LIKE",
        "IS NULL", "IS NOT NULL", "EXISTS", "CASE", "WHEN",
        "THEN", "ELSE", "END", "WITH", "DISTINCT"
    ]
    formatted = sql.strip()
    for kw in sorted(keywords, key=len, reverse=True):
        formatted = formatted.replace(f" {kw.lower()} ", f" {kw} ")
    return formatted


def data_to_csv(data: list[dict[str, Any]]) -> str:
    """Convert a list of dictionaries to CSV string for download.
    
    Args:
        data: List of row dictionaries from the backend.
        
    Returns:
        CSV formatted string.
    """
    if not data:
        return ""
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


# Example prompts for the empty state and sidebar
EXAMPLE_PROMPTS: list[str] = [
    "Show all customers",
    "Top 5 customers by spending",
    "Revenue for March",
    "Products cheaper than ₹1000",
    "Total orders per month",
    "Average order value by category",
]

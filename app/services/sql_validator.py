from sqlglot import parse_one, exp


MAX_ROWS = 100


def validate_sql(sql: str):
    """
    Validate LLM-generated SQL before execution.

    Rules:
    - Only SELECT statements are allowed.
    - Multiple SQL statements are rejected.
    - Invalid SQL is rejected.
    - Automatically adds LIMIT 100 if no LIMIT exists.

    Returns:
        (True, parsed_tree) if valid
        (False, error_message) if invalid
    """

    try:
        sql = sql.strip()

        # Reject multiple SQL statements
        # Allow a single trailing semicolon.
        if ";" in sql[:-1]:
            return False, "Multiple SQL statements are not allowed."

        # Parse SQL into an Abstract Syntax Tree (AST)
        tree = parse_one(sql, dialect="postgres")

        # Allow only SELECT queries
        if not isinstance(tree, exp.Select):
            return False, "Only SELECT queries are allowed."

        # Automatically add LIMIT if missing
        if tree.args.get("limit") is None:
            tree.set(
                "limit",
                exp.Limit(
                    expression=exp.Literal.number(MAX_ROWS)
                )
            )

        return True, tree

    except Exception as e:
        return False, f"Invalid SQL: {str(e)}"
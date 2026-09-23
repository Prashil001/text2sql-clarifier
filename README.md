# Text2SQL Clarifier

> A production-style AI Text-to-SQL system that converts natural language into safe PostgreSQL queries using **FastAPI, LangChain, Ollama (Qwen 3), SQLAlchemy, and PostgreSQL**.

Unlike typical Text-to-SQL demos, this project includes **dynamic schema grounding**, an **ambiguity clarification engine**, **AST-based SQL validation**, and **safe query execution**, making it much closer to real-world enterprise AI systems.

---

## Features

- Dynamic database schema grounding using PostgreSQL `information_schema`
- Local LLM with **Ollama + Qwen 3**
- Natural language → PostgreSQL SQL generation
- Ambiguity clarification before SQL generation
- Structured LLM outputs with **Pydantic**
- SQL safety validation using **sqlglot**
- Whitelist policy (only `SELECT` queries allowed)
- Automatic `LIMIT 100` injection
- Secure SQL execution with SQLAlchemy
- Dockerized PostgreSQL
- Alembic database migrations
- Interactive Swagger API documentation

---

## Demo

### Architecture

```text
User
 │
 ▼
FastAPI
 │
 ▼
Clarification Engine
 │
 ▼
Schema Loader
 │
 ▼
Qwen 3 (Ollama)
 │
 ▼
SQL Validator (sqlglot)
 │
 ▼
Safe Query Executor
 │
 ▼
PostgreSQL
 │
 ▼
JSON Response
```

### Example

**Input**

```json
{
  "question": "Top 5 customers by spending"
}
```

**Output**

```json
{
  "sql": "SELECT c.name, SUM(o.total_amount) AS spending ... LIMIT 5;",
  "reason": "Join customers and orders, aggregate spending, and return the top five.",
  "rows_returned": 5,
  "data": [
    {
      "name": "John",
      "spending": 12450
    }
  ]
}
```

### Ambiguous Query

**Input**

```json
{
  "question": "Show sales"
}
```

**Output**

```json
{
  "type": "clarification",
  "question": "Which sales do you mean?",
  "options": [
    "Total revenue",
    "Number of orders",
    "Sales for a specific period"
  ]
}
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| AI | LangChain |
| Local LLM | Ollama (Qwen 3) |
| Validation | Pydantic |
| SQL Parser | sqlglot |
| Containerization | Docker |

---

## Project Structure

```text
text2sql-clarifier/
│
├── app/
│   ├── api/
│   │   └── query.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   └── base.py
│   │
│   ├── models/
│   ├── prompts/
│   ├── schemas/
│   ├── services/
│   │   ├── llm.py
│   │   ├── schema_loader.py
│   │   ├── clarifier.py
│   │   ├── sql_generator.py
│   │   ├── sql_validator.py
│   │   └── query_executor.py
│   │
│   ├── utils/
│   │   └── serializer.py
│   │
│   └── main.py
│
├── alembic/
├── tests/
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## How It Works

### Step 1 — Dynamic Schema Grounding

Instead of hardcoding table names, the system queries PostgreSQL's `information_schema`.

Example:

```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema='public';
```

This keeps the AI synchronized with the latest database schema after every Alembic migration.

---

### Step 2 — Clarification Engine

Before generating SQL, the system determines whether the user's request is ambiguous.

Example:

| User Input | Action |
|------------|---------|
| Show all customers | Generate SQL |
| Revenue for March | Generate SQL |
| Show sales | Ask clarification |
| Best customer | Ask clarification |

---

### Step 3 — SQL Generation

The LLM receives:

- System instructions
- Live database schema
- User question

It returns structured JSON.

```json
{
  "sql":"SELECT ...",
  "reason":"..."
}
```

---

### Step 4 — SQL Safety Guardrails

Generated SQL is parsed into an Abstract Syntax Tree using **sqlglot**.

Security rules:

- Only `SELECT` statements are allowed.
- Multiple SQL statements are rejected.
- Invalid SQL is rejected.
- Missing `LIMIT` automatically becomes `LIMIT 100`.

Example:

Input:

```sql
SELECT * FROM customers;
```

Executed:

```sql
SELECT * FROM customers LIMIT 100;
```

---

### Step 5 — Safe Query Execution

Validated SQL is executed using SQLAlchemy.

Results are serialized into JSON-safe values.

Supported types:

- `Decimal`
- `datetime`
- `date`
- `UUID`

---

## Installation

### Clone

```bash
git clone https://github.com/yourusername/text2sql-clarifier.git
cd text2sql-clarifier
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Start PostgreSQL using Docker.

```bash
docker-compose up -d
```

Run migrations.

```bash
alembic upgrade head
```

Seed the database.

```bash
python seed.py
```

---

## Ollama Setup

Install Ollama.

Download:

https://ollama.com

Pull Qwen 3.

```bash
ollama pull qwen3:4b
```

Verify.

```bash
ollama list
```

---

## Environment Variables

Create `.env`.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/text2sql
OLLAMA_MODEL=qwen3:4b
MAX_QUERY_ROWS=100
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

Open Swagger.

```
http://127.0.0.1:8000/docs
```

---

## API

### Generate SQL

`POST /query`

Request

```json
{
  "question":"Show all customers"
}
```

Response

```json
{
  "sql":"SELECT * FROM customers LIMIT 100;",
  "reason":"Retrieve all customers.",
  "rows_returned":100,
  "data":[]
}
```

---

## Security Features

- Dynamic schema grounding
- Structured LLM outputs
- SQL AST validation
- SELECT-only execution
- Automatic row limiting
- Multi-statement blocking
- Safe SQL execution

---

## Testing

Run validator tests.

```bash
python test_validator.py
```

Run executor tests.

```bash
python test_executor.py
```

Run clarification tests.

```bash
python test_clarifier.py
```

---

## Why sqlglot Instead of Regex?

Regex only matches text.

`sqlglot` parses SQL into an Abstract Syntax Tree.

Example:

```sql
SELECT name
FROM customers
WHERE id=1;
```

becomes a structured tree that allows reliable security checks regardless of formatting or comments.

---

## Engineering Decisions

| Problem | Solution |
|---------|----------|
| Hallucinated columns | Dynamic schema grounding |
| Ambiguous requests | Clarification Engine |
| Unsafe SQL | AST validation |
| Large queries | Automatic LIMIT |
| Non-JSON database types | Serializer |
| Schema evolution | Alembic |

---

## Future Improvements

- Conversation memory for follow-up questions
- SQL execution history
- Query caching
- Streaming responses
- Role-based database permissions
- Query cost estimation before execution
- Multi-database support (MySQL, SQLite, SQL Server)

---

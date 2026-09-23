# 🧠 Text2SQL Clarifier

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Qwen_3_(4B)-black?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com/)
[![sqlglot](https://img.shields.io/badge/SQL_Parser-sqlglot-blue?style=flat-square)](https://github.com/tobymao/sqlglot)
[![Docker Compose](https://img.shields.io/badge/Docker-Orchestrated-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

> **Enterprise-grade, guarded Text-to-SQL execution engine featuring dynamic schema grounding, interactive ambiguity resolution, AST-level safety verification, and containerized orchestration.**

---

## 📌 Executive Summary

Most open-source Text-to-SQL implementations suffer from four critical production failure modes:

| Failure Mode | Naive Implementation | Text2SQL Clarifier Solution |
| :--- | :--- | :--- |
| **Hallucination** | Hardcoded prompts or static table lists | **Dynamic Schema Grounding** via PostgreSQL `information_schema` |
| **Ambiguous Intent** | Generates arbitrary/guessed SQL queries | **Human-in-the-Loop Clarification Engine** generating discrete options |
| **SQL Injection / DDL** | Regex blacklists (`DROP`, `DELETE`) | **AST Validation (`sqlglot`)** enforcing strict `SELECT` visitor policies |
| **Runaway Queries** | Unbounded `SELECT *` exhausting memory | **AST Rewriting** automatically injecting safe `LIMIT 100` clauses |

This project demonstrates a production-hardened AI engineering pipeline designed for zero-trust database environments.

---

## 🏗️ System Architecture

```text
                                  +---------------------------------------+
                                  |             Client Layer              |
                                  |   Streamlit Web UI / REST Consumers   |
                                  +-------------------+-------------------+
                                                      |
                                          HTTP POST   | /query
                                                      v
+---------------------------------------------------------------------------------------------------------+
|                                         FastAPI Backend Service                                         |
|                                                                                                         |
|   1. Request Ingestion  ──>  2. Ambiguity Detection  ──[ Ambiguous ]──> Returns Clarification Options  |
|                                     │                                                                   |
|                                  [ Clear ]                                                              |
|                                     │                                                                   |
|                                     v                                                                   |
|                              3. Live Schema Loader (queries PostgreSQL information_schema)              |
|                                     │                                                                   |
|                                     v                                                                   |
|                              4. Structured SQL Generation (via Ollama Qwen 3 LLM)                       |
|                                     │                                                                   |
|                                     v                                                                   |
|                              5. AST Guardrails (sqlglot parse_one & SELECT node check)                  |
|                                     │                                                                   |
|                                     v                                                                   |
|                              6. AST Rewriter (enforces LIMIT <= 100)                                    |
|                                     │                                                                   |
|                                     v                                                                   |
|                              7. Safe Query Execution (SQLAlchemy session + serializer)                  |
+-------------------------------------+-----------------------------------+-------------------------------+
                                      │                                   │
                           SQL Query  │                        Inference  │ HTTP (host.docker.internal)
                                      v                                   v
                      +-------------------------------+   +-------------------------------+
                      |      PostgreSQL Database      |   |          Ollama LLM           |
                      |   (Docker: text2sql_db:5432)  |   |     (Host Machine: 11434)     |
                      +-------------------------------+   +-------------------------------+
```

---

## 🛡️ Core Engineering Highlights

### 1. Dynamic Schema Grounding
Rather than providing static table definitions that quickly become outdated, the engine inspects PostgreSQL's live catalog at runtime:
```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```
* **Zero Schema Drift**: Automatically stays synchronized with Alembic migrations without code redeployment.
* **Token Optimization**: Extracts only relevant tables and ordinal column mappings, minimizing prompt token consumption.

### 2. Ambiguity Clarification Engine
When a user prompt lacks distinct metrics or filtering criteria (e.g., *"Show sales"* or *"Best customer"*):
* The engine flags the request as `AMBIGUOUS`.
* Formulates a targeted follow-up question with 2–4 actionable choices (e.g., *Total Revenue*, *Order Count*, *Monthly Breakdown*).
* Returns an interactive clarification schema without executing speculative SQL.

### 3. AST-Level Safety Guardrails (`sqlglot`)
Regex-based SQL validation is fundamentally flawed—comments, subqueries, and dialect-specific formatting easily circumvent naive keyword filters. 

This engine parses generated SQL into a semantic **Abstract Syntax Tree (AST)**:
```python
# Parse SQL into Postgres-specific AST
tree = parse_one(sql, dialect="postgres")

# 1. Statement Type Whitelist: Allow ONLY SELECT expressions
if not isinstance(tree, exp.Select):
    raise SecurityException("Only SELECT queries are allowed.")

# 2. Multi-statement Injection Prevention
if ";" in sql[:-1]:
    raise SecurityException("Multi-statement queries are forbidden.")

# 3. AST Mutation: Automatically inject safe LIMIT if omitted
if tree.args.get("limit") is None:
    tree.set("limit", exp.Limit(expression=exp.Literal.number(MAX_ROWS)))
```

### 4. Hybrid Host-Docker Topology
* **Database & Services**: PostgreSQL, FastAPI, and Streamlit run isolated within a unified Docker Compose bridge network.
* **LLM Engine**: Ollama runs directly on the host machine and is bridged via `host.docker.internal:11434`.
* **Engineering Advantage**: Enables native hardware/GPU acceleration (Metal on macOS, CUDA on Windows/Linux) without inflating Docker container images or requiring complex GPU container drivers.

---

## 🛠️ Technology Stack

| Domain | Technology | Key Function |
| :--- | :--- | :--- |
| **API Framework** | **FastAPI** | High-performance asynchronous REST API with automatic OpenAPI docs |
| **AI Orchestration** | **LangChain** + **ChatOllama** | Model integration, prompt templating, and structured schema bindings |
| **Local Foundation Model** | **Qwen 3 (4B)** | High-efficiency instruction-tuned model for structured SQL generation |
| **AST Parser** | **sqlglot** | SQL parsing, syntactic tree validation, and safe query rewriting |
| **Database & ORM** | **PostgreSQL 16** + **SQLAlchemy** | Relational data persistence and pooled connection management |
| **Migrations** | **Alembic** | Version-controlled database schema migrations |
| **Data Synthesizer** | **Faker** | Automated multi-table mock data generation for seeding |
| **Containerization** | **Docker** + **Docker Compose** | Multi-container declarative orchestration and network topology |

---

## 📂 Repository Structure

```text
text2sql-clarifier/
│
├── app/                              # Core application package
│   ├── api/
│   │   └── query.py                  # POST /query route & pipeline orchestration
│   ├── core/
│   │   └── config.py                 # Pydantic BaseSettings & environment management
│   ├── database/
│   │   ├── base.py                   # SQLAlchemy DeclarativeBase
│   │   ├── session.py                # Engine connection factory & SessionLocal
│   │   └── seed.py                   # Database seeding script (Faker)
│   ├── models/                       # SQLAlchemy declarative models
│   │   ├── customer.py               # Customers entity
│   │   ├── order.py                  # Orders entity
│   │   ├── order_item.py             # Order items associative entity
│   │   └── product.py                # Products entity
│   ├── prompts/
│   │   ├── clarifier_prompt.py       # Ambiguity detection prompt & few-shot rules
│   │   └── sql_prompt.py             # Grounded SQL generation prompt
│   ├── schemas/                      # Pydantic contract schemas
│   │   ├── query_request.py          # Incoming query payload
│   │   ├── query_result.py           # Successful execution schema
│   │   ├── clarification_response.py # Interactive clarification schema
│   │   ├── clarifier_result.py       # LLM structured output schema
│   │   └── sql_response.py           # SQL generation payload schema
│   ├── services/
│   │   ├── clarifier.py              # Ambiguity classification service
│   │   ├── schema_loader.py          # Runtime information_schema inspection
│   │   ├── sql_generator.py          # Structured LLM invocation
│   │   ├── sql_validator.py          # AST parsing & safety rewriting
│   │   ├── query_executor.py         # SQLAlchemy execution & transaction handling
│   │   └── llm.py                    # Ollama model instance initialization
│   ├── utils/
│   │   └── serializer.py             # Non-JSON data type sanitization (Decimal, UUID, datetime)
│   └── main.py                       # FastAPI entrypoint & router configuration
│
├── frontend/                         # Streamlit frontend package
│   ├── api.py                        # Client communication with FastAPI
│   ├── components.py                 # Modular UI components
│   ├── styles.py                     # Minimalist UI design system
│   └── utils.py                      # Data export, formatting, & UI utilities
│
├── alembic/                          # Database schema migration revisions
├── streamlit_app.py                  # Streamlit application entrypoint
├── Dockerfile.backend                # Multi-stage container recipe for FastAPI
├── Dockerfile.frontend               # Container recipe for Streamlit
├── docker-compose.yml                # Declarative multi-service compose specification
├── requirements.txt                  # Locked Python dependency manifest
├── .dockerignore                     # Build context exclusions
├── .env                              # Environment configuration
└── README.md                         # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. [Ollama](https://ollama.com/) installed and serving on your host machine.

### 1. Model Setup
Pull the lightweight Qwen 3 model onto your host machine:
```bash
ollama pull qwen3:4b
```
Ensure Ollama is running and accessible:
```bash
curl http://localhost:11434/api/tags
```

### 2. Clone & Launch Infrastructure
Clone the repository and spin up all services via Docker Compose:
```bash
git clone https://github.com/Prashil001/text2sql-clarifier.git
cd text2sql-clarifier

# Build and start PostgreSQL, FastAPI, and Streamlit
docker compose up --build -d
```

### 3. Initialize & Seed Database
Run Alembic migrations and the synthetic data seeder inside the backend container:
```bash
# Apply schema migrations
docker compose exec backend alembic upgrade head

# Seed synthetic database with realistic customers, orders, and products
docker compose exec backend python -m app.database.seed
```

### 4. Access Interfaces
* **FastAPI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Streamlit UI**: [http://localhost:8501](http://localhost:8501)
* **PostgreSQL (Host Access)**: `localhost:5433` (User: `postgres` / Pass: `postgres` / DB: `text2sql`)

---

## 📡 API Reference

### `POST /query`
Main endpoint for the text-to-SQL translation pipeline.

#### Scenario A: Unambiguous Query (Direct Execution)
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Top 5 customers by spending"}'
```

**Response (`200 OK`)**:
```json
{
  "sql": "SELECT customers.name, SUM(orders.total_amount) AS total_spending FROM customers JOIN orders ON customers.id = orders.customer_id GROUP BY customers.name ORDER BY total_spending DESC LIMIT 5",
  "reason": "Joined customers with orders, aggregated total spending per customer, and sorted in descending order.",
  "rows_returned": 5,
  "data": [
    { "name": "Jane Doe", "total_spending": 4820.50 },
    { "name": "John Smith", "total_spending": 3910.00 }
  ]
}
```

#### Scenario B: Ambiguous Query (Clarification Required)
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Show sales"}'
```

**Response (`200 OK`)**:
```json
{
  "type": "clarification",
  "question": "Which sales metric do you mean?",
  "options": [
    "Total revenue",
    "Order count",
    "Monthly sales breakdown"
  ]
}
```

---

## 🧪 Verification & Security Testing

The repository includes sanity validation tests verifying AST rejection of malicious queries:

```python
from app.services.sql_validator import validate_sql

# 1. SQL Injection / Mutation Prevention
valid, _ = validate_sql("DROP TABLE customers;")
assert valid is False  # Rejects DDL

valid, _ = validate_sql("DELETE FROM orders WHERE id = 1;")
assert valid is False  # Rejects DML deletions

valid, _ = validate_sql("SELECT * FROM customers; DROP TABLE orders;")
assert valid is False  # Rejects multi-statement injection

# 2. Automatic Safeguard Injection
valid, tree = validate_sql("SELECT * FROM customers;")
assert valid is True
assert tree.sql(dialect="postgres") == "SELECT * FROM customers LIMIT 100"  # Injects LIMIT
```

---

## ⚖️ Engineering Decisions & Trade-Offs

| Decision | Alternative Considered | Trade-Off Rationale |
| :--- | :--- | :--- |
| **`sqlglot` AST Parser** | Regex / Keyword Search | Regex fails against SQL comments (`/* ... */`), string literals, or CTEs. AST validation inspects the syntactic grammar with mathematical certainty. |
| **`information_schema` Dynamic Querying** | Hardcoded Schema in System Prompt | Hardcoded schemas drift when migrations are applied. Dynamic querying ensures 100% catalog parity with zero deployment overhead. |
| **Local Host Ollama via Gateway** | Containerized Ollama / Dockerized Model | Running Ollama in Docker requires downloading multi-gigabyte models into volumes and fragile GPU passthrough. `host.docker.internal` allows zero-friction GPU inference. |
| **Pydantic Structured Outputs** | Freeform text parsing / Regex extraction | Constrains model generation to conform directly to typed schema contracts, eliminating JSON syntax errors. |
| **Explicit Clarification Stage** | Multi-Turn Conversational Memory | Keeping individual queries deterministic reduces token context bloat and eliminates state management complexity in stateless API layers. |

---

## 📈 Roadmap & Production Enhancements

- [ ] **Vector Store Hybrid Search (RAG)**: Index table schemas and business definitions with ChromaDB for 100+ table enterprise schemas.
- [ ] **Query Cost Optimization**: Run `EXPLAIN (FORMAT JSON)` on generated queries before execution to abort high-cost queries before DB saturation.
- [ ] **Read-Only Connection Pooling**: Enforce read-only replicas at the PostgreSQL connection level (`SET default_transaction_read_only = on`).
- [ ] **Streaming Execution**: Server-Sent Events (SSE) for streaming query generation and tabular data chunks.

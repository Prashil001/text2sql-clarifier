# 🧠 Text2SQL Clarifier

> A production-grade AI Text-to-SQL system that converts natural language into **safe PostgreSQL queries** using **FastAPI, LangChain, Ollama (Qwen 3), SQLAlchemy, PostgreSQL, and Streamlit**.

Unlike typical Text-to-SQL demos, this project includes **dynamic schema grounding**, an **ambiguity clarification engine**, **AST-based SQL validation**, and **secure query execution**, making it much closer to enterprise AI applications.

---

## ✨ Features

- 💬 Natural Language → PostgreSQL SQL generation
- 🦙 Local LLM inference using **Ollama + Qwen 3**
- 🗂️ Dynamic schema grounding from PostgreSQL `information_schema`
- ❓ Clarification Engine for ambiguous requests
- ✅ Structured LLM outputs using Pydantic
- 🛡️ SQL AST validation using `sqlglot`
- 🔒 Only `SELECT` queries are allowed
- 📏 Automatic `LIMIT 100` injection
- ⚡ Secure SQL execution using SQLAlchemy
- 🎨 Interactive Streamlit chat interface
- 🐳 Docker Compose orchestration
- 🔄 Alembic database migrations
- 📚 Swagger API documentation

---

# 🏗️ System Architecture

The application follows a layered architecture where each service has a single responsibility.

```text
                    Docker Compose Network

        ┌──────────────────────────────────────┐
        │                                      │
        │   Streamlit Frontend (Port 8501)     │
        │              │                       │
        │              ▼ HTTP                  │
        │      FastAPI Backend (8000)          │
        │         │                │           │
        │         ▼                ▼           │
        │ PostgreSQL (5432)   Ollama (Host)    │
        └──────────────────────────────────────┘
```

## Service Responsibilities

| Service | Responsibility |
|---------|---------------|
| **Streamlit** | User interface and API communication |
| **FastAPI** | Clarification, schema loading, LLM orchestration, SQL validation, and execution |
| **PostgreSQL** | Stores application data |
| **Ollama** | Runs the local Qwen model |

> The Streamlit frontend never communicates directly with PostgreSQL or Ollama. Every request flows through FastAPI.

---

# 🤖 AI Processing Pipeline

Every query passes through multiple safety layers before reaching the database.

```text
User Question
      │
      ▼
Clarification Engine
      │
      ▼
Dynamic Schema Loader
      │
      ▼
Qwen 3 (Ollama)
      │
      ▼
Structured SQL Output
      │
      ▼
SQL AST Validation (sqlglot)
      │
      ▼
Safe Query Execution
      │
      ▼
JSON Response
```

## Pipeline Breakdown

### 1. Clarification Engine

Detects ambiguous requests before SQL generation.

| User Input | Action |
|------------|---------|
| Show all customers | Generate SQL |
| Revenue for March | Generate SQL |
| Show sales | Ask clarification |
| Best customer | Ask clarification |

---

### 2. Dynamic Schema Grounding

Instead of hardcoding tables, the backend queries PostgreSQL's `information_schema`.

```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema='public';
```

This keeps the LLM synchronized with the latest database schema.

---

### 3. SQL Generation

The LLM receives:

- User question
- Live database schema
- System instructions

It returns structured JSON.

```json
{
  "sql": "SELECT ...",
  "reason": "..."
}
```

---

### 4. SQL Safety Guardrails

Every generated query is parsed into an Abstract Syntax Tree using **sqlglot**.

Security rules:

- ✅ Only `SELECT` statements
- ❌ Reject `DELETE`, `UPDATE`, `INSERT`, `DROP`
- ❌ Block multiple SQL statements
- ✅ Automatically add `LIMIT 100`

Example:

Generated:

```sql
SELECT * FROM customers;
```

Executed:

```sql
SELECT * FROM customers LIMIT 100;
```

---

### 5. Safe Query Execution

Validated SQL is executed using SQLAlchemy.

Returned values are serialized into JSON-safe types:

- Decimal
- datetime
- date
- UUID

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| AI Framework | LangChain |
| Local LLM | Ollama (Qwen 3) |
| Validation | Pydantic |
| SQL Parser | sqlglot |
| Containerization | Docker & Docker Compose |

---

# 📂 Project Structure

```text
text2sql-clarifier/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
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
│   ├── utils/
│   │   └── serializer.py
│   └── main.py
│
├── frontend/
│   ├── api.py
│   ├── components.py
│   ├── styles.py
│   └── utils.py
│
├── streamlit_app.py
├── alembic/
├── tests/
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Quick Start (Docker)

## Prerequisites

- Docker Desktop
- Docker Compose
- Ollama installed locally

### Pull the model

```bash
ollama pull qwen3:4b
```

Verify:

```bash
ollama list
```

---

## Clone the repository

```bash
git clone https://github.com/yourusername/text2sql-clarifier.git
cd text2sql-clarifier
```

---

## Start the entire application

```bash
docker compose up --build
```

This launches:

| Service | URL |
|---------|-----|
| Streamlit | http://localhost:8501 |
| FastAPI Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

---

## Run database migrations

```bash
docker compose exec backend alembic upgrade head
```

(Optional) Seed the database.

```bash
docker compose exec backend python seed.py
```

---

# 🌐 Docker Networking

Inside Docker, services communicate using service names instead of `localhost`.

| Connection | Address |
|------------|----------|
| Frontend → Backend | `http://backend:8000` |
| Backend → PostgreSQL | `postgresql://postgres:password@db:5432/text2sql` |
| Backend → Ollama | `http://host.docker.internal:11434` |

### Why is Ollama outside Docker?

Keeping Ollama on the host machine provides:

- Faster startup
- Better GPU compatibility
- Easier model management
- Smaller Docker images

The backend accesses Ollama using `host.docker.internal`.

---

# ⚙️ Local Development

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start PostgreSQL.

```bash
docker compose up db -d
```

Run migrations.

```bash
alembic upgrade head
```

Start FastAPI.

```bash
uvicorn app.main:app --reload
```

Start Streamlit.

```bash
streamlit run streamlit_app.py
```

---

# 📡 API

## POST `/query`

### Request

```json
{
  "question": "Top 5 customers by spending"
}
```

### Success Response

```json
{
  "sql": "SELECT ... LIMIT 5;",
  "reason": "Joined customers and orders and ranked by spending.",
  "rows_returned": 5,
  "data": []
}
```

### Clarification Response

```json
{
  "type": "clarification",
  "question": "Which sales do you mean?",
  "options": [
    "Revenue",
    "Order Count",
    "Monthly Sales"
  ]
}
```

---

# 🔒 Security Features

Instead of trusting LLM output directly, every generated query passes through multiple protection layers.

- Dynamic schema grounding
- Structured LLM outputs
- SQL AST validation
- `SELECT`-only whitelist
- Automatic `LIMIT`
- Multi-statement blocking
- Safe SQL execution with SQLAlchemy

---

# 🧪 Testing

Run the included test scripts.

```bash
python test_validator.py
python test_executor.py
python test_clarifier.py
```

---

# ⚖️ Engineering Decisions

| Challenge | Solution |
|-----------|----------|
| Hallucinated columns | Dynamic schema grounding |
| Ambiguous requests | Clarification Engine |
| Unsafe SQL | AST validation with sqlglot |
| Large result sets | Automatic LIMIT |
| Non-JSON DB types | Serializer |
| Schema evolution | Alembic |
| Service orchestration | Docker Compose |
| Local LLM integration | Host-based Ollama |

---

# 🚀 Future Improvements

- Conversation memory
- Query history
- Streaming responses
- Query execution analytics
- Role-based database permissions
- Query cost estimation
- Multi-database support



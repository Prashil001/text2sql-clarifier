"""Reusable UI components for the Text2SQL Clarifier Streamlit app."""

import streamlit as st
import pandas as pd
from typing import Any

from frontend.utils import get_timestamp, format_sql, data_to_csv, EXAMPLE_PROMPTS
from frontend.api import check_backend_health


# ──────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────

def render_hero() -> None:
    """Render the hero section with title and subtitle."""
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-title">🧠 Text2SQL Clarifier</div>
            <div class="hero-divider"></div>
            <div class="hero-subtitle">Natural Language → Safe PostgreSQL Queries</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Empty State
# ──────────────────────────────────────────────

def render_empty_state() -> None:
    """Render the empty state with example prompts before first query."""
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">✨</div>
            <h3>Ask anything about your database</h3>
            <p>Type a natural language question and I'll convert it to SQL,
            validate it, and return the results — safely.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align:center; color: #9ca3af; font-size:0.8rem; "
        "margin-bottom:0.75rem;'>Try one of these examples</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for idx, prompt in enumerate(EXAMPLE_PROMPTS):
        with cols[idx % 2]:
            if st.button(f"→  {prompt}", key=f"example_{idx}", use_container_width=True):
                st.session_state["pending_prompt"] = prompt
                st.rerun()


# ──────────────────────────────────────────────
# Pipeline Animation
# ──────────────────────────────────────────────

PIPELINE_STEPS: list[tuple[str, str]] = [
    ("Understanding your question...", "🔍"),
    ("Checking ambiguity...", "🤔"),
    ("Generating SQL...", "⚙️"),
    ("Validating SQL...", "✅"),
    ("Executing query...", "🚀"),
]


def render_pipeline_animation() -> None:
    """Render the animated pipeline using st.status.

    This is called inside a st.status context from the main app.
    It simulates the pipeline steps visually.
    """
    import time

    for label, icon in PIPELINE_STEPS:
        st.write(f"{icon}  {label}")
        time.sleep(0.5)
    st.write("✅  Done!")


# ──────────────────────────────────────────────
# Clarification UI
# ──────────────────────────────────────────────

def render_clarification(response: dict[str, Any], msg_idx: int) -> None:
    """Render a clarification response with clickable option buttons.

    Args:
        response: The clarification response from the API.
        msg_idx: The message index for unique button keys.
    """
    question = response.get("question", "Could you clarify?")
    options = response.get("options", [])

    st.markdown(f"**{question}**")
    st.markdown("")

    for opt_idx, option in enumerate(options):
        col_key = f"clarify_{msg_idx}_{opt_idx}"
        if st.button(
            f"  {option}  ",
            key=col_key,
            use_container_width=True,
        ):
            st.session_state["pending_prompt"] = option
            st.rerun()


# ──────────────────────────────────────────────
# SQL Display
# ──────────────────────────────────────────────

def render_sql_section(sql: str) -> None:
    """Render the generated SQL in an expander with copy support.

    Args:
        sql: The generated SQL string.
    """
    formatted = format_sql(sql)

    with st.expander("📝  Generated SQL", expanded=False):
        st.code(formatted, language="sql")
        st.button(
            "📋  Copy SQL",
            key=f"copy_sql_{hash(sql)}",
            on_click=_copy_to_clipboard,
            args=(formatted,),
        )


def _copy_to_clipboard(text: str) -> None:
    """Set SQL text in session state for clipboard JS injection.

    Args:
        text: The text to copy.
    """
    st.session_state["clipboard_text"] = text


# ──────────────────────────────────────────────
# Reason Card
# ──────────────────────────────────────────────

def render_reason_card(reason: str) -> None:
    """Render the AI reasoning explanation card.

    Args:
        reason: The explanation from the backend.
    """
    st.markdown(
        f"""
        <div class="reason-card">
            <div class="reason-label">💡 Why this SQL was generated</div>
            {reason}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Results Table
# ──────────────────────────────────────────────

def render_results_table(data: list[Any], rows_returned: int) -> None:
    """Render the query results as a sortable, scrollable dataframe.

    Args:
        data: The query result rows.
        rows_returned: The number of rows returned.
    """
    st.markdown(
        f'<div class="metric-badge">📊 Rows Returned: {rows_returned}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, height=min(400, 35 * len(df) + 38))

        # Download CSV button
        csv_data = data_to_csv(data)
        st.download_button(
            label="⬇️  Download CSV",
            data=csv_data,
            file_name="query_results.csv",
            mime="text/csv",
            key=f"download_{hash(str(data)[:100])}",
        )
    else:
        st.info("Query executed successfully but returned no rows.")


# ──────────────────────────────────────────────
# Success Response (combined)
# ──────────────────────────────────────────────

def render_success_response(response: dict[str, Any]) -> None:
    """Render a complete success response with SQL, reason, and data.

    Args:
        response: The success response from the API.
    """
    render_sql_section(response.get("sql", ""))
    render_reason_card(response.get("reason", "No explanation provided."))
    render_results_table(
        response.get("data", []),
        response.get("rows_returned", 0),
    )


# ──────────────────────────────────────────────
# Message Timestamp
# ──────────────────────────────────────────────

def render_timestamp(timestamp: str) -> None:
    """Render a small timestamp below a message.

    Args:
        timestamp: The formatted timestamp string.
    """
    st.markdown(
        f'<div class="msg-timestamp">{timestamp}</div>',
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────

def render_sidebar() -> None:
    """Render the full sidebar with project info, examples, and status."""
    with st.sidebar:
        # Project branding
        st.markdown("### 🧠  Text2SQL Clarifier")
        st.markdown(
            "<p style='color: #9ca3af; font-size:0.8rem; margin-top:-0.5rem;'>"
            "AI-Powered SQL Assistant</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        # Tech Stack
        st.markdown("### ⚙️  Tech Stack")
        tech_items = [
            ("⚡", "FastAPI"),
            ("🤖", "Ollama Qwen 3"),
            ("🐘", "PostgreSQL"),
            ("🔗", "SQLAlchemy"),
            ("🔍", "sqlglot"),
            ("🦜", "LangChain"),
            ("🐳", "Docker"),
        ]
        badges_html = " ".join(
            f'<span class="tech-badge">{icon} {name}</span>'
            for icon, name in tech_items
        )
        st.markdown(badges_html, unsafe_allow_html=True)
        st.markdown("")
        st.divider()

        # Example Queries
        st.markdown("### 💬  Example Queries")
        for idx, prompt in enumerate(EXAMPLE_PROMPTS):
            if st.button(
                f"→  {prompt}",
                key=f"sidebar_example_{idx}",
                use_container_width=True,
            ):
                st.session_state["pending_prompt"] = prompt
                st.rerun()

        st.divider()

        # Conversation Controls
        st.markdown("### 🗂️  Conversation")
        if st.button("🗑️  Clear Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state.pop("pending_prompt", None)
            st.rerun()

        st.divider()

        # Backend Status
        st.markdown("### 📡  Backend Status")
        _render_backend_status()


@st.cache_data(ttl=30)
def _cached_health_check() -> bool:
    """Cached backend health check (30s TTL).

    Returns:
        True if backend is reachable.
    """
    return check_backend_health()


def _render_backend_status() -> None:
    """Render the backend connection status indicator."""
    is_online = _cached_health_check()

    if is_online:
        st.markdown(
            '<span class="status-dot status-online"></span> '
            '<span style="color: #059669; font-weight: 600;">Connected</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-dot status-offline"></span> '
            '<span style="color: #dc2626; font-weight: 600;">Backend Offline</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color: #9ca3af; font-size:0.75rem; margin-top:0.3rem;'>"
            "Start the backend with:<br>"
            "<code>uvicorn app.main:app --reload</code></p>",
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# Clipboard JS injection
# ──────────────────────────────────────────────

def inject_clipboard_js() -> None:
    """Inject JavaScript to copy text to clipboard if requested."""
    if "clipboard_text" in st.session_state:
        text = st.session_state.pop("clipboard_text")
        escaped = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        st.markdown(
            f"""
            <script>
            navigator.clipboard.writeText(`{escaped}`).then(function() {{
                // success
            }});
            </script>
            """,
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────
# Error Display
# ──────────────────────────────────────────────

def render_error_message(error: Exception) -> str:
    """Convert an exception to a user-friendly error message.

    Args:
        error: The caught exception.

    Returns:
        A friendly error message string.
    """
    if isinstance(error, ConnectionError):
        return (
            "🔴 **Cannot connect to the backend.**\n\n"
            "Please make sure the FastAPI server is running:\n"
            "```bash\nuvicorn app.main:app --reload\n```"
        )
    if isinstance(error, TimeoutError):
        return (
            "⏳ **Request timed out.**\n\n"
            "The AI model may be processing a complex query. "
            "Please try again in a moment."
        )
    if isinstance(error, ValueError):
        return (
            "⚠️ **Invalid response from backend.**\n\n"
            "The server returned an unexpected format. "
            "Please check the backend logs."
        )
    if isinstance(error, RuntimeError):
        return f"❌ **Error:** {error}"

    return f"❌ **An unexpected error occurred:** {error}"

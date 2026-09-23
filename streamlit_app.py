"""
Text2SQL Clarifier — Streamlit Frontend
========================================
A premium dark-themed chat interface for the Text2SQL Clarifier backend.
Communicates exclusively with the FastAPI backend via the /query endpoint.

Run:
    streamlit run streamlit_app.py
"""

import streamlit as st

from frontend.styles import get_custom_css
from frontend.api import send_query, is_clarification_response
from frontend.utils import get_timestamp
from frontend.components import (
    render_hero,
    render_empty_state,
    render_pipeline_animation,
    render_clarification,
    render_success_response,
    render_timestamp,
    render_sidebar,
    render_error_message,
    inject_clipboard_js,
)


# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Text2SQL Clarifier",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────

def _init_session_state() -> None:
    """Initialize all session state variables on first load."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "pending_prompt" not in st.session_state:
        st.session_state["pending_prompt"] = None


_init_session_state()


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────

render_sidebar()


# ──────────────────────────────────────────────
# Hero Section
# ──────────────────────────────────────────────

render_hero()


# ──────────────────────────────────────────────
# Chat History
# ──────────────────────────────────────────────

def _render_chat_history() -> None:
    """Render all messages from the conversation history."""
    if not st.session_state["messages"]:
        render_empty_state()
        return

    for idx, message in enumerate(st.session_state["messages"]):
        role = message["role"]
        with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🧠"):
            if role == "user":
                st.markdown(message["content"])
            elif message.get("type") == "clarification":
                render_clarification(message["response"], idx)
            elif message.get("type") == "error":
                st.markdown(message["content"])
            else:
                render_success_response(message["response"])

            # Timestamp
            if "timestamp" in message:
                render_timestamp(message["timestamp"])


_render_chat_history()


# ──────────────────────────────────────────────
# Process Query
# ──────────────────────────────────────────────

def _process_query(question: str) -> None:
    """Send a query to the backend and handle the response.

    Adds messages to session state and triggers the pipeline animation.

    Args:
        question: The natural language question to send.
    """
    timestamp = get_timestamp()

    # Add user message
    st.session_state["messages"].append({
        "role": "user",
        "content": question,
        "timestamp": timestamp,
    })

    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(question)
        render_timestamp(timestamp)

    # Display assistant response with pipeline animation
    with st.chat_message("assistant", avatar="🧠"):
        try:
            with st.status("🔄  Processing your query...", expanded=True) as status:
                render_pipeline_animation()
                response = send_query(question)
                status.update(
                    label="✅  Query completed!",
                    state="complete",
                    expanded=False,
                )

            response_timestamp = get_timestamp()

            if is_clarification_response(response):
                st.session_state["messages"].append({
                    "role": "assistant",
                    "type": "clarification",
                    "response": response,
                    "timestamp": response_timestamp,
                })
                render_clarification(
                    response,
                    len(st.session_state["messages"]) - 1,
                )
            else:
                st.session_state["messages"].append({
                    "role": "assistant",
                    "type": "success",
                    "response": response,
                    "timestamp": response_timestamp,
                })
                render_success_response(response)

            render_timestamp(response_timestamp)

        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as e:
            error_msg = render_error_message(e)
            st.session_state["messages"].append({
                "role": "assistant",
                "type": "error",
                "content": error_msg,
                "timestamp": get_timestamp(),
            })
            st.markdown(error_msg)
            render_timestamp(get_timestamp())


# ──────────────────────────────────────────────
# Input Handling
# ──────────────────────────────────────────────

# Handle pending prompt from example buttons
if st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")
    _process_query(prompt)

# Handle chat input (Enter key submits)
if user_input := st.chat_input("Ask a question about your database..."):
    _process_query(user_input)


# ──────────────────────────────────────────────
# Clipboard JS Injection
# ──────────────────────────────────────────────

inject_clipboard_js()


# ──────────────────────────────────────────────
# Auto-scroll (JS injection)
# ──────────────────────────────────────────────

if st.session_state["messages"]:
    st.markdown(
        """
        <script>
        window.setTimeout(function() {
            var chatContainer = window.parent.document.querySelector(
                'section.main'
            );
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }, 200);
        </script>
        """,
        unsafe_allow_html=True,
    )

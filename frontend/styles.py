"""Custom CSS styles for the Text2SQL Clarifier Streamlit app."""


def get_custom_css() -> str:
    """Return the complete custom CSS for a minimalistic light theme."""
    return """
    <style>
    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    div[data-testid="stStatusWidget"] {display: none;}

    /* ===== BASE ===== */
    :root {
        --bg: #ffffff;
        --bg-subtle: #f8f9fb;
        --bg-muted: #f1f3f5;
        --border: #e5e7eb;
        --border-focus: #6366f1;
        --text: #1a1a2e;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --accent: #4f46e5;
        --accent-light: #eef2ff;
        --success: #059669;
        --success-light: #ecfdf5;
        --error: #dc2626;
        --error-light: #fef2f2;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .main .block-container {
        max-width: 820px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* ===== HERO ===== */
    .hero-section {
        text-align: center;
        padding: 2.5rem 0 1rem 0;
    }

    .hero-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        color: var(--text-muted);
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.25rem;
    }

    .hero-divider {
        width: 40px;
        height: 2px;
        background: var(--accent);
        margin: 0.75rem auto;
        border-radius: 1px;
    }

    /* ===== CHAT MESSAGES ===== */
    div[data-testid="stChatMessage"] {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ===== CHAT INPUT ===== */
    div[data-testid="stChatInput"] textarea {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-size: 0.9rem !important;
    }

    div[data-testid="stChatInput"] textarea:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        background: var(--bg-subtle) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ===== EXPANDER ===== */
    div[data-testid="stExpander"] {
        background: var(--bg-subtle) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] details summary {
        color: var(--text) !important;
        font-weight: 500;
        font-size: 0.85rem;
    }

    /* ===== CODE ===== */
    pre {
        background: var(--bg-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.875rem !important;
    }

    code {
        color: var(--accent) !important;
        font-size: 0.82rem !important;
    }

    /* ===== DATAFRAME ===== */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: var(--bg-subtle) !important;
        border-right: 1px solid var(--border) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-secondary);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-top: 1.25rem;
    }

    /* ===== REASON CARD ===== */
    .reason-card {
        background: var(--accent-light);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .reason-card .reason-label {
        color: var(--accent);
        font-weight: 600;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.25rem;
    }

    /* ===== METRIC BADGE ===== */
    .metric-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: var(--success-light);
        border: 1px solid rgba(5, 150, 105, 0.15);
        border-radius: 6px;
        padding: 0.25rem 0.6rem;
        color: var(--success);
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem 1rem 1rem;
    }

    .empty-state .icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }

    .empty-state h3 {
        color: var(--text);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    .empty-state p {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }

    /* ===== TIMESTAMP ===== */
    .msg-timestamp {
        color: var(--text-muted);
        font-size: 0.65rem;
        margin-top: 0.4rem;
        text-align: right;
    }

    /* ===== STATUS DOT ===== */
    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        margin-right: 5px;
    }

    .status-online {
        background: var(--success);
    }

    .status-offline {
        background: var(--error);
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        font-size: 0.78rem !important;
    }

    .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ===== TECH BADGE ===== */
    .tech-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.2rem;
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.2rem 0.5rem;
        color: var(--text-secondary);
        font-size: 0.72rem;
        margin: 0.15rem;
    }
    </style>
    """

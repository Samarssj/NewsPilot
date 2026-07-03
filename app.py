"""Streamlit UI for the Hybrid News Intelligence Assistant.

Visual identity: "Wire Desk" — an AI newsroom wire service. Ink-dark
panels, a brass accent, a serif masthead, and mono-set metadata like an
old press ticker. Source attributions read like wire-service stamps.
"""
import streamlit as st
import config
from news_fetcher import fetch_latest_news
from vector_store import NewsVectorStore
from rag_engine import NewsRAGEngine, SOURCE_NEWS

st.set_page_config(
    page_title="NewsPilot — News AI",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme state (must exist before we build the stylesheet)
# ---------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # default to dark

dark = st.session_state.dark_mode

# ---------------------------------------------------------------------------
# Token system
# ---------------------------------------------------------------------------
if dark:
    ink = "#0b0f14"
    ink_2 = "#121821"
    ink_3 = "#1a2029"
    hairline = "rgba(201, 162, 39, 0.18)"
    text = "#e9e6dd"
    text_muted = "#8b93a1"
    brass = "#e93b14"
    brass_bright = "#36cf52"
    verified = "#7fbf8f"
    general = "#8ba3c9"
    shadow = "0 8px 24px rgba(0,0,0,0.35)"
else:
    ink = "#f3f4f7"
    ink_2 = "#ffffff"
    ink_3 = "#ffffff"
    hairline = "rgba(150, 118, 30, 0.28)"
    text = "#1b1f27"
    text_muted = "#5c6472"
    brass = "#9c7a13"
    brass_bright = "#eb6e0f"
    verified = "#2f8f52"
    general = "#3f5f9c"
    shadow = "0 6px 18px rgba(30,25,10,0.08)"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

    :root {{
        --ink: {ink}; --ink-2: {ink_2}; --ink-3: {ink_3};
        --hairline: {hairline}; --text: {text}; --text-muted: {text_muted};
        --brass: {brass}; --brass-bright: {brass_bright};
        --verified: {verified}; --general: {general}; --shadow: {shadow};
    }}

    html, body, .stApp {{
        background-color: var(--ink) !important;
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {{
        color: var(--text);
    }}
    ::selection {{ background: var(--brass); color: #10131a; }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-track {{ background: var(--ink); }}
    ::-webkit-scrollbar-thumb {{ background: var(--hairline); border-radius: 6px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--brass); }}

    /* Kill default Streamlit top padding so the masthead sits high */
    .block-container {{ padding-top: 1.4rem; max-width: 900px; }}

    /* ---------------- Masthead ---------------- */
    .masthead {{
        border-bottom: 1px solid var(--hairline);
        padding-bottom: 1rem;
        margin-bottom: 0.4rem;
    }}
    .masthead .eyebrow {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--brass);
        margin-bottom: 0.35rem;
    }}
    .masthead h1 {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.6rem;
        line-height: 1.05;
        margin: 0 0 0.4rem 0;
        color: var(--text);
        letter-spacing: -0.01em;
    }}
    .masthead .dek {{
        font-size: 0.98rem;
        color: var(--text-muted);
        max-width: 640px;
        line-height: 1.5;
    }}

    /* Ticker */
    .ticker-wrap {{
        overflow: hidden;
        border-top: 1px solid var(--hairline);
        border-bottom: 1px solid var(--hairline);
        background: var(--ink-2);
        margin: 0.9rem 0 1.3rem 0;
        white-space: nowrap;
    }}
    .ticker {{
        display: inline-block;
        padding: 0.45rem 0;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.76rem;
        letter-spacing: 0.04em;
        color: var(--text-muted);
        animation: scroll-ticker 32s linear infinite;
    }}
    .ticker span {{ color: var(--brass); margin: 0 0.5rem; }}
    @keyframes scroll-ticker {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .ticker {{ animation: none; }}
    }}

    /* ---------------- Sidebar ---------------- */
    [data-testid="stSidebar"] {{
        background-color: var(--ink-2);
        border-right: 1px solid var(--hairline);
    }}
    [data-testid="stSidebar"] * {{ color: var(--text); }}
    [data-testid="stSidebar"] .sidebar-mast {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.3rem;
        letter-spacing: -0.01em;
    }}
    [data-testid="stSidebar"] .sidebar-eyebrow {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.2rem;
    }}
    [data-testid="stSidebar"] hr {{ border-color: var(--hairline); }}
    .stApp [data-testid="stSidebarUserContent"] h3 {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--brass);
        margin-top: 0.6rem;
    }}

    /* Stat cards */
    .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin: 0.6rem 0 0.2rem 0; }}
    .stat-card {{
        background: var(--ink-3);
        border: 1px solid var(--hairline);
        border-radius: 6px;
        padding: 0.6rem 0.7rem;
    }}
    .stat-card .num {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.35rem;
        font-weight: 500;
        color: var(--text);
    }}
    .stat-card .lbl {{
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
    }}

    /* ---------------- Inputs & buttons ---------------- */
    .stTextInput input, .stChatInput textarea, textarea {{
        background-color: var(--ink-3) !important;
        color: var(--text) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 6px !important;
    }}
    .stTextInput input:focus, .stChatInput textarea:focus {{
        border-color: var(--brass) !important;
        box-shadow: 0 0 0 1px var(--brass) !important;
    }}
    .stButton button {{
        background-color: var(--ink-3);
        color: var(--text);
        border: 1px solid var(--hairline);
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
    }}
    .stButton button:hover {{
        border-color: var(--brass);
        color: var(--brass-bright);
        transform: translateY(-1px);
    }}
    .stButton button[kind="primary"] {{
        background-color: var(--brass);
        color: #171308;
        border: none;
        font-weight: 600;
    }}
    .stButton button[kind="primary"]:hover {{
        background-color: var(--brass-bright);
        color: #171308;
    }}
    [data-testid="stSlider"] [role="slider"] {{ background-color: var(--brass) !important; }}

    /* Suggested prompt cards */
    .prompt-eyebrow {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 1rem 0 0.5rem 0;
    }}

    /* ---------------- Chat ---------------- */
    [data-testid="stChatMessage"] {{
        background-color: var(--ink-2);
        border: 1px solid var(--hairline);
        border-radius: 10px;
        box-shadow: var(--shadow);
    }}

    /* Stamp badges */
    .stamp {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 4px;
        border: 1px solid currentColor;
        margin-bottom: 0.55rem;
    }}
    .stamp-verified {{ color: var(--verified); background: color-mix(in srgb, var(--verified) 12%, transparent); }}
    .stamp-general {{ color: var(--general); background: color-mix(in srgb, var(--general) 12%, transparent); }}

    /* Source clippings */
    .clip {{
        border-left: 2px solid var(--brass);
        background: var(--ink-3);
        border-radius: 0 6px 6px 0;
        padding: 0.55rem 0.8rem;
        margin-bottom: 0.45rem;
        transition: background 0.15s ease;
    }}
    .clip:hover {{ background: color-mix(in srgb, var(--brass) 8%, var(--ink-3)); }}
    .clip a {{
        text-decoration: none; font-weight: 600; color: var(--text);
    }}
    .clip a:hover {{ color: var(--brass-bright); }}
    .clip .meta {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 2px;
    }}

    .stExpander, [data-testid="stExpander"] {{
        background-color: var(--ink-2);
        border: 1px solid var(--hairline) !important;
        border-radius: 8px;
    }}

    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{ color: var(--text) !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Cached resources
# ---------------------------------------------------------------------------
@st.cache_resource
def get_store() -> NewsVectorStore:
    return NewsVectorStore()


@st.cache_resource
def get_engine(_store: NewsVectorStore) -> NewsRAGEngine:
    return NewsRAGEngine(vector_store=_store)


store = get_store()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of dicts: role, content, source, sources
if "last_fetch_count" not in st.session_state:
    st.session_state.last_fetch_count = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.markdown(
            "<div class='sidebar-eyebrow'>AI NEWS Service</div>"
            "<div class='sidebar-mast'>🗞️ NewsPilot</div>",
            unsafe_allow_html=True,
        )
    with top_right:
        st.toggle("🌙", key="dark_mode", help="Toggle dark / light mode")

    st.caption("Hybrid RAG — live news first, general knowledge as fallback.")

    st.markdown(
        f"""
        <div class="stat-grid">
            <div class="stat-card">
                <div class="num">{store.count()}</div>
                <div class="lbl">Chunks indexed</div>
            </div>
            <div class="stat-card">
                <div class="num">{len(st.session_state.chat_history) // 2}</div>
                <div class="lbl">Chat turns</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("🔄 Refresh news")
    query = st.text_input("Optional topic filter (NewsAPI)", "", placeholder="e.g. inflation, AI, elections")
    fulltext = st.checkbox("Extract full article text (slower, better quality)", value=True)

    if st.button("Fetch latest news", type="primary", use_container_width=True):
        with st.spinner("Fetching and indexing latest news..."):
            articles = fetch_latest_news(query=query or None, fetch_full_text=fulltext)
            added = store.add_articles(articles)
        st.session_state.last_fetch_count = (len(articles), added)
        st.success(f"Fetched {len(articles)} articles, added {added} new chunks.")
        st.rerun()

    if st.session_state.last_fetch_count:
        fetched, added = st.session_state.last_fetch_count
        st.caption(f"Last refresh: {fetched} fetched · {added} new chunks")

    st.divider()
    st.subheader("⚙️ Retrieval settings")
    top_k = st.slider("Sources to retrieve per question", 3, 12, config.TOP_K_DEFAULT)
    distance_threshold = st.slider(
        "Relevance threshold (lower = stricter)",
        min_value=0.05,
        max_value=1.5,
        value=config.RAG_DISTANCE_THRESHOLD,
        step=0.05,
        help=(
            "Maximum cosine distance for a retrieved article to count as "
            "'relevant'. If no retrieved article is this close to the "
            "question, the assistant falls back to Gemini's general "
            "knowledge instead of forcing an answer from unrelated news."
        ),
    )
    config.RAG_DISTANCE_THRESHOLD = distance_threshold

    use_fallback = st.checkbox(
        "Allow Gemini general-knowledge fallback",
        value=config.ENABLE_GEMINI_FALLBACK,
        help="If unchecked, the assistant behaves like a news-only bot again.",
    )
    config.ENABLE_GEMINI_FALLBACK = use_fallback

    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ---------------------------------------------------------------------------
# Masthead
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="masthead">
        <div class="eyebrow">Hybrid Retrieval &nbsp;·&nbsp; Live Index &nbsp;·&nbsp; Wire Service</div>
        <h1>News Intelligence</h1>
        <div class="dek">Ask about current events. Answers are pulled from the live
        indexed wire when relevant, and fall back to general knowledge when they're not.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {store.count()} CHUNKS INDEXED <span>//</span>
            RETRIEVAL {"ON" if config.ENABLE_GEMINI_FALLBACK else "STRICT"} <span>//</span>
            TOP-K {top_k} <span>//</span>
            THRESHOLD {distance_threshold:.2f} <span>//</span>
            {store.count()} CHUNKS INDEXED <span>//</span>
            RETRIEVAL {"ON" if config.ENABLE_GEMINI_FALLBACK else "STRICT"} <span>//</span>
            TOP-K {top_k} <span>//</span>
            THRESHOLD {distance_threshold:.2f} <span>//</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if store.count() == 0:
    st.warning(
        "Your news index is empty. Use **Fetch latest news** in the sidebar "
        "to index some articles before asking questions.",
        icon="⚠️",
    )

# Suggested prompts (shown only before the first question)
if not st.session_state.chat_history:
    st.markdown("<div class='prompt-eyebrow'>Try asking</div>", unsafe_allow_html=True)
    suggestions = [
        "What's the latest on interest rate decisions?",
        "Any major tech industry news today?",
        "Summarize recent developments in AI regulation.",
        "What's happening with global markets right now?",
    ]
    cols = st.columns(len(suggestions))
    clicked_suggestion = None
    for col, s in zip(cols, suggestions):
        if col.button(s, use_container_width=True):
            clicked_suggestion = s
else:
    clicked_suggestion = None

# ---------------------------------------------------------------------------
# Chat rendering helpers
# ---------------------------------------------------------------------------
def render_stamp(source: str) -> None:
    if source == SOURCE_NEWS:
        st.markdown(
            "<span class='stamp stamp-verified'>🗞️ Wire — News Database</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<span class='stamp stamp-general'>🤖 General Knowledge</span>",
            unsafe_allow_html=True,
        )


def render_sources(sources) -> None:
    if not sources:
        return
    with st.expander(f"View {len(sources)} source(s)"):
        for s in sources:
            published = f" · {s['published']}" if s["published"] else ""
            st.markdown(
                f"<div class='clip'>"
                f"<a href='{s['url']}' target='_blank'>[{s['n']}] {s['title']}</a>"
                f"<div class='meta'>{s['source']}{published}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )


# Render existing chat history
for turn in st.session_state.chat_history:
    avatar = "🧑" if turn["role"] == "user" else "🗞️"
    with st.chat_message(turn["role"], avatar=avatar):
        if turn["role"] == "assistant":
            render_stamp(turn["source"])
            st.write(turn["content"])
            if turn["source"] == SOURCE_NEWS:
                render_sources(turn.get("sources"))
        else:
            st.write(turn["content"])

# Chat input (pinned at the bottom automatically by Streamlit)
typed_question = st.chat_input("Ask about the latest news...")
question = clicked_suggestion or typed_question

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    with st.chat_message("assistant", avatar="🗞️"):
        with st.spinner("Retrieving relevant articles and generating answer..."):
            engine = get_engine(store)
            result = engine.ask(question, top_k=top_k)

        render_stamp(result["source"])
        st.write(result["answer"])

        if result["source"] == SOURCE_NEWS:
            render_sources(result.get("sources"))

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "source": result["source"],
            "sources": result.get("sources", []),
        }
    )
    st.rerun()

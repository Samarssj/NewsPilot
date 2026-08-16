"""NewsPilot — a polished, chat-first news intelligence workspace."""

from __future__ import annotations

import html
from typing import Any

import plotly.graph_objects as go
import streamlit as st


# Import project modules after the standard-library and visualization imports.
# The app intentionally avoids set_page_config so it can be embedded or relaunched
# cleanly by different Streamlit runners without stale page state.
import config
from news_fetcher import fetch_latest_news
from rag_engine import SOURCE_GEMINI, SOURCE_NEWS, NewsRAGEngine
from vector_store import NewsVectorStore


# -----------------------------------------------------------------------------
# Theme and visual system
# -----------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

if dark:
    colors = {
        "bg": "#0e080a",
        "panel": "#171013",
        "panel_2": "#211419",
        "panel_3": "#2b1a20",
        "text": "#fff4f5",
        "muted": "#b59ca3",
        "line": "rgba(255, 150, 160, 0.18)",
        "accent": "#e5484d",
        "accent_2": "#ff8a8f",
        "cyan": "#ffb4a2",
        "green": "#78d6a6",
        "orange": "#ffc078",
        "danger": "#ff6b78",
        "shadow": "0 22px 60px rgba(45, 5, 12, 0.38)",
    }
else:
    colors = {
        "bg": "#fff7f7",
        "panel": "#ffffff",
        "panel_2": "#fff0f1",
        "panel_3": "#ffe4e6",
        "text": "#2b1115",
        "muted": "#7e5d64",
        "line": "rgba(145, 45, 58, 0.16)",
        "accent": "#c9303e",
        "accent_2": "#a51f2d",
        "cyan": "#d65a63",
        "green": "#188d62",
        "orange": "#a86114",
        "danger": "#c33145",
        "shadow": "0 18px 44px rgba(126, 34, 48, 0.12)",
    }


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,500,0,0..1&display=swap');

    :root {{
        --bg: {colors['bg']}; --panel: {colors['panel']}; --panel-2: {colors['panel_2']};
        --panel-3: {colors['panel_3']}; --text: {colors['text']}; --muted: {colors['muted']};
        --line: {colors['line']}; --accent: {colors['accent']}; --accent-2: {colors['accent_2']};
        --cyan: {colors['cyan']}; --green: {colors['green']}; --orange: {colors['orange']};
        --danger: {colors['danger']}; --shadow: {colors['shadow']};
    }}

    html, body, .stApp {{ background: var(--bg) !important; color: var(--text); }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {{
        color: var(--text); font-family: 'DM Sans', sans-serif;
    }}
    .ui-icon {{ display: inline-block; width: 1.15em; text-align: center; line-height: 1; font-size: 1.05em; vertical-align: -0.04em; }}
    .block-container {{ max-width: 1480px; padding: 1.6rem 2.4rem 4rem; }}
    [data-testid='stSidebar'] {{ background: var(--panel); border-right: 1px solid var(--line); }}
    [data-testid='stSidebar'] * {{ color: var(--text); }}
    [data-testid='stSidebar'] .block-container {{ padding: 1.2rem 1rem; }}
    [data-testid='stSidebar'] hr {{ border-color: var(--line); margin: 1rem 0; }}
    [data-testid='stSidebarCollapseButton'] button,
    [data-testid='stSidebarCollapsedControl'] button {{
        background: var(--panel-3) !important; color: var(--accent) !important;
        border: 1px solid var(--line) !important; border-radius: 10px !important;
        box-shadow: 0 6px 16px color-mix(in srgb, var(--accent) 18%, transparent) !important;
    }}
    [data-testid='stSidebarCollapseButton'] button:hover,
    [data-testid='stSidebarCollapsedControl'] button:hover {{
        background: color-mix(in srgb, var(--accent) 14%, var(--panel-3)) !important;
        color: var(--accent-2) !important;
    }}
    [data-testid='stSidebarCollapseButton'] svg,
    [data-testid='stSidebarCollapsedControl'] svg {{ color: var(--accent) !important; fill: currentColor !important; }}
    [data-testid='stSidebar'] label[data-baseweb='checkbox']:has(input[aria-label='Dark mode']) {{
        color: var(--text) !important; min-height: 2rem; align-items: center;
    }}
    [data-testid='stSidebar'] label[data-baseweb='checkbox']:has(input[aria-label='Dark mode']) > div:first-of-type {{
        background: var(--panel-3) !important; border: 1px solid var(--line) !important;
        border-radius: 999px !important; box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 10%, transparent) !important;
    }}
    [data-testid='stSidebar'] label[data-baseweb='checkbox']:has(input[aria-label='Dark mode']) > div:first-of-type > div:first-child {{
        background: var(--accent) !important; border-color: var(--accent) !important;
    }}
    ::-webkit-scrollbar {{ width: 9px; height: 9px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: var(--panel-3); border-radius: 8px; }}

    .brand {{ display: flex; align-items: center; gap: 0.7rem; margin: 0.1rem 0 1.4rem; }}
    .brand-mark {{
        width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center;
        color: #fff; background: linear-gradient(135deg, var(--accent), #ff7a7f);
        box-shadow: 0 10px 26px color-mix(in srgb, var(--accent) 30%, transparent);
    }}
    .brand-name {{ font: 800 1.05rem 'Manrope', sans-serif; letter-spacing: -0.03em; }}
    .brand-sub {{ color: var(--muted) !important; font: 500 0.68rem 'DM Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }}
    .side-label {{ color: var(--muted) !important; font: 500 0.68rem 'DM Mono', monospace; letter-spacing: 0.12em; text-transform: uppercase; margin: 1.2rem 0 0.5rem; }}

    .hero {{
        background: radial-gradient(circle at 84% 10%, color-mix(in srgb, var(--accent) 18%, transparent), transparent 30%),
                    linear-gradient(135deg, var(--panel), var(--panel-2));
        border: 1px solid var(--line); border-radius: 24px; padding: 2.15rem 2.35rem;
        box-shadow: var(--shadow); position: relative; overflow: hidden; margin-bottom: 1rem;
    }}
    .hero::after {{ content: ''; position: absolute; width: 210px; height: 210px; right: -55px; top: -65px; border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent); border-radius: 50%; box-shadow: 0 0 0 22px color-mix(in srgb, var(--accent) 5%, transparent), 0 0 0 46px color-mix(in srgb, var(--accent) 4%, transparent); }}
    .eyebrow {{ color: var(--accent-2) !important; font: 500 0.68rem 'DM Mono', monospace; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 0.7rem; }}
    .hero h1 {{ font: 800 clamp(2rem, 4vw, 3.35rem) 'Manrope', sans-serif; letter-spacing: -0.06em; line-height: 1.02; margin: 0; max-width: 720px; }}
    .hero-copy {{ color: var(--muted) !important; font-size: 1rem; line-height: 1.6; max-width: 670px; margin: 0.9rem 0 0; }}
    .hero-chip-row {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.35rem; }}
    .hero-chip, .status-pill {{ display: inline-flex; align-items: center; gap: 0.38rem; border: 1px solid var(--line); border-radius: 999px; background: color-mix(in srgb, var(--panel-3) 70%, transparent); color: var(--muted) !important; padding: 0.36rem 0.7rem; font: 500 0.72rem 'DM Mono', monospace; }}
    .hero-chip .ui-icon {{ color: var(--cyan); font-size: 16px; }}

    .metric-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.8rem; margin: 0.9rem 0 1.35rem; }}
    .metric-card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 1rem 1.05rem; box-shadow: var(--shadow); }}
    .metric-top {{ display: flex; justify-content: space-between; align-items: center; color: var(--muted) !important; font: 500 0.68rem 'DM Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }}
    .metric-icon {{ color: var(--accent-2) !important; }}
    .metric-value {{ font: 700 1.55rem 'Manrope', sans-serif; letter-spacing: -0.05em; margin-top: 0.45rem; }}
    .metric-note {{ color: var(--muted) !important; font-size: 0.75rem; margin-top: 0.25rem; }}

    .section-kicker {{ color: var(--muted) !important; font: 500 0.68rem 'DM Mono', monospace; letter-spacing: 0.13em; text-transform: uppercase; margin: 1.2rem 0 0.55rem; }}
    .welcome-card {{ background: linear-gradient(135deg, var(--panel), color-mix(in srgb, var(--accent) 7%, var(--panel))); border: 1px solid var(--line); border-radius: 20px; padding: 1.45rem; margin-bottom: 0.8rem; }}
    .welcome-title {{ font: 700 1.18rem 'Manrope', sans-serif; letter-spacing: -0.03em; }}
    .welcome-copy {{ color: var(--muted) !important; margin: 0.35rem 0 0; line-height: 1.55; }}

    [data-testid='stChatMessage'] {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 0.9rem 1.1rem; box-shadow: 0 10px 32px color-mix(in srgb, #000 10%, transparent); margin-bottom: 0.7rem; }}
    [data-testid='stChatMessage'] [data-testid='stMarkdownContainer'] p {{ line-height: 1.7; }}
    [data-testid='stChatInput'] {{ border-color: var(--line) !important; background: var(--panel) !important; }}
    [data-testid='stChatInput'] textarea {{ background: var(--panel-2) !important; color: var(--text) !important; border: 1px solid var(--line) !important; border-radius: 14px !important; }}
    [data-testid='stChatInput'] textarea:focus {{ border-color: var(--accent) !important; box-shadow: 0 0 0 1px var(--accent) !important; }}
    .stamp {{ display: inline-flex; align-items: center; gap: 0.35rem; border-radius: 999px; padding: 0.34rem 0.62rem; margin-bottom: 0.5rem; font: 500 0.67rem 'DM Mono', monospace; letter-spacing: 0.06em; text-transform: uppercase; }}
    .stamp-news {{ color: var(--green) !important; background: color-mix(in srgb, var(--green) 12%, transparent); border: 1px solid color-mix(in srgb, var(--green) 25%, transparent); }}
    .stamp-general {{ color: var(--orange) !important; background: color-mix(in srgb, var(--orange) 12%, transparent); border: 1px solid color-mix(in srgb, var(--orange) 25%, transparent); }}
    .source-card {{ border-left: 2px solid var(--accent); background: var(--panel-2); border-radius: 0 12px 12px 0; padding: 0.7rem 0.85rem; margin: 0.45rem 0; }}
    .source-card a {{ color: var(--text) !important; text-decoration: none; font-weight: 600; line-height: 1.35; }}
    .source-card a:hover {{ color: var(--accent-2) !important; }}
    .source-meta {{ color: var(--muted) !important; font: 500 0.68rem 'DM Mono', monospace; margin-top: 0.3rem; }}
    .retrieval-summary {{ display: flex; gap: 0.55rem; flex-wrap: wrap; margin: 0.65rem 0 0.3rem; }}
    .retrieval-summary span {{ color: var(--muted) !important; background: var(--panel-2); border: 1px solid var(--line); border-radius: 8px; padding: 0.38rem 0.55rem; font: 500 0.68rem 'DM Mono', monospace; }}
    .retrieval-summary b {{ color: var(--text) !important; }}

    .stButton button {{ background: var(--panel-2); color: var(--text); border: 1px solid var(--line); border-radius: 11px; min-height: 2.4rem; transition: all .15s ease; }}
    .stButton button:hover {{ border-color: var(--accent); color: var(--accent-2); transform: translateY(-1px); }}
    .stButton button[kind='primary'] {{ background: linear-gradient(135deg, var(--accent), #e65a61); border: none; color: #fff; font-weight: 700; }}
    .stButton button[kind='primary']:hover {{ color: #fff; filter: brightness(1.08); }}
    .stTextInput input, .stSelectbox div[data-baseweb='select'] > div, .stNumberInput input {{ background: var(--panel-2) !important; color: var(--text) !important; border-color: var(--line) !important; border-radius: 10px !important; }}
    .stSlider [data-baseweb='slider'] {{ padding-top: 0.3rem; }}
    .stExpander {{ background: var(--panel); border: 1px solid var(--line); border-radius: 13px; }}
    .stTabs [data-baseweb='tab-list'] {{ gap: 0.35rem; }}
    .stTabs [data-baseweb='tab'] {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 0.45rem 0.75rem; }}
    .stTabs [aria-selected='true'] {{ background: color-mix(in srgb, var(--accent) 15%, var(--panel)); color: var(--accent-2) !important; }}
    .empty-state {{ text-align: center; color: var(--muted) !important; border: 1px dashed var(--line); border-radius: 16px; padding: 1.5rem; }}
    @media (max-width: 900px) {{ .block-container {{ padding: 1rem 1rem 3rem; }} .metric-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} .hero {{ padding: 1.4rem; }} }}
    @media (max-width: 768px) {{
        .block-container {{ max-width: 100%; overflow-x: hidden; padding: 0.8rem 0.75rem 4.5rem; }}
        [data-testid='stSidebar'] {{ position: fixed !important; inset: 0 auto 0 0; z-index: 1000; height: 100dvh !important; max-height: 100dvh; border: 0 !important; transition: transform .2s ease, width .2s ease; }}
        [data-testid='stSidebar'][aria-expanded='true'] {{ width: min(86vw, 340px) !important; min-width: min(86vw, 340px) !important; max-width: min(86vw, 340px) !important; transform: translateX(0); box-shadow: 18px 0 45px rgba(0,0,0,.34); overflow-y: auto !important; }}
        [data-testid='stSidebar'][aria-expanded='false'] {{ width: 0 !important; min-width: 0 !important; max-width: 0 !important; transform: translateX(-100%); overflow: hidden !important; }}
        [data-testid='stSidebar'] > div:first-child, [data-testid='stSidebar'] [data-testid='stSidebarContent'] {{ max-width: 100% !important; }}
        [data-testid='stSidebarCollapseButton'] {{ display: block !important; position: absolute; top: .7rem; right: .7rem; z-index: 2; }}
        .hero {{ padding: 1.15rem; border-radius: 18px; }}
        .hero::after {{ display: none; }}
        .hero h1 {{ font-size: 2rem; max-width: 100%; }}
        .hero-copy {{ font-size: 0.9rem; line-height: 1.5; }}
        .hero-chip-row {{ gap: 0.35rem; }}
        .hero-chip {{ font-size: 0.62rem; padding: 0.3rem 0.5rem; }}
        .metric-grid {{ gap: 0.5rem; }}
        .metric-card {{ min-width: 0; padding: 0.75rem 0.65rem; border-radius: 13px; }}
        .metric-top {{ font-size: 0.56rem; }}
        .metric-value {{ font-size: 1.15rem; }}
        .metric-note {{ font-size: 0.66rem; line-height: 1.25; }}
        .welcome-card {{ padding: 1rem; border-radius: 16px; }}
        [data-testid='stChatInput'] {{ padding-bottom: 0.4rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Data and state
# -----------------------------------------------------------------------------
@st.cache_resource
def get_store() -> NewsVectorStore:
    return NewsVectorStore()


@st.cache_resource
def get_engine(_store: NewsVectorStore) -> NewsRAGEngine:
    return NewsRAGEngine(vector_store=_store)


store = get_store()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_fetch_count" not in st.session_state:
    st.session_state.last_fetch_count = None
if "last_retrieval" not in st.session_state:
    st.session_state.last_retrieval = None


ICON_GLYPHS = {
    "auto_awesome": "✦", "verified": "✓", "link": "↗", "open_in_new": "↗",
    "insights": "⌁", "database": "◈", "forum": "◌", "target": "◎", "bolt": "⚡",
    "hub": "⌘", "tune": "≡", "waving_hand": "✦", "trending_up": "↗",
    "memory": "▣", "monitoring": "◉", "public": "◇",
}


def icon(name: str) -> str:
    return f"<span class='ui-icon' aria-hidden='true'>{ICON_GLYPHS.get(name, '•')}</span>"


def plain_icon(name: str) -> str:
    """Return a text-only icon for Streamlit-native labels that do not parse HTML."""
    return ICON_GLYPHS.get(name, "•")


def render_metric(label: str, value: str, note: str, icon_name: str) -> str:
    return (
        f"<div class='metric-card'><div class='metric-top'><span>{label}</span>"
        f"<span class='metric-icon'>{icon(icon_name)}</span></div>"
        f"<div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>"
    )


def render_stamp(source: str) -> None:
    if source == SOURCE_NEWS:
        st.markdown(f"<span class='stamp stamp-news'>{icon('verified')} Grounded in live news</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='stamp stamp-general'>{icon('auto_awesome')} General knowledge fallback</span>", unsafe_allow_html=True)


def render_sources(sources: list[dict[str, Any]] | None) -> None:
    if not sources:
        return
    with st.expander(f"{plain_icon('link')} View {len(sources)} cited source(s)", expanded=False):
        for source in sources:
            title = html.escape(source.get("title") or "Untitled article")
            url = html.escape(source.get("url") or "#", quote=True)
            publisher = html.escape(source.get("source") or "Unknown publisher")
            published = html.escape(source.get("published") or "Date unavailable")
            number = source.get("n", "—")
            st.markdown(
                f"<div class='source-card'><a href='{url}' target='_blank'>[{number}] {title}</a>"
                f"<div class='source-meta'>{publisher} · {published} · Open article {icon('open_in_new')}</div></div>",
                unsafe_allow_html=True,
            )


def render_retrieval(retrieval: dict[str, Any] | None, expanded: bool = False) -> None:
    if not retrieval:
        return

    raw_count = int(retrieval.get("raw_count", 0))
    relevant_count = int(retrieval.get("relevant_count", 0))
    threshold = float(retrieval.get("threshold", config.RAG_DISTANCE_THRESHOLD))
    hits = retrieval.get("hits", []) or []
    total_chunks = sum(int(hit.get("chunk_count", 1)) for hit in hits)

    st.markdown(
        f"<div class='retrieval-summary'><span><b>{relevant_count}/{raw_count}</b> relevant hits</span>"
        f"<span><b>{total_chunks}</b> supporting chunks</span><span>threshold <b>{threshold:.2f}</b></span></div>",
        unsafe_allow_html=True,
    )

    with st.expander(f"{plain_icon('insights')} Inspect retrieval graph", expanded=expanded):
        if not hits:
            st.markdown("<div class='empty-state'>No indexed chunks were close enough to plot for this question.</div>", unsafe_allow_html=True)
            return

        titles = [str(hit.get("title") or "Untitled")[:42] + ("…" if len(str(hit.get("title") or "")) > 42 else "") for hit in hits]
        distances = [float(hit.get("distance", 0.0)) for hit in hits]
        chunk_counts = [int(hit.get("chunk_count", 1)) for hit in hits]
        colors_by_hit = [colors["green"] if distance <= threshold else colors["muted"] for distance in distances]

        rank_fig = go.Figure(go.Bar(
            x=distances[::-1], y=titles[::-1], orientation="h",
            marker_color=colors_by_hit[::-1],
            text=[f"{distance:.3f}" for distance in distances[::-1]], textposition="outside",
            hovertemplate="%{y}<br>Distance: %{x:.3f}<extra></extra>",
        ))
        rank_fig.update_layout(
            title="Relevance distance · lower is better", height=max(240, 42 * len(hits) + 80),
            margin=dict(l=0, r=40, t=42, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=colors["muted"], family="DM Sans"), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor=colors["line"], zeroline=False, title="distance"),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        )

        chunk_fig = go.Figure(go.Bar(
            x=titles, y=chunk_counts, marker_color=colors["accent"],
            hovertemplate="%{x}<br>Chunks merged: %{y}<extra></extra>",
        ))
        chunk_fig.update_layout(
            title="Supporting chunks per article", height=max(240, 42 * len(hits) + 80),
            margin=dict(l=0, r=10, t=42, b=80), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=colors["muted"], family="DM Sans"), showlegend=False,
            xaxis=dict(showgrid=False, tickangle=-32, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor=colors["line"], zeroline=False, dtick=1),
        )

        left, right = st.columns(2)
        with left:
            st.plotly_chart(rank_fig, use_container_width=True, config={"displayModeBar": False})
        with right:
            st.plotly_chart(chunk_fig, use_container_width=True, config={"displayModeBar": False})


def render_history_turn(turn: dict[str, Any]) -> None:
    role = turn.get("role", "assistant")
    avatar = "user" if role == "user" else "assistant"
    with st.chat_message(role, avatar=avatar):
        if role == "assistant":
            render_stamp(turn.get("source", SOURCE_GEMINI))
            st.markdown(turn.get("content", ""))
            render_retrieval(turn.get("retrieval"))
            if turn.get("source") == SOURCE_NEWS:
                render_sources(turn.get("sources"))
        else:
            st.markdown(turn.get("content", ""))


# -----------------------------------------------------------------------------
# Sidebar controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"<div class='brand'><div class='brand-mark'>{icon('auto_awesome')}</div>"
        f"<div><div class='brand-name'>NewsPilot</div><div class='brand-sub'>Intelligence workspace</div></div></div>",
        unsafe_allow_html=True,
    )

    toggle_left, toggle_right = st.columns([3, 1])
    with toggle_left:
        st.markdown("<div class='side-label'>Workspace</div>", unsafe_allow_html=True)
    with toggle_right:
        st.toggle("Dark mode", key="dark_mode", help="Toggle dark and light mode", label_visibility="collapsed")

    st.caption("Live retrieval, grounded answers, and transparent source inspection in one place.")

    st.markdown("<div class='side-label'>Index operations</div>", unsafe_allow_html=True)
    query = st.text_input("Topic filter", placeholder="e.g. AI regulation", label_visibility="collapsed")
    fulltext = st.checkbox("Extract full article text", value=True, help="Slower, but produces richer chunks for retrieval.")
    if st.button("Refresh news index", type="primary", use_container_width=True):
        with st.spinner("Fetching and indexing the latest wire..."):
            articles = fetch_latest_news(query=query or None, fetch_full_text=fulltext)
            added = store.add_articles(articles)
        st.session_state.last_fetch_count = (len(articles), added)
        st.success(f"{len(articles)} fetched · {added} new chunks")
        st.rerun()

    if st.session_state.last_fetch_count:
        fetched, added = st.session_state.last_fetch_count
        st.caption(f"Last refresh · {fetched} fetched · {added} added")

    st.markdown("<div class='side-label'>Retrieval controls</div>", unsafe_allow_html=True)
    top_k = st.slider("Articles per answer", 3, 12, config.TOP_K_DEFAULT)
    distance_threshold = st.slider(
        "Relevance threshold", 0.05, 1.5, config.RAG_DISTANCE_THRESHOLD, 0.05,
        help="Lower values are stricter. Articles above this distance are not used as grounded context.",
    )
    config.RAG_DISTANCE_THRESHOLD = distance_threshold
    config.ENABLE_GEMINI_FALLBACK = st.checkbox(
        "Allow general-knowledge fallback", value=config.ENABLE_GEMINI_FALLBACK,
        help="When no relevant news is found, let the assistant answer without citations.",
    )

    st.markdown("<div class='side-label'>Session</div>", unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.chat_history) // 2} conversation turn(s) · {store.count()} indexed chunks")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_retrieval = None
        st.rerun()


# -----------------------------------------------------------------------------
# Main workspace
# -----------------------------------------------------------------------------
mode_label = "Live news + fallback" if config.ENABLE_GEMINI_FALLBACK else "Strict live news"
latest = st.session_state.last_retrieval or {}
latest_hits = latest.get("hits", []) if latest else []
latest_relevant = latest.get("relevant_count", 0) if latest else 0

st.markdown(
    f"""
    <div class='hero'>
        <div class='eyebrow'>News intelligence · transparent retrieval · private index</div>
        <h1>Ask the news. See the reasoning.</h1>
        <p class='hero-copy'>A calmer way to explore fast-moving stories. NewsPilot searches your indexed wire, grounds the answer when evidence is strong, and shows exactly which articles and chunks shaped the response.</p>
        <div class='hero-chip-row'>
            <span class='hero-chip'>{icon('database')} {store.count()} chunks indexed</span>
            <span class='hero-chip'>{icon('hub')} {mode_label}</span>
            <span class='hero-chip'>{icon('tune')} top-{top_k} retrieval</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='metric-grid'>"
    + render_metric("Indexed chunks", f"{store.count():,}", "Persistent local news memory", "database")
    + render_metric("Conversation turns", f"{len(st.session_state.chat_history) // 2}", "Questions asked this session", "forum")
    + render_metric("Latest hits", f"{latest_relevant}/{len(latest_hits)}" if latest else "—", "Passed the relevance threshold", "target")
    + render_metric("Mode", "LIVE" if config.ENABLE_GEMINI_FALLBACK else "STRICT", "Grounded context routing", "bolt")
    + "</div>",
    unsafe_allow_html=True,
)

if not st.session_state.chat_history:
    st.markdown(
        f"<div class='welcome-card'><div class='welcome-title'>{icon('waving_hand')} Welcome to your news desk</div>"
        "<p class='welcome-copy'>Start with a focused question, or choose a prompt below. Once you ask, the retrieval panel will show relevance distance and supporting chunks for every grounded answer.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-kicker'>Suggested investigations</div>", unsafe_allow_html=True)
    suggestions = [
        ("trending_up", "What are the biggest stories today?"),
        ("memory", "Summarize recent AI regulation developments."),
        ("monitoring", "What is moving global markets right now?"),
        ("public", "Which technology companies made major announcements?"),
    ]
    suggestion_cols = st.columns(4)
    clicked_suggestion = None
    for col, (suggestion_icon, suggestion) in zip(suggestion_cols, suggestions):
        with col:
            if st.button(f"{suggestion_icon}  {suggestion}", use_container_width=True):
                clicked_suggestion = suggestion
else:
    clicked_suggestion = None

for turn in st.session_state.chat_history:
    render_history_turn(turn)

if st.session_state.chat_history and latest:
    st.markdown("<div class='section-kicker'>Latest retrieval pulse</div>", unsafe_allow_html=True)
    render_retrieval(latest, expanded=False)

typed_question = st.chat_input("Ask a question about the latest news…")
question = clicked_suggestion or typed_question

if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="user"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Searching the wire and composing a grounded answer…"):
            engine = get_engine(store)
            result = engine.ask(question, top_k=top_k)
        render_stamp(result.get("source", SOURCE_GEMINI))
        st.markdown(result.get("answer", "No answer returned."))
        render_retrieval(result.get("retrieval"), expanded=True)
        if result.get("source") == SOURCE_NEWS:
            render_sources(result.get("sources"))

    st.session_state.last_retrieval = result.get("retrieval")
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": result.get("answer", "No answer returned."),
            "source": result.get("source", SOURCE_GEMINI),
            "sources": result.get("sources", []),
            "retrieval": result.get("retrieval"),
        }
    )
    st.rerun()

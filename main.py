import streamlit as st
from utils.pipeline import run_research_pipeline

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .stApp { background: #0e0e10; color: #e8e6e1; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 3rem; max-width: 860px; }

  .hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: 3.2rem;
    line-height: 1.1;
    color: #f0ede6;
    margin-bottom: 0.25rem;
  }
  .hero-sub {
    font-weight: 300;
    font-size: 1rem;
    color: #7a7870;
    margin-bottom: 2.5rem;
    letter-spacing: 0.02em;
  }

  .stTextInput > div > div > input {
    background: #1a1a1e !important;
    border: 1px solid #2e2e35 !important;
    border-radius: 10px !important;
    color: #e8e6e1 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: #c8a96e;
  }
  .stTextInput > div > div > input:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 3px rgba(200,169,110,0.15) !important;
  }
  .stTextInput > label {
    color: #9e9b93 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
  }

  .stButton > button {
    background: #c8a96e !important;
    color: #0e0e10 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 2.2rem !important;
    width: 100%;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    background: #dbbf82 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(200,169,110,0.3) !important;
  }

  .result-card {
    background: #16161a;
    border: 1px solid #252529;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
  }
  .card-label {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c8a96e;
    font-weight: 500;
    margin-bottom: 0.8rem;
    font-family: 'DM Mono', monospace;
  }
  .card-content {
    color: #ccc9c0;
    font-size: 0.95rem;
    line-height: 1.75;
    white-space: pre-wrap;
  }

  .report-card {
    background: #13131a;
    border: 1px solid #2a2a40;
    border-left: 3px solid #c8a96e;
    border-radius: 14px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
  }
  .report-content {
    color: #dbd8d0;
    font-size: 1rem;
    line-height: 1.85;
    white-space: pre-wrap;
  }

  .score-badge {
    display: inline-block;
    background: rgba(200,169,110,0.15);
    color: #c8a96e;
    border: 1px solid rgba(200,169,110,0.3);
    border-radius: 6px;
    padding: 0.15rem 0.7rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.8rem;
  }

  .section-divider { border: none; border-top: 1px solid #1e1e22; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Research Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Search · Scrape · Write · Critique — powered by GPT-4o mini</div>',
    unsafe_allow_html=True,
)

# ── Input ────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.2])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  Impact of LLMs on scientific research in 2025",
    )

with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("Run →", use_container_width=True)


# ── Run pipeline ─────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        with st.spinner("Running research pipeline — this takes ~30–60s..."):
            try:
                result = run_research_pipeline(topic=topic.strip())
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                st.stop()

        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

        # Report
        st.markdown(
            f'<div class="report-card">'
            f'<div class="card-label">📝 Research Report</div>'
            f'<div class="report-content">{result["report"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Critic feedback
        feedback_text = result["feedback"]
        score_line = next(
            (l.strip() for l in feedback_text.splitlines() if l.strip().lower().startswith("score")),
            ""
        )
        st.markdown(
            f'<div class="result-card">'
            f'<div class="card-label">🧐 Critic Feedback</div>'
            f'{"<div class=\'score-badge\'>" + score_line + "</div><br>" if score_line else ""}'
            f'<div class="card-content">{feedback_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Raw data collapsed
        with st.expander("🔍 Raw Search Results"):
            st.markdown(
                f'<div class="card-content" style="font-family:\'DM Mono\',monospace;font-size:0.82rem;">'
                f'{result["search_results"]}</div>',
                unsafe_allow_html=True,
            )

        with st.expander("📄 Scraped Page Content"):
            st.markdown(
                f'<div class="card-content" style="font-family:\'DM Mono\',monospace;font-size:0.82rem;">'
                f'{result["scraped_content"]}</div>',
                unsafe_allow_html=True,
            )
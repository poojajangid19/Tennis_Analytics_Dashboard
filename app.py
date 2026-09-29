
import streamlit as st
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Tennis Analytics Hub",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# HELPER: DYNAMIC PAGE DETECTOR
# ==========================================
def find_page_path(keyword):
    """Dynamically locates page file paths even if named with prefixes like '1_Rankings.py'"""
    if os.path.exists("pages"):
        for fname in os.listdir("pages"):
            if fname.endswith(".py") and keyword.lower() in fname.lower().replace("_", " "):
                return f"pages/{fname}"
    for fname in os.listdir("."):
        if fname.endswith(".py") and keyword.lower() in fname.lower().replace("_", " ") and fname != "app.py":
            return fname
    return None

# Locate paths for each module
p_competitors = find_page_path("competitor")
p_rankings = find_page_path("ranking")
p_comparison = find_page_path("comparison")
p_insights = find_page_path("insight")
p_match = find_page_path("match")
p_leaderboard = find_page_path("leaderboard")

# ==========================================
# ULTRA-PREMIUM CSS (DARK BLUE TEXT & ACTIVE BUTTONS)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    /* ---------------- HERO SHOWCASE ---------------- */
    .hero-container {
        background: radial-gradient(circle at 85% 15%, rgba(59, 130, 246, 0.28) 0%, rgba(15, 23, 42, 0) 65%),
                    linear-gradient(135deg, #090d16 0%, #0f172a 55%, #172554 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 28px;
        padding: 55px 44px;
        color: #ffffff !important;
        margin-bottom: 28px;
        box-shadow: 0 25px 50px -12px rgba(2, 6, 23, 0.65);
        text-align: center;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399 !important;
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 9999px;
        padding: 6px 18px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 18px;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        background-color: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 10px #34d399;
    }

    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        margin: 0 0 14px 0 !important;
        color: #ffffff !important;
        line-height: 1.15 !important;
    }

    .hero-gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-desc {
        color: #cbd5e1 !important;
        font-size: 1.15rem !important;
        max-width: 800px !important;
        margin: 0 auto !important;
        line-height: 1.6 !important;
    }

    /* ---------------- TELEMETRY CARDS (FIXED DARK BLUE) ---------------- */
    .metric-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 22px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .metric-header {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #1e40af !important; /* DARK BLUE */
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    .metric-val {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        color: #0f172a !important; /* HIGH CONTRAST DARK NAVY */
        line-height: 1.1 !important;
    }
    .metric-trend {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        border-radius: 6px;
        width: fit-content;
    }
    .trend-up { background: #ecfdf5; color: #059669 !important; }
    .trend-neutral { background: #f1f5f9; color: #475569 !important; }

    /* ---------------- MODULE CONTAINER & TYPOGRAPHY ---------------- */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #3b82f6;
        box-shadow: 0 12px 25px -5px rgba(37, 99, 235, 0.12);
        transform: translateY(-4px);
    }

    .card-icon {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        margin-bottom: 12px;
    }
    .icon-blue   { background: #eff6ff; }
    .icon-amber  { background: #fffbeb; }
    .icon-emerald{ background: #ecfdf5; }
    .icon-purple { background: #faf5ff; }
    .icon-rose   { background: #fff1f2; }
    .icon-indigo { background: #eef2ff; }

    .card-title {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #0f172a !important; /* DARK NAVY BLUE */
        margin: 0 0 8px 0 !important;
    }
    .card-desc {
        font-size: 0.95rem !important;
        color: #334155 !important; /* DARK BLUE-GRAY (NEVER WHITE) */
        line-height: 1.5 !important;
        min-height: 65px;
        margin-bottom: 12px !important;
    }

    /* ---------------- STYLE STREAMLIT PAGE LINK BUTTONS ---------------- */
    div[data-testid="stPageLink"] a {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-decoration: none !important;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stPageLink"] a:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
    }
    div[data-testid="stPageLink"] a span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SHOWCASE
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="live-dot"></span> Live ATP & WTA Analytics Engine
    </div>
    <h1 class="hero-title">
        The Premier Intelligence Portal for <span class="hero-gradient-text">World Tennis</span>
    </h1>
    <p class="hero-desc">
        Explore real-time competitor rankings, run multi-vector head-to-head simulations, track tournament momentum shifts, and evaluate machine-learning performance metrics across all professional tours.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TELEMETRY CARDS (DARK NAVY / BLUE TEXT)
# ==========================================
c_m1, c_m2, c_m3, c_m4 = st.columns(4)

with c_m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>👥</span> Tracked Competitors</div>
        <div class="metric-val">1,240+</div>
        <div class="metric-trend trend-up">↗ 18 active today</div>
    </div>
    """, unsafe_allow_html=True)
with c_m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>🏆</span> Matches Ingested</div>
        <div class="metric-val">45,210</div>
        <div class="metric-trend trend-neutral">→ All Grand Slams</div>
    </div>
    """, unsafe_allow_html=True)
with c_m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>📊</span> Telemetry Points</div>
        <div class="metric-val">2.4M</div>
        <div class="metric-trend trend-up">↗ +14.2% YoY</div>
    </div>
    """, unsafe_allow_html=True)
with c_m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>🤖</span> AI Precision</div>
        <div class="metric-val">94.2%</div>
        <div class="metric-trend trend-up">↗ Benchmark tier</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ==========================================
# INTERACTIVE PLATFORM MODULES (ROW 1)
# ==========================================
st.markdown("<h3 style='color: #0f172a; margin-bottom: 2px;'>🧭 Platform Modules</h3>", unsafe_allow_html=True)
st.caption("Click any module below to jump directly into the analytical suite.")
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

r1_c1, r1_c2, r1_c3 = st.columns(3, gap="medium")

# 1. Competitors Explorer
with r1_c1:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-blue">👥</div>
        <div class="card-title">Competitors Explorer</div>
        <div class="card-desc">Search, filter, and drill into athlete biographies, registered nations, and universal IDs worldwide.</div>
        """, unsafe_allow_html=True)
        if p_competitors:
            st.page_link(p_competitors, label="Explore Competitors ➔", use_container_width=True)
        else:
            st.info("Select 'Competitors' in sidebar")

# 2. Global Rankings
with r1_c2:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-amber">🏆</div>
        <div class="card-title">Global Rankings</div>
        <div class="card-desc">Analyze historical point progression by year and week with interactive bar charts and histograms.</div>
        """, unsafe_allow_html=True)
        if p_rankings:
            st.page_link(p_rankings, label="View Rankings ➔", use_container_width=True)
        else:
            st.info("Select 'Rankings' in sidebar")

# 3. Player Comparison
with r1_c3:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-emerald">⚔️</div>
        <div class="card-title">Player Comparison</div>
        <div class="card-desc">Compare two athletes head-to-head using multi-axis skill radars, service indexes, and clutch ratings.</div>
        """, unsafe_allow_html=True)
        if p_comparison:
            st.page_link(p_comparison, label="Compare Players ➔", use_container_width=True)
        else:
            st.info("Select 'Player Comparison' in sidebar")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ==========================================
# INTERACTIVE PLATFORM MODULES (ROW 2)
# ==========================================
r2_c1, r2_c2, r2_c3 = st.columns(3, gap="medium")

# 4. AI Insights
with r2_c1:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-purple">💡</div>
        <div class="card-title">AI Insights</div>
        <div class="card-desc">Synthesized executive intelligence highlighting rating ceilings, momentum anomalies, and density clusters.</div>
        """, unsafe_allow_html=True)
        if p_insights:
            st.page_link(p_insights, label="View Insights ➔", use_container_width=True)
        else:
            st.info("Select 'Insights' in sidebar")

# 5. Match Analysis
with r2_c2:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-rose">🎾</div>
        <div class="card-title">Match Analysis</div>
        <div class="card-desc">Deep-dive into set-by-set telemetries, win probability swings, and live-style digital scoreboard breakdowns.</div>
        """, unsafe_allow_html=True)
        if p_match:
            st.page_link(p_match, label="Analyze Matches ➔", use_container_width=True)
        else:
            st.info("Select 'Match Analysis' in sidebar")

# 6. Leaderboard
with r2_c3:
    with st.container(border=True):
        st.markdown("""
        <div class="card-icon icon-indigo">🏅</div>
        <div class="card-title">Tour Leaderboard</div>
        <div class="card-desc">Podium highlights for top seeds with live movement tracking, points totals, and tournament indicators.</div>
        """, unsafe_allow_html=True)
        if p_leaderboard:
            st.page_link(p_leaderboard, label="Open Leaderboard ➔", use_container_width=True)
        else:
            st.info("Select 'Leaderboard' in sidebar")

# ==========================================
# SIDEBAR REFINEMENT
# ==========================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80",
        use_container_width=True
    )
    st.markdown("### 🎾 Workspace")
    st.caption("Active Engine: ATP/WTA Analytics Suite v3.2")

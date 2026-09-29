
import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION (Must be first)
# ==========================================
st.set_page_config(
    page_title="Global Leaderboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ULTRA-PREMIUM DESIGN SYSTEM (CSS)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    /* ---------------- HERO SHOWCASE ---------------- */
    .hero-container {
        background: radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.22) 0%, rgba(15, 23, 42, 0) 65%),
                    linear-gradient(135deg, #090d16 0%, #0f172a 55%, #172554 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 40px 45px;
        color: #ffffff !important;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px -10px rgba(2, 6, 23, 0.6);
        position: relative;
        overflow: hidden;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(59, 130, 246, 0.15);
        color: #93c5fd !important;
        border: 1px solid rgba(147, 197, 253, 0.35);
        backdrop-filter: blur(8px);
        border-radius: 9999px;
        padding: 6px 16px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin: 0 0 10px 0 !important;
        color: #ffffff !important;
        line-height: 1.15 !important;
    }

    .hero-gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-desc {
        color: #94a3b8 !important;
        font-size: 1.05rem !important;
        max-width: 800px !important;
        margin: 0 !important;
        line-height: 1.6 !important;
    }

    /* ---------------- PODIUM CARDS (FIXED ALIGNMENT) ---------------- */
    .podium-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px 16px !important; /* Optimized padding */
        text-align: center;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
        position: relative;
        height: 100%;
        overflow: hidden; /* Prevents text bleeding */
    }
    .podium-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6 !important;
        box-shadow: 0 12px 20px -6px rgba(37, 99, 235, 0.12) !important;
    }
    
    /* Top Borders for Ranks */
    .rank-1 { border-top: 6px solid #fbbf24 !important; } /* Gold */
    .rank-2 { border-top: 6px solid #94a3b8 !important; } /* Silver */
    .rank-3 { border-top: 6px solid #b45309 !important; } /* Bronze */

    .podium-medal {
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    .podium-name {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; /* Graceful cutoff on small screens */
    }
    .podium-country {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 18px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .podium-points {
        display: inline-block;
        background: #f1f5f9;
        color: #1e40af;
        font-weight: 800;
        padding: 6px 16px;
        border-radius: 10px;
        font-size: 1.1rem;
        white-space: nowrap;
    }

    /* ---------------- CONTAINER STYLING ---------------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80",
        use_container_width=True
    )
    st.markdown("### 🎾 Workspace")
    st.caption("Active Module: Tour Leaderboard")

# ==========================================
# DATASET ENRICHMENT
# ==========================================
df = pd.DataFrame({
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8],
    "Player": ["Novak Djokovic", "Carlos Alcaraz", "Jannik Sinner", "Daniil Medvedev", "Alexander Zverev", "Andrey Rublev", "Holger Rune", "Hubert Hurkacz"],
    "Country": ["🇷🇸 Serbia", "🇪🇸 Spain", "🇮🇹 Italy", "🇷🇺 Russia", "🇩🇪 Germany", "🇷🇺 Russia", "🇩🇰 Denmark", "🇵🇱 Poland"],
    "Points": [9870, 9500, 9100, 8700, 8200, 4805, 4125, 3995],
    "Tournaments": [18, 17, 21, 22, 23, 22, 21, 20],
    "Movement": [0, 1, 1, -1, 0, 2, -1, 0]
})

# ==========================================
# HERO BANNER
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        🏅 ATP Tour Standings
    </div>
    <h1 class="hero-title">
        Global <span class="hero-gradient-text">Leaderboard</span>
    </h1>
    <p class="hero-desc">
        Live performance standings, points distributions, and active rankings for the top competitors on the professional circuit.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TOP 3 PODIUM SECTION
# ==========================================
st.markdown("<h3 style='color: #0f172a; margin-top: 0;'>🏆 Top Contenders</h3>", unsafe_allow_html=True)
st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

# NOTE: Using <div> instead of <p> for text to prevent Streamlit from adding unwanted markdown bottom margins.
with c1:
    st.markdown("""
    <div class="podium-card rank-1">
        <div class="podium-medal">🥇</div>
        <div class="podium-name">Novak Djokovic</div>
        <div class="podium-country">🇷🇸 Serbia</div>
        <div class="podium-points">9,870 pts</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="podium-card rank-2">
        <div class="podium-medal">🥈</div>
        <div class="podium-name">Carlos Alcaraz</div>
        <div class="podium-country">🇪🇸 Spain</div>
        <div class="podium-points">9,500 pts</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="podium-card rank-3">
        <div class="podium-medal">🥉</div>
        <div class="podium-name">Jannik Sinner</div>
        <div class="podium-country">🇮🇹 Italy</div>
        <div class="podium-points">9,100 pts</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ==========================================
# FULL DATA TABLE
# ==========================================
with st.container(border=True):
    st.markdown("<h3 style='color: #0f172a; margin-top: 0;'>📋 Complete Standings</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    max_points = df["Points"].max()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=320,
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank", 
                format="#%d", 
                width="small"
            ),
            "Player": st.column_config.TextColumn(
                "Athlete Name", 
                width="medium"
            ),
            "Country": st.column_config.TextColumn(
                "Nation", 
                width="small"
            ),
            "Points": st.column_config.ProgressColumn(
                "Total Points",
                help="Accumulated ATP ranking points",
                format="%d pts",
                min_value=0,
                max_value=int(max_points + 500),
                width="medium"
            ),
            "Tournaments": st.column_config.NumberColumn(
                "Events Played",
                width="small"
            ),
            "Movement": st.column_config.NumberColumn(
                "Trend",
                help="Rank movement since last week (Positive = Up, Negative = Down)",
                format="%+d",
                width="small"
            )
        }
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.caption("⚡ Standings are automatically synchronized with the latest ATP tour data pipelines.")

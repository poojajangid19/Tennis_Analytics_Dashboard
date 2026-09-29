

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Tennis Analytics Dashboard",
    page_icon="🎾",
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
        padding-bottom: 3.5rem;
        max-width: 1400px;
    }

    /* ---------------- HERO SHOWCASE ---------------- */
    .hero-container {
        background: radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.22) 0%, rgba(15, 23, 42, 0) 65%),
                    linear-gradient(135deg, #090d16 0%, #0f172a 55%, #172554 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 40px 35px;
        color: #ffffff !important;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px -10px rgba(2, 6, 23, 0.6);
        position: relative;
        overflow: hidden;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.14);
        color: #34d399 !important;
        border: 1px solid rgba(52, 211, 153, 0.35);
        backdrop-filter: blur(8px);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }

    .live-dot {
        width: 6px;
        height: 6px;
        background-color: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 8px #34d399;
    }

    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin: 0 0 8px 0 !important;
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
        font-size: 1rem !important;
        max-width: 760px !important;
        margin: 0 !important;
        line-height: 1.5 !important;
    }

    /* ---------------- TELEMETRY CARDS (FIXED ALIGNMENT) ---------------- */
    .metric-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 16px !important; /* Reduced padding to prevent squishing */
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 8px;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #3b82f6 !important;
        box-shadow: 0 8px 16px -4px rgba(37, 99, 235, 0.12) !important;
    }
    .metric-header {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #1e40af !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important; /* Scaled down slightly */
        white-space: nowrap; /* Prevents awkward text wrapping */
    }
    .metric-val {
        font-size: 1.8rem !important; /* Scaled down to fit 4 columns */
        font-weight: 800 !important;
        color: #0f172a !important;
        line-height: 1 !important;
        margin: 4px 0;
    }
    .metric-trend {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 8px;
        border-radius: 6px;
        width: fit-content;
        white-space: nowrap;
    }
    .trend-up { background: #ecfdf5; color: #059669 !important; }
    .trend-neutral { background: #f1f5f9; color: #475569 !important; }

    /* ---------------- CHART CONTAINER STYLING ---------------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
        padding: 1rem !important; /* Uniform internal padding */
    }
    
    /* Subheader Alignment Fixes */
    h3 {
        padding-top: 0 !important;
        margin-top: 0 !important;
        font-size: 1.25rem !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATASETS 
# ==========================================
@st.cache_data
def get_dashboard_data():
    country_df = pd.DataFrame({
        "Country": ["Serbia", "Spain", "Italy", "USA", "Russia", "Germany", "France", "Australia"],
        "Players": [18, 16, 14, 12, 10, 8, 7, 5],
        "Continent": ["Europe", "Europe", "Europe", "Americas", "Europe", "Europe", "Europe", "Oceania"]
    })

    player_df = pd.DataFrame({
        "Rank": [1, 2, 3, 4, 5, 6, 7, 8],
        "Player": ["Novak Djokovic", "Carlos Alcaraz", "Jannik Sinner", "Daniil Medvedev", "Alexander Zverev", "Andrey Rublev", "Holger Rune", "Hubert Hurkacz"],
        "Country": ["Serbia", "Spain", "Italy", "Russia", "Germany", "Russia", "Denmark", "Poland"],
        "Points": [9870, 9500, 9100, 8700, 8200, 4805, 4125, 3995],
        "Tournaments": [18, 17, 21, 22, 23, 22, 21, 20],
        "Win_Rate": [88.5, 84.2, 86.1, 79.8, 77.4, 73.1, 69.5, 71.0]
    })
    return country_df, player_df

country_df, player_df = get_dashboard_data()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80", use_container_width=True)
    st.header("⚙️ Workspace Controls")
    
    selected_continents = st.multiselect(
        "Filter by Region",
        options=country_df["Continent"].unique(),
        default=country_df["Continent"].unique()
    )
    
    top_n = st.slider("Leaderboard Display Limit", min_value=3, max_value=len(player_df), value=6)
    
    min_points = st.sidebar.number_input(
        "Points Cutoff Threshold",
        min_value=0,
        max_value=10000,
        value=3500,
        step=500
    )
    st.caption("Active Session: ATP/WTA Season 2026")

# Filter logic
filtered_countries = country_df[country_df["Continent"].isin(selected_continents)]
filtered_players = player_df[
    (player_df["Points"] >= min_points)
].sort_values("Points", ascending=False).head(top_n)

# ==========================================
# HERO SHOWCASE
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="live-dot"></span> ATP Tour Insights • Season 2026
    </div>
    <h1 class="hero-title">
        Tennis Analytics <span class="hero-gradient-text">Command Center</span>
    </h1>
    <p class="hero-desc">
        Live performance benchmarks, global competitor distributions, and points leadership tracking across professional circuits.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI METRICS SECTION 
# ==========================================
k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>👤</span> Active Players</div>
        <div class="metric-val">150</div>
        <div class="metric-trend trend-up">↗ +12 on tour</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>🌍</span> Nations Represented</div>
        <div class="metric-val">{country_df['Country'].nunique()}</div>
        <div class="metric-trend trend-up">↗ +3 this season</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-header"><span>🏆</span> Tournaments Tracked</div>
        <div class="metric-val">120</div>
        <div class="metric-trend trend-neutral">→ 4 Grand Slams</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>⭐</span> Active ATP Points</div>
        <div class="metric-val">{player_df['Points'].sum():,}</div>
        <div class="metric-trend trend-up">↗ +14.2% YoY</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==========================================
# VISUAL ANALYTICS TABS
# ==========================================
tab_visuals, tab_roster = st.tabs(["📊 Performance Intelligence", "📋 Detailed Roster Directory"])

with tab_visuals:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")

    # Chart 1: Players by Country
    with left:
        with st.container(border=True):
            st.subheader("🌐 Global Representation")
            st.caption("Distribution of top athletes by registered nation")

            fig1 = px.bar(
                filtered_countries.sort_values("Players", ascending=False),
                x="Country",
                y="Players",
                color="Players",
                color_continuous_scale=["#93c5fd", "#3b82f6", "#1e3a8a"],
                text="Players"
            )
            fig1.update_traces(
                marker_line_width=0,
                textposition="outside",
                cliponaxis=False
            )
            fig1.update_layout(
                height=350,
                coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(title="", showgrid=False),
                yaxis=dict(title="Player Count", showgrid=True, gridcolor="#f1f5f9"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Top Players by Points
    with right:
        with st.container(border=True):
            st.subheader("⭐ Elite Standings")
            st.caption("Ranking point progression for top contenders")

            fig2 = px.bar(
                filtered_players.sort_values("Points", ascending=True),
                x="Points",
                y="Player",
                orientation="h",
                color="Points",
                color_continuous_scale=["#38bdf8", "#2563eb", "#0f172a"],
                text="Points"
            )
            fig2.update_traces(
                marker_line_width=0,
                texttemplate="%{x:,} pts",
                textposition="outside",
                cliponaxis=False
            )
            fig2.update_layout(
                height=350,
                coloraxis_showscale=False,
                margin=dict(l=0, r=40, t=20, b=0),
                xaxis=dict(title="", showgrid=True, gridcolor="#f1f5f9"),
                yaxis=dict(title="", showgrid=False),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Bottom Full-Width Chart: Multi-Factor Scatter
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("🎯 Efficiency Matrix: Points vs. Win Rate")
        st.caption("Evaluating win efficiency vs accumulated ranking capital")

        fig3 = px.scatter(
            player_df,
            x="Win_Rate",
            y="Points",
            size="Tournaments",
            color="Country",
            hover_name="Player",
            text="Player",
            size_max=22,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig3.update_traces(textposition="top center")
        fig3.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(title="Match Win Rate (%)", showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(title="ATP Points", showgrid=True, gridcolor="#f1f5f9"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig3, use_container_width=True)

with tab_roster:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("📋 Leaderboard Breakdown")
        
        st.dataframe(
            filtered_players,
            use_container_width=True,
            hide_index=True,
            height=380,
            column_order=["Rank", "Player", "Country", "Points", "Win_Rate", "Tournaments"],
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", format="#%d", width="small"),
                "Player": st.column_config.TextColumn("Athlete Name", width="medium"),
                "Country": st.column_config.TextColumn("Country", width="medium"),
                "Points": st.column_config.NumberColumn("ATP Points", format="%d pts", width="medium"),
                "Win_Rate": st.column_config.ProgressColumn(
                    "Win Rate (%)",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                    width="medium"
                ),
                "Tournaments": st.column_config.NumberColumn("Events Played", format="%d", width="small")
            }
        )

# ==========================================
# FOOTER
# ==========================================
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
st.caption(f"⚡ Live Telemetry: Displaying **{len(filtered_players)}** top seeded athletes across **{len(filtered_countries)}** active regions.")



import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION (Must be first)
# ==========================================
st.set_page_config(
    page_title="Rankings Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PREMIUM CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }

    /* Hero Banner */
    .hero-banner {
        background: radial-gradient(circle at top right, #1e3a8a 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0 0 8px 0;
        color: #ffffff;
    }
    .hero-desc {
        color: #94a3b8;
        font-size: 1.05rem;
        margin: 0;
        max-width: 720px;
    }

    /* Styled Metric Cards */
    div[data-testid="stMetric"] {
        background-color: var(--background-secondary);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA (Cached for performance)
# ==========================================
@st.cache_data
def load_data():
    rankings = pd.read_csv("data/competitor_rankings.csv")
    competitors = pd.read_csv("data/competitors.csv")

    # Clean IDs
    rankings["competitor_id"] = rankings["competitor_id"].astype(str).str.replace(
        "sr:competitor:", "", regex=False
    )
    competitors["competitor_id"] = competitors["competitor_id"].astype(str).str.replace(
        "sr:competitor:", "", regex=False
    )

    # Merge player names and countries
    df = rankings.merge(
        competitors[["competitor_id", "name", "country"]],
        on="competitor_id",
        how="left"
    )
    return df

df = load_data()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # Year Filter
    years = sorted(df["year"].dropna().unique(), reverse=True)
    selected_year = st.selectbox("📅 Select Year", years)

    # Week Filter
    weeks = sorted(df[df["year"] == selected_year]["week"].dropna().unique(), reverse=True)
    selected_week = st.selectbox("📆 Select Week", weeks)

    st.divider()
    
    search_player = st.text_input("🔍 Search Player", placeholder="e.g. Novak Djokovic")

# Apply filters
filtered_df = df[(df["year"] == selected_year) & (df["week"] == selected_week)]

if search_player:
    filtered_df = filtered_df[
        filtered_df["name"].astype(str).str.contains(search_player, case=False, na=False)
    ]

if filtered_df.empty:
    st.warning("⚠️ No data found for the selected filters. Please adjust your search criteria.")
    st.stop()

# ==========================================
# HERO HEADER
# ==========================================
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🏆 Player Rankings Dashboard</h1>
    <p class="hero-desc">Explore live player rankings, tracking points, and historical performance metrics across different regions and competitions.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI METRICS
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👤 Active Players", f"{len(filtered_df):,}")
with col2:
    st.metric("🏆 Best Rank", int(filtered_df["rank"].min()))
with col3:
    st.metric("⭐ Highest Points", f"{int(filtered_df['points'].max()):,}")
with col4:
    st.metric("🌍 Countries Represented", filtered_df["country"].nunique())

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# VISUAL ANALYTICS TABS
# ==========================================
tab_visuals, tab_roster = st.tabs(["📊 Performance Charts", "📋 Player Directory"])

with tab_visuals:
    col_chart1, col_chart2 = st.columns((3, 2), gap="large")
    
    # Chart 1: Top 10 Bar Chart
    with col_chart1:
        with st.container(border=True):
            st.subheader("📈 Top 10 Ranked Players")
            st.caption("Highest scoring athletes by total ranking points")
            top10 = filtered_df.sort_values("rank").head(10)
            
            fig = px.bar(
                top10,
                x="points",
                y="name",
                orientation="h",
                color="points",
                color_continuous_scale=["#38bdf8", "#2563eb", "#1e40af"],
                text="points"
            )
            
            fig.update_traces(
                texttemplate="%{text:,} pts",
                textposition="outside",
                marker_line_width=0,
                cliponaxis=False
            )
            fig.update_layout(
                height=420,
                yaxis=dict(categoryorder="total ascending", title=""),
                xaxis=dict(title="", showgrid=True, gridcolor="rgba(128, 128, 128, 0.15)"),
                showlegend=False,
                coloraxis_showscale=False,
                margin=dict(l=0, r=40, t=20, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    # Chart 2: Distribution Histogram
    with col_chart2:
        with st.container(border=True):
            st.subheader("📊 Rank Distribution")
            st.caption("Volume of players spread across ranking tiers")
            fig2 = px.histogram(
                filtered_df,
                x="rank",
                nbins=25,
                color_discrete_sequence=["#3b82f6"],
                opacity=0.85
            )
            fig2.update_traces(marker_line_width=0.5, marker_line_color="white")
            fig2.update_layout(
                height=420,
                xaxis=dict(title="Rank Position", showgrid=False),
                yaxis=dict(title="Number of Players", showgrid=True, gridcolor="rgba(128, 128, 128, 0.15)"),
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

with tab_roster:
    st.subheader("🥇 Detailed Rankings Table")
    
    # Safely configure progress bar max
    max_comps = int(filtered_df["competitions_played"].max()) if not filtered_df["competitions_played"].isnull().all() else 100
    
    st.dataframe(
        filtered_df.sort_values("rank")[
            ["rank", "name", "country", "points", "movement", "competitions_played"]
        ],
        column_config={
            "rank": st.column_config.NumberColumn("Rank", format="%d 🏅", width="small"),
            "name": st.column_config.TextColumn("Player Name", width="medium"),
            "country": st.column_config.TextColumn("Country", width="medium"),
            "points": st.column_config.NumberColumn("Points", format="%d pts", width="small"),
            "movement": st.column_config.NumberColumn("Movement", help="Change in rank", width="small"),
            "competitions_played": st.column_config.ProgressColumn(
                "Competitions",
                help="Number of competitions played",
                format="%d",
                min_value=0,
                max_value=max_comps,
                width="medium"
            )
        },
        use_container_width=True,
        hide_index=True,
        height=550
    )

# ==========================================
# FOOTER / SUMMARY
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.caption(f"⚡ Showing records for **{len(filtered_df):,}** active players across **{filtered_df['country'].nunique()}** countries.")


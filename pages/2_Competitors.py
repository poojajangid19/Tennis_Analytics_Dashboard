import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION (Must be first)
# ==========================================
st.set_page_config(
    page_title="Competitors Explorer",
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
        margin-bottom: 24px;
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

    /* ---------------- TELEMETRY CARDS (FIXED ALIGNMENT & COLOR) ---------------- */
    .metric-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 16px 14px !important; /* Tighter padding so text fits */
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 8px;
        height: 100%;
        min-height: 110px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        overflow: hidden; /* Prevents anything from spilling out */
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #3b82f6 !important;
        box-shadow: 0 10px 20px -6px rgba(37, 99, 235, 0.12) !important;
    }
    .metric-header {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #1e40af !important; /* Dark Navy Blue */
        font-weight: 700 !important;
        font-size: 0.85rem !important; /* Scaled down */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; /* Adds '...' if text is too long */
    }
    .metric-val {
        font-size: 1.8rem !important; /* Scaled down */
        font-weight: 800 !important;
        color: #0f172a !important; /* High Contrast Black/Navy */
        line-height: 1.1 !important;
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
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .trend-up { background: #ecfdf5; color: #059669 !important; }
    .trend-neutral { background: #f1f5f9; color: #475569 !important; }

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
# LOAD DATA (Cached for Performance)
# ==========================================
@st.cache_data
def load_data():
    # Ensure the 'data/' folder exists and contains 'competitors.csv'
    try:
        df = pd.read_csv("data/competitors.csv")
        df["competitor_id"] = (
            df["competitor_id"]
            .astype(str)
            .str.replace("sr:competitor:", "", regex=False)
        )
        return df
    except FileNotFoundError:
        # Fallback empty dataframe for preview purposes if file is missing
        return pd.DataFrame(columns=["competitor_id", "name", "country", "country_code", "abbreviation"])

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80",
        use_container_width=True
    )
    st.markdown("### 🎾 Workspace")
    st.caption("Active Module: Competitors Explorer")

# ==========================================
# HERO BANNER
# ==========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        🔍 Global Directory Search
    </div>
    <h1 class="hero-title">
        Competitors <span class="hero-gradient-text">Explorer</span>
    </h1>
    <p class="hero-desc">
        Search, filter, and analyze tennis competitors worldwide with real-time dynamic filtering. Access universal IDs, country representations, and abbreviations instantly.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CONTROL PANEL (Filters & Search)
# ==========================================
with st.container(border=True):
    st.markdown("<h4 style='color: #0f172a; margin-top: 0;'>🔍 Query Parameters</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        search = st.text_input(
            "Quick Search", 
            placeholder="Search by ID, Name, Country Code, or Abbreviation...",
            label_visibility="collapsed"
        )
        
    with col2:
        countries = ["All Countries"] + sorted(df["country"].dropna().unique()) if not df.empty else ["All Countries"]
        selected_country = st.selectbox(
            "Filter by Country",
            countries,
            label_visibility="collapsed"
        )

# ==========================================
# APPLY FILTERS
# ==========================================
filtered_df = df.copy()

if not filtered_df.empty:
    if search:
        # Creating a boolean mask for cross-column searching
        mask = (
            filtered_df["competitor_id"].astype(str).str.contains(search, case=False, na=False) |
            filtered_df["name"].astype(str).str.contains(search, case=False, na=False) |
            filtered_df["country_code"].astype(str).str.contains(search, case=False, na=False) |
            filtered_df["abbreviation"].astype(str).str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if selected_country != "All Countries":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

# Handle empty state
if filtered_df.empty:
    st.warning("⚠️ No competitors found matching your search criteria. Try adjusting your filters.")
    st.stop()

# ==========================================
# KPI METRICS
# ==========================================
k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>👤</span> Competitors</div>
        <div class="metric-val">{len(filtered_df):,}</div>
        <div class="metric-trend trend-up">✓ Query Match</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>🌍</span> Nations</div>
        <div class="metric-val">{filtered_df['country'].nunique()}</div>
        <div class="metric-trend trend-neutral">Filtered Scope</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>🔤</span> Country Codes</div>
        <div class="metric-val">{filtered_df['country_code'].nunique()}</div>
        <div class="metric-trend trend-neutral">Filtered Scope</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header"><span>📊</span> Total Records</div>
        <div class="metric-val">{len(filtered_df):,}</div>
        <div class="metric-trend trend-up">✓ Database Sync</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# ==========================================
# DATA GRID DISPLAY
# ==========================================
with st.container(border=True):
    st.markdown("<h3 style='color: #0f172a; margin-top: 0;'>📋 Competitors Directory</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=450,
        column_order=["competitor_id", "name", "country", "country_code", "abbreviation"],
        column_config={
            "competitor_id": st.column_config.TextColumn(
                "Competitor ID", 
                width="medium"
            ),
            "name": st.column_config.TextColumn(
                "Player Name", 
                width="large"
            ),
            "country": st.column_config.TextColumn(
                "Country", 
                width="medium"
            ),
            "country_code": st.column_config.TextColumn(
                "Country Code", 
                width="small"
            ),
            "abbreviation": st.column_config.TextColumn(
                "Abbreviation", 
                width="small"
            )
        }
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
st.caption(f"⚡ Successfully retrieved and rendered **{len(filtered_df):,}** competitor records based on the active query parameters.")
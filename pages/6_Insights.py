
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Insights & Highlights",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ULTRA-PREMIUM CUSTOM CSS
# ==========================================
st.markdown("""
<style>
    /* Premium Font Integration */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Container Adjustments */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Animated Live Dot */
    @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.2); box-shadow: 0 0 10px rgba(16, 185, 129, 0.8); }
        100% { opacity: 1; transform: scale(1); }
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }
    .dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        animation: blink 2s infinite ease-in-out;
    }

    /* Hero Header Banner */
    .insights-header {
        background: radial-gradient(circle at 100% 0%, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 35px 40px;
        color: white;
        margin-bottom: 35px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
    }
    .header-text h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
    }
    .header-text p {
        margin: 8px 0 0 0;
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 600px;
    }
    
    /* Custom Insight Cards */
    .insight-card {
        background: linear-gradient(145deg, var(--background-secondary), var(--background-primary));
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 20px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .insight-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: rgba(128, 128, 128, 0.3);
    }
    
    /* Card Internals */
    .card-top {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
    }
    .icon-box {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
    }
    .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }
    .card-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .card-trend {
        margin-top: 18px;
        padding-top: 16px;
        border-top: 1px dashed rgba(128, 128, 128, 0.2);
        font-size: 0.95rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Unique Color Themes with Glow Effects */
    .theme-success .icon-box { background: linear-gradient(135deg, #10b981, #059669); color: white; }
    .theme-success .card-trend { color: #10b981; }
    
    .theme-info .icon-box { background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; }
    .theme-info .card-trend { color: #3b82f6; }
    
    .theme-warning .icon-box { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
    .theme-warning .card-trend { color: #f59e0b; }
    
    .theme-error .icon-box { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
    .theme-error .card-trend { color: #ef4444; }

    /* Light/Dark mode auto text adaptation */
    @media (prefers-color-scheme: dark) {
        .card-value { color: #ffffff; }
        .card-title { color: #94a3b8; }
    }
    @media (prefers-color-scheme: light) {
        .card-value { color: #0f172a; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown("""
<div class="insights-header">
    <span class="live-badge"><div class="dot"></div> LIVE AI TELEMETRY</span>
    <div style="display: flex; justify-content: space-between; align-items: flex-end;">
        <div class="header-text">
            <h1>💡 Intelligence Briefing</h1>
            <p>Real-time highlights, algorithmic takeaways, and performance anomalies detected across the current ATP season.</p>
        </div>
        <div style="font-size: 4rem; opacity: 0.4; filter: blur(1px); transform: rotate(15deg);">🎾</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INSIGHT CARDS (Grid Layout)
# ==========================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="insight-card theme-success">
        <div>
            <div class="card-top">
                <div class="icon-box">🏆</div>
                <p class="card-title">World Number 1</p>
            </div>
            <h2 class="card-value">Novak Djokovic</h2>
        </div>
        <div class="card-trend">
            <span style="font-size: 1.2rem;">↗</span> Retained #1 for 400+ weeks
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="insight-card theme-info">
        <div>
            <div class="card-top">
                <div class="icon-box">🌍</div>
                <p class="card-title">Highest Density</p>
            </div>
            <h2 class="card-value">Serbia</h2>
        </div>
        <div class="card-trend">
            <span style="font-size: 1.2rem;">→</span> 18 active athletes in Top 100
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="insight-card theme-warning">
        <div>
            <div class="card-top">
                <div class="icon-box">⚡</div>
                <p class="card-title">Momentum Shift</p>
            </div>
            <h2 class="card-value">Carlos Alcaraz</h2>
        </div>
        <div class="card-trend">
            <span style="font-size: 1.2rem;">↗</span> +2 ranks in last 30 days
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="insight-card theme-error">
        <div>
            <div class="card-top">
                <div class="icon-box">⭐</div>
                <p class="card-title">Ceiling Metric</p>
            </div>
            <h2 class="card-value">9,870 <span style="font-size: 1.1rem; color: #64748b; font-weight: 600;">pts</span></h2>
        </div>
        <div class="card-trend">
            <span style="font-size: 1.2rem;">↗</span> +450 pts from last major
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TREND VISUALIZATION & AI SUMMARY
# ==========================================
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

col_chart, col_summary = st.columns([2.5, 1.5], gap="large")

with col_chart:
    with st.container(border=True):
        st.subheader("📈 Top 3 Points Progression")
        st.caption("Trailing 6-month ranking points trajectory")
        
        # Generate mock trend data for the premium chart
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        trend_data = pd.DataFrame({
            "Month": months * 3,
            "Player": ["Djokovic"]*6 + ["Alcaraz"]*6 + ["Sinner"]*6,
            "Points": [
                8900, 9100, 9350, 9350, 9500, 9870,  # Djokovic
                8200, 8400, 8900, 9100, 9250, 9500,  # Alcaraz
                7800, 8100, 8500, 8700, 8950, 9100   # Sinner
            ]
        })
        
        fig = px.area(
            trend_data, 
            x="Month", y="Points", color="Player",
            color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981"]
        )
        
        # FIXED: Removed fillOpacity, using clean lines+markers
        fig.update_traces(mode="lines+markers", line=dict(width=3), marker=dict(size=6))
        
        fig.update_layout(
            height=300,
            margin=dict(l=10, r=20, t=20, b=20),
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="ATP Points", showgrid=True, gridcolor="rgba(128, 128, 128, 0.15)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

with col_summary:
    with st.container(border=True):
        st.markdown("### 🤖 Algorithmic Synthesis")
        st.markdown("""
        <div style="color: #64748b; font-size: 1.05rem; line-height: 1.6;">
        The competitive landscape demonstrates a heavy concentration of talent at the absolute top tier. 
        <br><br>
        While <b>Novak Djokovic</b> maintains structural dominance in the rankings equation, the derivative momentum of <b>Carlos Alcaraz</b> and <b>Jannik Sinner</b> shows a steepening upward curve. 
        <br><br>
        If current point-accumulation win rates continue, our models predict a potential rank inversion within the next <b>90 days</b>.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
        st.button("📄 Export Full AI Report", use_container_width=True, type="primary")

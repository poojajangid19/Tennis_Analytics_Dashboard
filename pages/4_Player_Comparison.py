import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Player Head-to-Head Comparison",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS / STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1350px;
    }

    /* Hero Header */
    .hero-banner {
        background: radial-gradient(circle at 50% 0%, #1e3a8a 0%, #090d16 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px 32px;
        color: white;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        border: 1px solid rgba(147, 197, 253, 0.3);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        color: #ffffff;
    }
    .hero-desc {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* Player Profile Cards */
    .player-card {
        background: var(--background-secondary);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }
    .player-flag {
        font-size: 1.8rem;
        margin-bottom: 4px;
    }
    .player-name {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 4px 0 2px 0;
    }
    .player-meta {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 12px;
    }

    /* VS Badge */
    .vs-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 160px;
    }
    .vs-circle {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white;
        font-weight: 900;
        font-size: 1.15rem;
        letter-spacing: 0.05em;
        width: 58px;
        height: 58px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 18px rgba(239, 68, 68, 0.4);
        border: 3px solid rgba(255, 255, 255, 0.2);
    }

    /* Stat Cards */
    div[data-testid="stMetric"] {
        background-color: var(--background-secondary);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 14px;
        padding: 14px 16px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PLAYER DATABASE
# ==========================================
PLAYERS = {
    "Novak Djokovic": {
        "country": "Serbia",
        "flag": "🇷🇸",
        "rank": 1,
        "points": 9870,
        "titles": 98,
        "win_rate": 88.5,
        "serve": 88,
        "return": 96,
        "baseline": 95,
        "speed": 86,
        "mental": 98,
        "color": "#3b82f6"
    },
    "Carlos Alcaraz": {
        "country": "Spain",
        "flag": "🇪🇸",
        "rank": 2,
        "points": 9500,
        "titles": 16,
        "win_rate": 84.2,
        "serve": 89,
        "return": 90,
        "baseline": 92,
        "speed": 96,
        "mental": 90,
        "color": "#f59e0b"
    },
    "Jannik Sinner": {
        "country": "Italy",
        "flag": "🇮🇹",
        "rank": 3,
        "points": 9100,
        "titles": 14,
        "win_rate": 86.1,
        "serve": 92,
        "return": 88,
        "baseline": 94,
        "speed": 91,
        "mental": 89,
        "color": "#10b981"
    },
    "Daniil Medvedev": {
        "country": "Russia",
        "flag": "🇷🇺",
        "rank": 4,
        "points": 8700,
        "titles": 20,
        "win_rate": 79.8,
        "serve": 86,
        "return": 93,
        "baseline": 91,
        "speed": 87,
        "mental": 85,
        "color": "#8b5cf6"
    }
}

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="hero-banner">
    <span class="hero-badge">ATP Tour • Head-to-Head Analysis</span>
    <h1 class="hero-title">⚔️ Player Comparison Suite</h1>
    <p class="hero-desc">Evaluate direct match-ups, attribute radars, and core ATP performance metrics side-by-side.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PLAYER SELECTORS & PROFILES
# ==========================================
col_left, col_mid, col_right = st.columns([1, 0.22, 1], gap="medium")

player_list = list(PLAYERS.keys())

with col_left:
    with st.container(border=True):
        st.caption("PRIMARY CONTENDER")
        p1_name = st.selectbox("Select Player 1", player_list, index=0, label_visibility="collapsed")
        p1 = PLAYERS[p1_name]

        st.markdown(f"""
        <div class="player-card">
            <div class="player-flag">{p1['flag']}</div>
            <div class="player-name">{p1_name}</div>
            <div class="player-meta">{p1['country']} • World Rank #{p1['rank']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_mid:
    st.markdown("""
    <div class="vs-container">
        <div class="vs-circle">VS</div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    with st.container(border=True):
        st.caption("SECONDARY CONTENDER")
        # Default index to 1 if available
        p2_name = st.selectbox("Select Player 2", player_list, index=1, label_visibility="collapsed")
        p2 = PLAYERS[p2_name]

        st.markdown(f"""
        <div class="player-card">
            <div class="player-flag">{p2['flag']}</div>
            <div class="player-name">{p2_name}</div>
            <div class="player-meta">{p2['country']} • World Rank #{p2['rank']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ==========================================
# QUICK COMPARISON METRICS
# ==========================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    rank_diff = p2["rank"] - p1["rank"]  # Negative diff means p1 is higher rank
    st.metric(
        "Rank Delta",
        f"#{p1['rank']} vs #{p2['rank']}",
        delta=f"{rank_diff:+d} pos" if rank_diff != 0 else "Equal",
        delta_color="normal" if rank_diff > 0 else "inverse"
    )

with c2:
    pts_diff = p1["points"] - p2["points"]
    st.metric(
        "Points Spread",
        f"{p1['points']:,} vs {p2['points']:,}",
        delta=f"{pts_diff:+,} pts"
    )

with c3:
    win_diff = round(p1["win_rate"] - p2["win_rate"], 1)
    st.metric(
        "Win Rate",
        f"{p1['win_rate']}% vs {p2['win_rate']}%",
        delta=f"{win_diff:+.1f}%"
    )

with c4:
    title_diff = p1["titles"] - p2["titles"]
    st.metric(
        "Career Titles",
        f"{p1['titles']} vs {p2['titles']}",
        delta=f"{title_diff:+d} titles"
    )

# ==========================================
# VISUAL BREAKDOWN TABS
# ==========================================
tab_radar, tab_bars, tab_table = st.tabs(["🕸️ Skill Radar", "📊 Head-to-Head Bars", "📋 Data Breakdown"])

attributes = ["serve", "return", "baseline", "speed", "mental"]
labels = ["Serve Power", "Return Game", "Baseline Rally", "Pace & Speed", "Clutch / Mental"]

with tab_radar:
    with st.container(border=True):
        st.subheader("Attributes Radar")
        st.caption("Ratings out of 100 benchmarked across ATP performance data")

        r1 = [p1[a] for a in attributes] + [p1[attributes[0]]]
        r2 = [p2[a] for a in attributes] + [p2[attributes[0]]]
        radar_labels = labels + [labels[0]]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=r1,
            theta=radar_labels,
            fill='toself',
            name=p1_name,
            line=dict(color="#3b82f6", width=2.5),
            fillcolor="rgba(59, 130, 246, 0.25)"
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=r2,
            theta=radar_labels,
            fill='toself',
            name=p2_name,
            line=dict(color="#ef4444", width=2.5),
            fillcolor="rgba(239, 68, 68, 0.25)"
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[75, 100], gridcolor="rgba(128, 128, 128, 0.2)"),
                angularaxis=dict(gridcolor="rgba(128, 128, 128, 0.2)")
            ),
            height=430,
            margin=dict(l=40, r=40, t=30, b=30),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_radar, use_container_width=True)

with tab_bars:
    with st.container(border=True):
        st.subheader("Direct Metric Comparisons")
        st.caption("Point-by-point head-to-head scores")

        bar_data = pd.DataFrame({
            "Skill": labels,
            p1_name: [p1[a] for a in attributes],
            p2_name: [p2[a] for a in attributes]
        })

        fig_bars = go.Figure()
        fig_bars.add_trace(go.Bar(
            y=bar_data["Skill"],
            x=bar_data[p1_name],
            name=p1_name,
            orientation='h',
            marker=dict(color="#3b82f6"),
            text=bar_data[p1_name],
            textposition="inside"
        ))
        fig_bars.add_trace(go.Bar(
            y=bar_data["Skill"],
            x=bar_data[p2_name],
            name=p2_name,
            orientation='h',
            marker=dict(color="#ef4444"),
            text=bar_data[p2_name],
            textposition="inside"
        ))

        fig_bars.update_layout(
            barmode='group',
            height=380,
            margin=dict(l=10, r=20, t=20, b=20),
            xaxis=dict(title="Score (out of 100)", range=[0, 105], showgrid=True, gridcolor="rgba(128, 128, 128, 0.15)"),
            yaxis=dict(title=""),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bars, use_container_width=True)

with tab_table:
    st.subheader("Side-by-Side Summary")

    comparison_df = pd.DataFrame({
        "Performance Metric": [
            "World Rank",
            "ATP Points",
            "Win Rate",
            "Career Titles",
            "Serve Index",
            "Return Index",
            "Baseline Index",
            "Speed & Agility",
            "Clutch Rating"
        ],
        p1_name: [
            f"#{p1['rank']}",
            f"{p1['points']:,}",
            f"{p1['win_rate']}%",
            f"{p1['titles']}",
            f"{p1['serve']} / 100",
            f"{p1['return']} / 100",
            f"{p1['baseline']} / 100",
            f"{p1['speed']} / 100",
            f"{p1['mental']} / 100"
        ],
        p2_name: [
            f"#{p2['rank']}",
            f"{p2['points']:,}",
            f"{p2['win_rate']}%",
            f"{p2['titles']}",
            f"{p2['serve']} / 100",
            f"{p2['return']} / 100",
            f"{p2['baseline']} / 100",
            f"{p2['speed']} / 100",
            f"{p2['mental']} / 100"
        ]
    })

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "Performance Metric": st.column_config.TextColumn("Metric", width="medium"),
            p1_name: st.column_config.TextColumn(f"{p1['flag']} {p1_name}", width="medium"),
            p2_name: st.column_config.TextColumn(f"{p2['flag']} {p2_name}", width="medium")
        }
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
st.caption(f"⚡ Head-to-Head generated between **{p1_name}** ({p1['country']}) and **{p2_name}** ({p2['country']}).")
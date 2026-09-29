import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎾 Match Analysis")

# Load Data
df = pd.read_csv("data/competitions.csv")

# Show available columns
# st.write(df.columns)

# -----------------------
# Filters
# -----------------------

col1, col2 = st.columns(2)

with col1:
    if "gender" in df.columns:
        gender = st.selectbox(
            "Select Gender",
            ["All"] + sorted(df["gender"].dropna().unique().tolist())
        )
    else:
        gender = "All"

with col2:
    if "type" in df.columns:
        comp_type = st.selectbox(
            "Competition Type",
            ["All"] + sorted(df["type"].dropna().unique().tolist())
        )
    else:
        comp_type = "All"

filtered = df.copy()

if gender != "All":
    filtered = filtered[filtered["gender"] == gender]

if comp_type != "All":
    filtered = filtered[filtered["type"] == comp_type]

# -----------------------
# KPI Cards
# -----------------------

st.markdown("---")

k1, k2, k3, k4 = st.columns(4)

k1.metric("🏆 Competitions", len(filtered))

if "category" in filtered.columns:
    k2.metric(
        "📂 Categories",
        filtered["category"].nunique()
    )

if "country" in filtered.columns:
    k3.metric(
        "🌍 Countries",
        filtered["country"].nunique()
    )

if "name" in filtered.columns:
    k4.metric(
        "🎾 Events",
        filtered["name"].nunique()
    )

st.markdown("---")

# -----------------------
# Competition Chart
# -----------------------

if "country" in filtered.columns:

    country_df = (
        filtered["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_df.columns = ["Country", "Competitions"]

    fig = px.bar(
        country_df,
        x="Country",
        y="Competitions",
        color="Competitions",
        title="Top Countries by Competitions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------
# Competition Table
# -----------------------

st.subheader("📋 Competition Details")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.success(
    f"Showing {len(filtered)} competitions"
)
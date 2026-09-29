import streamlit as st
import pandas as pd

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Data Inspection",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tennis Analytics - Data Inspection")
st.markdown("Inspect all datasets before starting EDA and dashboard development.")

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    competitors = pd.read_csv("data/competitors.csv")
    rankings = pd.read_csv("data/competitor_rankings.csv")
    competitions = pd.read_csv("data/competitions.csv")
    venues = pd.read_csv("data/venues.csv")
    complexes = pd.read_csv("data/complexes.csv")
    categories = pd.read_csv("data/categories.csv")

    return (
        competitors,
        rankings,
        competitions,
        venues,
        complexes,
        categories
    )

(
    competitors,
    rankings,
    competitions,
    venues,
    complexes,
    categories
) = load_data()

# ------------------------------
# Dataset Viewer Function
# ------------------------------
def show_dataset(name, df):

    st.markdown("---")
    st.header(f"📁 {name}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    st.subheader("Column Names")
    st.write(df.columns.tolist())

    st.subheader("Sample Records")
    st.dataframe(df.head())

# ------------------------------
# Sidebar Dataset Selector
# ------------------------------
dataset_option = st.sidebar.selectbox(
    "Select Dataset",
    [
        "Competitors",
        "Rankings",
        "Competitions",
        "Venues",
        "Complexes",
        "Categories"
    ]
)

# ------------------------------
# Display Selected Dataset
# ------------------------------
if dataset_option == "Competitors":
    show_dataset("Competitors", competitors)

elif dataset_option == "Rankings":
    show_dataset("Rankings", rankings)

elif dataset_option == "Competitions":
    show_dataset("Competitions", competitions)

elif dataset_option == "Venues":
    show_dataset("Venues", venues)

elif dataset_option == "Complexes":
    show_dataset("Complexes", complexes)

elif dataset_option == "Categories":
    show_dataset("Categories", categories)

# ------------------------------
# Dataset Summary
# ------------------------------
st.markdown("---")
st.subheader("📋 Dataset Summary")

summary_df = pd.DataFrame({
    "Dataset": [
        "Competitors",
        "Rankings",
        "Competitions",
        "Venues",
        "Complexes",
        "Categories"
    ],
    "Rows": [
        competitors.shape[0],
        rankings.shape[0],
        competitions.shape[0],
        venues.shape[0],
        complexes.shape[0],
        categories.shape[0]
    ],
    "Columns": [
        competitors.shape[1],
        rankings.shape[1],
        competitions.shape[1],
        venues.shape[1],
        complexes.shape[1],
        categories.shape[1]
    ]
})

st.dataframe(summary_df, use_container_width=True)

st.success("✅ Data Loaded Successfully")
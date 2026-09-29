import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Inspection", layout="wide")

st.title("📊 Data Inspection")

# Load CSV Files
competitors = pd.read_csv("data/competitors.csv")
rankings = pd.read_csv("data/competitor_rankings.csv")
competitions = pd.read_csv("data/competitions.csv")
venues = pd.read_csv("data/venues.csv")
complexes = pd.read_csv("data/complexes.csv")
categories = pd.read_csv("data/categories.csv")

# Function to display dataset info
def show_dataset(name, df):
    st.header(name)

    st.subheader("Columns")
    st.write(df.columns.tolist())

    st.subheader("Shape")
    st.write(df.shape)

    st.subheader("Sample Data")
    st.dataframe(df.head())

# Display all datasets
show_dataset("Competitors", competitors)
show_dataset("Rankings", rankings)
show_dataset("Competitions", competitions)
show_dataset("Venues", venues)
show_dataset("Complexes", complexes)
show_dataset("Categories", categories)
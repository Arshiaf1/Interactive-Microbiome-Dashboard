import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="Microbiome Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("🦠 Interactive Microbiome & Metagenomics Dashboard")
st.markdown("### By Arshia")

st.markdown("""
Welcome to the Interactive Microbiome Dashboard! This tool allows you to explore and visualize the 
**Moving Pictures of the Human Microbiome** dataset.

Navigate through the pages on the sidebar to discover:
- **Taxonomy**: Explore microbial composition across different body sites.
- **Diversity**: Analyze within-sample (Alpha) and between-sample (Beta) diversity.
- **Ordination**: Visualize sample clustering using Principal Coordinates Analysis (PCoA).
- **Sample Explorer**: Drill down into specific samples.
""")

st.divider()

# Load summary statistics
@st.cache_data
def load_summary():
    try:
        df_meta = pd.read_csv('data/processed/metadata.csv')
        df_otu = pd.read_csv('data/processed/otu_counts.csv', index_col=0)
        return df_meta, df_otu
    except FileNotFoundError:
        return None, None

df_meta, df_otu = load_summary()

if df_meta is not None:
    st.subheader("Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Samples", len(df_meta))
    with col2:
        st.metric("Body Sites", df_meta["body-site"].nunique())
    with col3:
        st.metric("Subjects", df_meta["subject"].nunique())
    with col4:
        st.metric("Unique ASVs", len(df_otu.columns))

    st.markdown("### Metadata Snapshot")
    st.dataframe(df_meta.head())
else:
    st.warning("⚠️ Processed data not found. Please run the preprocessing pipeline first.")

st.markdown("---")
st.markdown("*Developed with Python, Streamlit, and Plotly.*")

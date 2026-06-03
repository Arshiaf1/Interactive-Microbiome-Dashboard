import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Alpha Diversity", page_icon="🧬", layout="wide")

st.title("🧬 Alpha Diversity")

@st.cache_data
def load_data():
    try:
        df_alpha = pd.read_csv('data/processed/alpha_diversity.csv', index_col=0)
        df_meta = pd.read_csv('data/processed/metadata.csv', index_col=0)
        return df_alpha, df_meta
    except FileNotFoundError:
        return None, None

df_alpha, df_meta = load_data()

if df_alpha is not None:
    # Merge alpha and meta
    df_merged = df_alpha.join(df_meta)
    
    st.markdown("""
    **Alpha diversity** measures the richness and evenness of microbial species within a single sample.
    - **Shannon**: Accounts for both abundance and evenness of the species present.
    - **Simpson**: Measures the degree of concentration when individuals are classified into types.
    - **Chao1**: Estimates total richness (including unobserved species).
    """)
    
    st.sidebar.header("Plot Settings")
    
    metric = st.sidebar.selectbox("Diversity Metric", ['shannon', 'simpson', 'chao1'])
    group_by = st.sidebar.selectbox("Group By (X-axis)", df_meta.columns, index=list(df_meta.columns).index('body-site') if 'body-site' in df_meta.columns else 0)
    color_by = st.sidebar.selectbox("Color By", ['None'] + list(df_meta.columns), index=list(df_meta.columns).index('subject')+1 if 'subject' in df_meta.columns else 0)
    
    # Box plot
    fig = px.box(
        df_merged.reset_index(),
        x=group_by,
        y=metric,
        color=color_by if color_by != 'None' else None,
        points="all",
        title=f"{metric.capitalize()} Index by {group_by}",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        xaxis_title=group_by.capitalize(),
        yaxis_title=f"{metric.capitalize()} Diversity",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Diversity data not found. Please run `diversity_calc.py` first.")

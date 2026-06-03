import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sample Explorer", page_icon="🔍", layout="wide")

st.title("🔍 Sample Explorer")

@st.cache_data
def load_data():
    try:
        df_otu_rel = pd.read_csv('data/processed/otu_rel_abundance.csv', index_col=0)
        df_tax = pd.read_csv('data/processed/taxonomy.csv', index_col=0)
        df_meta = pd.read_csv('data/processed/metadata.csv', index_col=0)
        return df_otu_rel, df_tax, df_meta
    except FileNotFoundError:
        return None, None, None

df_otu_rel, df_tax, df_meta = load_data()

if df_otu_rel is not None:
    st.markdown("Select a sample from the sidebar to view its specific metadata and taxonomic composition.")
    
    sample_id = st.sidebar.selectbox("Select Sample ID", df_meta.index)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"Metadata for `{sample_id}`")
        sample_meta = df_meta.loc[sample_id]
        st.table(sample_meta)
        
    with col2:
        st.subheader("Taxonomic Composition")
        tax_level = st.selectbox("Taxonomic Level", ['Phylum', 'Class', 'Order', 'Family', 'Genus'])
        
        sample_counts = df_otu_rel.loc[sample_id]
        # Filter non-zero
        sample_counts = sample_counts[sample_counts > 0]
        
        # Merge with taxonomy
        df_sample = pd.DataFrame(sample_counts).join(df_tax[[tax_level]])
        df_sample.columns = ['Relative Abundance', tax_level]
        
        # Aggregate
        df_agg = df_sample.groupby(tax_level).sum()
        
        # Keep top 10
        top_taxa = df_agg['Relative Abundance'].nlargest(10).index
        df_agg_top = df_agg.loc[top_taxa].copy()
        other_sum = df_agg.loc[~df_agg.index.isin(top_taxa), 'Relative Abundance'].sum()
        if other_sum > 0:
            df_agg_top.loc['Other'] = other_sum
            
        fig = px.pie(
            df_agg_top.reset_index(), 
            values='Relative Abundance', 
            names=tax_level,
            title=f"Top 10 {tax_level} in {sample_id}",
            hole=0.4,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Data not found. Please run the preprocessing pipeline first.")

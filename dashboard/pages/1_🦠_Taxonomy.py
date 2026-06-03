import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Taxonomy", page_icon="🦠", layout="wide")

st.title("🦠 Taxonomic Composition")

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
    # Sidebar Filters
    st.sidebar.header("Filter Settings")
    
    tax_level = st.sidebar.selectbox(
        "Taxonomic Level",
        ['Phylum', 'Class', 'Order', 'Family', 'Genus']
    )
    
    group_by = st.sidebar.selectbox(
        "Group by Metadata",
        ['None'] + list(df_meta.columns)
    )
    
    body_site_filter = st.sidebar.multiselect(
        "Filter Body Site",
        options=df_meta['body-site'].unique(),
        default=df_meta['body-site'].unique()
    )
    
    # Filter metadata
    df_meta_filtered = df_meta[df_meta['body-site'].isin(body_site_filter)]
    valid_samples = df_meta_filtered.index
    
    df_otu_filtered = df_otu_rel.loc[valid_samples]
    
    # Merge OTU with Taxonomy
    df_merged = df_otu_filtered.T.join(df_tax[[tax_level]])
    
    # Aggregate by Taxonomic Level
    df_agg = df_merged.groupby(tax_level).sum().T
    
    # If Grouping by metadata
    if group_by != 'None':
        df_agg = df_agg.join(df_meta_filtered[[group_by]])
        df_agg = df_agg.groupby(group_by).mean()
        
    # Keep top 15 taxa for visualization, group rest as 'Other'
    top_taxa = df_agg.mean().nlargest(15).index
    df_agg_top = df_agg[top_taxa].copy()
    df_agg_top['Other'] = 1.0 - df_agg_top.sum(axis=1)
    
    # Plotly Stacked Bar Chart
    df_plot = df_agg_top.reset_index().melt(id_vars=df_agg_top.index.name or 'index', var_name='Taxon', value_name='Relative Abundance')
    
    fig = px.bar(
        df_plot, 
        x=df_agg_top.index.name or 'index', 
        y='Relative Abundance', 
        color='Taxon',
        title=f"Relative Abundance at {tax_level} Level",
        color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_white"
    )
    
    fig.update_layout(
        xaxis_title=group_by if group_by != 'None' else "Sample ID",
        yaxis_title="Relative Abundance",
        legend_title="Taxon",
        barmode='stack',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.subheader("Aggregated Data")
    st.dataframe(df_agg_top.style.format("{:.2%}"))

else:
    st.warning("⚠️ Data not found. Please run the preprocessing pipeline first.")

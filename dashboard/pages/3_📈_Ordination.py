import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Beta Diversity (PCoA)", page_icon="📈", layout="wide")

st.title("📈 Beta Diversity (Ordination)")

@st.cache_data
def load_data():
    try:
        df_pcoa = pd.read_csv('data/processed/pcoa_braycurtis.csv', index_col=0)
        df_prop = pd.read_csv('data/processed/pcoa_braycurtis_explained.csv', index_col=0)
        df_meta = pd.read_csv('data/processed/metadata.csv', index_col=0)
        return df_pcoa, df_prop, df_meta
    except FileNotFoundError:
        return None, None, None

df_pcoa, df_prop, df_meta = load_data()

if df_pcoa is not None:
    st.markdown("""
    **Beta diversity** measures the differences in composition between samples. 
    Here, we use Principal Coordinates Analysis (PCoA) on Bray-Curtis dissimilarity distances to visualize how samples cluster together based on their metadata.
    """)
    
    # Merge pcoa and meta
    df_merged = df_pcoa.join(df_meta)
    
    st.sidebar.header("Plot Settings")
    
    color_by = st.sidebar.selectbox("Color By", df_meta.columns, index=list(df_meta.columns).index('body-site') if 'body-site' in df_meta.columns else 0)
    symbol_by = st.sidebar.selectbox("Shape By", ['None'] + list(df_meta.columns), index=list(df_meta.columns).index('subject')+1 if 'subject' in df_meta.columns else 0)
    
    plot_type = st.sidebar.radio("Plot Type", ["2D Scatter", "3D Scatter"])
    
    # Ensure prop names
    prop_1 = df_prop.iloc[0, 0] * 100
    prop_2 = df_prop.iloc[1, 0] * 100
    prop_3 = df_prop.iloc[2, 0] * 100
    
    if plot_type == "2D Scatter":
        fig = px.scatter(
            df_merged.reset_index(),
            x='PC1',
            y='PC2',
            color=color_by,
            symbol=symbol_by if symbol_by != 'None' else None,
            hover_data=['index'] + list(df_meta.columns),
            title="PCoA - Bray-Curtis (2D)",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            xaxis_title=f"Axis 1 ({prop_1:.1f}%)",
            yaxis_title=f"Axis 2 ({prop_2:.1f}%)",
            height=700
        )
        # Increase marker size
        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        fig = px.scatter_3d(
            df_merged.reset_index(),
            x='PC1',
            y='PC2',
            z='PC3',
            color=color_by,
            symbol=symbol_by if symbol_by != 'None' else None,
            hover_data=['index'] + list(df_meta.columns),
            title="PCoA - Bray-Curtis (3D)",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            scene=dict(
                xaxis_title=f"Axis 1 ({prop_1:.1f}%)",
                yaxis_title=f"Axis 2 ({prop_2:.1f}%)",
                zaxis_title=f"Axis 3 ({prop_3:.1f}%)"
            ),
            height=800
        )
        fig.update_traces(marker=dict(size=8, line=dict(width=0)))
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ PCoA data not found. Please run `diversity_calc.py` first.")

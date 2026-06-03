import os
import pandas as pd
import numpy as np
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.ordination import pcoa
import warnings

# Suppress warnings from scikit-bio regarding missing taxa
warnings.filterwarnings('ignore')

def calculate_diversity():
    print("Starting diversity calculations...")
    
    processed_dir = os.path.join('data', 'processed')
    otu_counts_path = os.path.join(processed_dir, 'otu_counts.csv')
    
    if not os.path.exists(otu_counts_path):
        raise FileNotFoundError("Processed OTU counts not found. Run pipeline.py first.")
        
    df_otu = pd.read_csv(otu_counts_path, index_col=0)
    
    # 1. Alpha Diversity
    print("Computing Alpha Diversity (Shannon, Simpson, Chao1)...")
    
    # ensure counts are integers for chao1
    counts = np.round(df_otu.values).astype(int)
    ids = df_otu.index.tolist()
    
    shannon = alpha_diversity('shannon', counts, ids)
    simpson = alpha_diversity('simpson', counts, ids)
    chao1 = alpha_diversity('chao1', counts, ids)
    
    df_alpha = pd.DataFrame({
        'shannon': shannon,
        'simpson': simpson,
        'chao1': chao1
    })
    
    alpha_path = os.path.join(processed_dir, 'alpha_diversity.csv')
    df_alpha.to_csv(alpha_path)
    print(f"Saved Alpha Diversity to {alpha_path}")
    
    # 2. Beta Diversity & PCoA
    print("Computing Beta Diversity (Bray-Curtis)...")
    
    # Beta diversity requires non-empty samples
    valid_samples = df_otu.sum(axis=1) > 0
    if not valid_samples.all():
        print(f"Filtering out {sum(~valid_samples)} empty samples before Beta Diversity")
        df_otu = df_otu.loc[valid_samples]
        ids = df_otu.index.tolist()
        counts = df_otu.values
        
    bc_dm = beta_diversity("braycurtis", counts, ids)
    
    print("Performing Principal Coordinates Analysis (PCoA)...")
    bc_pcoa = pcoa(bc_dm)
    
    # Extract Coordinates
    df_pcoa = bc_pcoa.samples
    # Save the proportion explained for the dashboard
    proportion_explained = bc_pcoa.proportion_explained
    
    df_pcoa.index = ids
    
    # Save PCoA coordinates and proportions
    pcoa_path = os.path.join(processed_dir, 'pcoa_braycurtis.csv')
    df_pcoa.to_csv(pcoa_path)
    
    prop_path = os.path.join(processed_dir, 'pcoa_braycurtis_explained.csv')
    proportion_explained.to_csv(prop_path)
    
    print(f"Saved PCoA coordinates to {pcoa_path}")
    print("Diversity calculations complete!")

if __name__ == '__main__':
    calculate_diversity()

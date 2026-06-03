import os
import glob
import pandas as pd
from biom import load_table

def find_file(base_dir, pattern):
    search_path = os.path.join(base_dir, '**', pattern)
    matches = glob.glob(search_path, recursive=True)
    if not matches:
        raise FileNotFoundError(f"Could not find {pattern} in {base_dir}")
    return matches[0]

def process_data():
    print("Starting data processing pipeline...")
    
    # Paths
    raw_dir = os.path.join('data', 'raw')
    processed_dir = os.path.join('data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    # 1. Load Metadata
    metadata_path = os.path.join(raw_dir, 'sample_metadata.tsv')
    print(f"Loading metadata from {metadata_path}")
    df_meta = pd.read_csv(metadata_path, sep='\t', skiprows=[1]) # Skip the q2:types row
    df_meta.rename(columns={'sample-id': 'sample_id'}, inplace=True)
    df_meta.set_index('sample_id', inplace=True)
    
    # 2. Load Feature Table (BIOM)
    table_qza_dir = os.path.join(raw_dir, 'table_qza')
    biom_path = find_file(table_qza_dir, 'feature-table.biom')
    print(f"Loading BIOM table from {biom_path}")
    table = load_table(biom_path)
    df_otu = table.to_dataframe(dense=True).T # Transpose: samples as rows, OTUs as columns
    
    # 3. Load Taxonomy
    tax_qza_dir = os.path.join(raw_dir, 'taxonomy_qza')
    tax_path = find_file(tax_qza_dir, 'taxonomy.tsv')
    print(f"Loading taxonomy from {tax_path}")
    df_tax = pd.read_csv(tax_path, sep='\t')
    df_tax.rename(columns={'Feature ID': 'feature_id', 'Taxon': 'taxonomy'}, inplace=True)
    df_tax.set_index('feature_id', inplace=True)
    
    # Clean up taxonomy string into levels
    print("Parsing taxonomy levels...")
    tax_levels = ['Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    tax_split = df_tax['taxonomy'].str.split(';', expand=True)
    
    # Make sure we only take up to 7 levels, or pad if less
    for i in range(len(tax_levels)):
        if i < tax_split.shape[1]:
            # Clean up the "d__Bacteria" or "k__Bacteria" prefixes
            df_tax[tax_levels[i]] = tax_split[i].str.replace(r'^[a-z]__', '', regex=True).str.strip()
        else:
            df_tax[tax_levels[i]] = 'Unassigned'
            
    df_tax.fillna('Unassigned', inplace=True)
    
    # Filter OTU table and Metadata to only overlapping samples
    common_samples = df_otu.index.intersection(df_meta.index)
    df_otu = df_otu.loc[common_samples]
    df_meta = df_meta.loc[common_samples]
    
    # Convert OTU counts to relative abundance (compositional)
    print("Calculating relative abundances...")
    df_otu_rel = df_otu.div(df_otu.sum(axis=1), axis=0)
    
    # Save processed files
    print("Saving processed files to data/processed/ ...")
    df_meta.to_csv(os.path.join(processed_dir, 'metadata.csv'))
    df_otu.to_csv(os.path.join(processed_dir, 'otu_counts.csv'))
    df_otu_rel.to_csv(os.path.join(processed_dir, 'otu_rel_abundance.csv'))
    df_tax.to_csv(os.path.join(processed_dir, 'taxonomy.csv'))
    
    print("Data processing complete!")

if __name__ == '__main__':
    process_data()

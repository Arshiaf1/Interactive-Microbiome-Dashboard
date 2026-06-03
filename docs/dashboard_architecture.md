# Dashboard Architecture

## Tech Stack
*   **Framework**: Streamlit (Python)
*   **Data Manipulation**: pandas, numpy
*   **Visualization**: Plotly Graph Objects and Express

## Layout Structure
The dashboard is structured as a multi-page Streamlit application to ensure a clean, modular user experience.

1.  **Home (`app.py`)**: The entry point. Provides an overview of the dataset, project goals, and high-level dataset statistics.
2.  **Taxonomy Page**: Features interactive stacked bar charts to explore microbial composition across different taxonomic levels (Phylum to Genus), with dynamic filtering by body site and subject.
3.  **Diversity Page**: Visualizes Alpha Diversity metrics (Shannon, Simpson) via box plots to compare within-sample richness and evenness across metadata groups.
4.  **Ordination Page**: Displays Beta Diversity (e.g., Bray-Curtis) using Principal Coordinates Analysis (PCoA). Users can color and shape points based on metadata to observe clustering.
5.  **Sample Explorer Page**: Allows for deep-dive investigation of individual samples and their specific taxonomic makeup.

## Data Flow
1.  **Offline Processing**: Raw data (OTU tables, taxonomy, metadata) is processed offline using scripts in `src/data_processing/`. Diversity metrics are pre-calculated to ensure the dashboard remains fast.
2.  **Loading**: The dashboard loads processed datasets (`.csv` or `.parquet`) using Streamlit's `@st.cache_data` decorator to prevent redundant I/O operations.
3.  **Interactivity**: User inputs (dropdowns, sliders) trigger pandas filtering operations, which then dynamically update Plotly figures.

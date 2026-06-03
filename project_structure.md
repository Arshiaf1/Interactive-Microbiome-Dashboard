# Project Structure

```text
.
├── dashboard/               # Streamlit application
│   ├── app.py               # Main entry point for the dashboard
│   └── pages/               # Multi-page Streamlit views (e.g., taxonomy, diversity)
├── data/
│   ├── metadata/            # Sample metadata files
│   ├── processed/           # Cleaned data ready for dashboard visualization
│   └── raw/                 # Original dataset files
├── docs/                    # Project documentation
│   ├── dashboard_architecture.md
│   ├── dataset_description.md
│   └── reproducibility.md
├── env/                     # Environment configuration (if any specific scripts)
├── figures/                 # Generated static figures and plots
├── notebooks/               # Jupyter notebooks for exploratory data analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_microbiome_analysis.ipynb
│   └── 03_dashboard_validation.ipynb
├── results/                 # Analysis outputs (e.g., statistical tests)
├── src/                     # Source code for data processing and analysis
│   ├── data_processing/     # Scripts to clean and format data
│   ├── utils/               # Helper functions
│   └── visualization/       # Reusable plotting functions
├── tests/                   # Unit tests for source code
├── .gitignore               # Git ignored files
├── CONTRIBUTING.md          # Contribution guidelines
├── environment.yml          # Conda environment file
├── LICENSE                  # MIT License
├── README.md                # Project overview and instructions
└── requirements.txt         # pip dependencies
```

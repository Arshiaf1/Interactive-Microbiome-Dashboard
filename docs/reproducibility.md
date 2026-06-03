# Reproducibility

Ensuring reproducibility is a core tenet of this project. Follow these steps to reproduce the entire environment and analysis.

## Environment Setup

You can set up the required Python environment using either Conda or standard pip.

### Using Conda (Recommended)
1. Ensure Conda/Miniconda is installed.
2. Run the following command in the repository root:
   ```bash
   conda env create -f environment.yml
   conda activate microbiome-dashboard
   ```

### Using pip
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Data Pipeline
If you wish to re-run the data processing and diversity calculations from scratch:
1. Ensure the raw datasets are located in `data/raw/`.
2. Run the processing pipeline:
   ```bash
   python src/data_processing/pipeline.py
   python src/data_processing/diversity_calc.py
   ```
This will populate the `data/processed/` directory.

## Running the Dashboard
To launch the Streamlit dashboard locally:
```bash
streamlit run dashboard/app.py
```
The dashboard will open automatically in your default web browser at `http://localhost:8501`.

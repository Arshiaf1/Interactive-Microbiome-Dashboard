# Dataset Description

## Overview
This project uses the classic **"Moving Pictures of the Human Microbiome"** dataset, originally published by Caporaso et al. (2011) and widely used as the foundational tutorial dataset for QIIME 2.

## Source
*   **Original Publication**: Caporaso, J. G., et al. (2011). Global patterns of 16S rRNA diversity at a depth of millions of sequences per sample. *PNAS*.
*   **Data Access**: Obtained via the QIIME 2 tutorial resources.

## Dataset Characteristics
*   **Sample Count**: 34 samples.
*   **Subjects**: Two individuals (Subject 1 and Subject 2).
*   **Body Sites**: Four distinct sites were sampled:
    *   Gut (feces)
    *   Left palm
    *   Right palm
    *   Tongue
*   **Timepoints**: Samples were collected at multiple timepoints (days since the start of the experiment).
*   **Other Metadata**: Antibiotic usage (reported during the study).

## Biological Context
This dataset is excellent for demonstrating microbiome analysis techniques because it exhibits strong biological signals:
1.  **Body Site Differentiation**: Microbiome composition varies drastically between the gut, skin (palms), and oral cavity (tongue). This is easily visualizable in beta diversity ordinations.
2.  **Inter-personal Variation**: Samples from the same body site cluster more closely within an individual than across individuals.

## Limitations
*   The sample size is relatively small, which limits the statistical power of complex machine learning models.
*   It is an amplicon sequencing (16S rRNA) dataset, not whole-genome shotgun metagenomics, meaning functional profiling is limited or inferred.

## Justification
The Moving Pictures dataset was selected because it provides clear, undeniable biological signals that are perfect for visualization in an interactive dashboard. It is lightweight, ensuring the dashboard remains fast and responsive, while still containing enough metadata complexity (body site, subject, timepoint) to enable rich interactive filtering and exploration.

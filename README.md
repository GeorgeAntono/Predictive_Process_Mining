# Predictive Process Mining: Clustering-Based PM Framework

List of contributors:
Georgios Antonopoulos
Orcun Karabicak
Sjoerd Offringa
Krzysztof Wiesniakowski

**Subtitle:** Enhancing predictive accuracy in process mining through clustering, supervised learning, and on-the-fly prediction.

## Motivation

In predictive process mining, identifying deviant and normal behaviors in event traces is crucial for actionable insights and operational efficiency. This project addresses the challenge of providing robust and accurate predictions for partially completed traces. 

The **on-the-fly model** serves as a baseline, demonstrating the trade-offs between runtime overhead and accuracy, while the **clustering-based predictive monitoring framework** offers a more efficient solution by pre-training classifiers offline.

## Method and Results

### Method

The project employs two approaches for predictive process monitoring:

1. **Clustering-Based Predictive Monitoring**
   - **Trace Preprocessing:** Event logs are sorted by timestamps, missing values are handled, and trace attributes are encoded. The **latest-payload encoding** is used to capture both static (trace-level) and dynamic (event-level) attributes, ensuring predictive relevance.
   - **Prefix Extraction and Encoding:** Partial prefixes of varying lengths are extracted from traces and encoded to capture trace behavior over time.
   - **Clustering with DBSCAN:** Encoded prefixes are clustered using DBSCAN, with parameters:
     - `eps`: Maximum distance between points to form a cluster.
     - `min_samples`: Minimum number of points required to form a cluster.
     These parameters are optimized for trace variability and clustering density.
   - **Training Classifiers:** Decision tree classifiers are trained for each cluster to distinguish between deviant and normal traces, providing cluster-specific predictions.
   - **Predictive Monitoring:** Running traces are matched to clusters based on their prefixes, and predictions are made using the corresponding cluster’s pre-trained classifier, significantly reducing runtime overhead.

2. **On-the-Fly Predictive Monitoring**
   

### Results

- **Accuracy:** The clustering-based model achieves comparable accuracy to the on-the-fly model while maintaining runtime efficiency.
- **Runtime Efficiency:** The clustering-based framework significantly reduces runtime overhead compared to the on-the-fly model, making it suitable for high-throughput and low-latency environments.
- **Parameter Insights:** Adjustments to DBSCAN parameters (`eps`, `min_samples`) and classifier thresholds improve clustering quality and prediction reliability.
- **Visualizations:** t-SNE plots demonstrate distinct clusters, with visual annotations showing decision tree predictions, validating the framework’s effectiveness.

## Repository Overview

This repository contains the files and scripts needed for preprocessing, clustering, training, and evaluating both predictive monitoring approaches:

```plaintext
__pycache__/                    # Python cache files
data/                           # Event logs and data files
visualizations/                 # Visual outputs (e.g., cluster plots)
.gitignore                      # Git ignore file
DBSCAN_DT.ipynb                 # Clustering-based predictive monitoring implementation
README.md                       # This README file
data_exploration.ipynb          # Data preprocessing and exploration
data_exploration.py             # Script for preprocessing
functions.py                    # Core functions (encoding, clustering, prediction)
label_functions.py              # Custom labeling functions
on-the-fly_model.ipynb          # Implementation of the on-the-fly predictive monitoring model
on_the_fly_results.csv          # Results of the on-the-fly model
requirements.txt                # Python dependencies


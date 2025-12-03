# 📈 RESULTS ANALYSIS & Dataset Generation

This document outlines the standard operating procedure for post-processing the raw benchmark data (Flow B) into the final analysis-ready dataset and generating publishable figures.

---

## 🛠️ Raw Data Processing Pipeline

The goal of the processing pipeline is to transform the high-granularity raw data log into a sanitized, standardized **CSV Dataset** suitable for community sharing and direct academic analysis.

### 1. **Data Extraction and Conversion**

* **Source:** The primary input is the high-resolution raw data log generated during the benchmark execution (Flow B, as defined in `METRICS_SPECIFICATION.md`).
* **Initial Scripting:** A dedicated Python script (`data_processor.py`) will be used to ingest the raw log structure (e.g., JSON Lines) and perform initial field mapping and data type casting.
* **Output Format:** The final dataset for publication must conform to the **Comma Separated Values (CSV)** standard, ensuring maximum compatibility with statistical software (e.g., R, Python Pandas).

### 2. **Data Sanitization and Filtering**

Before aggregation, the following steps ensure data quality and integrity:

* **Filter Warm-up Phase:** All data points recorded during the initial **warm-up phase** of the benchmark (e.g., the first 60 seconds of execution) must be discarded to eliminate startup overhead artifacts.
* **Outlier Handling:** Statistical outliers (e.g., $\text{Value} > \text{Mean} + 3\sigma$) may be identified but **must not be removed** from the public raw dataset. A separate filtered dataset may be used for specific aggregations, with explicit documentation of the removal criteria.
* **Error Reporting:** Entries corresponding to failed transactions or cryptographic operations must be isolated and reported separately in the final analysis (e.g., failure rate metric).

### 3. **Statistical Aggregation**

While the public dataset is raw, the final results presented in the paper will rely on aggregated statistics derived from this dataset.

* **Key Aggregates:** The pipeline will calculate the **Mean**, **Standard Deviation ($\sigma$)**, and the **95th Percentile (P95)** for the following core time metrics, segmented by **Cryptosystem** and **Operation Phase**:
    * Signature Generation Time (ms)
    * Signature Verification Time (ms)
    * End-to-End Transaction Latency (s)
* **Statistical Robustness:** All final reported aggregates must be the mean of the metrics calculated across the $\text{N} \ge 5$ independent benchmark runs.

---

## 🖼️ Publishable Figures Generation

The processed CSV Dataset is the single source for generating all figures required for publication and comparison reports.

### 1. **Comparative Distributions (Box Plots)**

* **Purpose:** Visually compare the central tendency, spread, and skewness of the latency distributions for different cryptographic modes.
* **Data Source:** Raw data from the `Signature Verification Time` and `Transaction Latency` metrics (Flow B).
* **Figure Type:** **Box-and-Whisker Plots** or **Violin Plots** are mandatory for illustrating the entire distribution (Mean, Median, Quartiles, and potential outliers) rather than relying solely on the mean.

### 2. **Throughput Scaling (Line Graphs)**

* **Purpose:** Analyze the relationship between load (concurrency) and system capacity.
* **Data Source:** Aggregated `Transaction Throughput (TPS)` metric (Flow A or aggregated Flow B).
* **Figure Type:** **Line Graphs** where the X-axis represents the number of concurrent client threads and the Y-axis represents the achieved TPS. Clear labeling for ECDSA, PQC, and Hybrid modes is required.

### 3. **Overhead Quantification (Bar Charts)**

* **Purpose:** Explicitly quantify the relative performance penalty.
* **Data Source:** Aggregated `Average Block Size` and `Signature Time` metrics.
* **Figure Type:** **Bar Charts** comparing the percentage increase in size or time for PQC/Hybrid relative to the established ECDSA baseline.

---

## 📚 Dataset Documentation and Reproducibility

The following elements must accompany the published dataset to ensure scientific rigor:

1.  **Schema Definition:** A separate document detailing the exact column names, data types, and units used in the public CSV file.
2.  **Benchmark Configuration:** The configuration files used for the $\text{N}$ runs must be archived alongside the dataset.
3.  **Analysis Scripts:** The Python scripts used for post-processing and figure generation should be open-sourced to facilitate replication of the reported results.
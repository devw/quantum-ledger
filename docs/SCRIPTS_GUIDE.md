# Scripts Guide

Comprehensive guide for all executable scripts in the project. All commands should be run from the project root directory.

## 📋 Table of Contents

- [Data Generation](#data-generation)
- [Data Analysis & Visualization](#data-analysis--visualization)
- [Prerequisites](#prerequisites)

---

## Data Generation

### Generate Monte Carlo Samples

Generate synthetic Monte Carlo simulation data for testing and analysis.

**Script:** `tools/scripts/generate_mock_data.py`

```bash
# Generate 1000 samples (default)
python tools/scripts/generate_mock_data.py \
    --iterations 1000 \
    --output data/fixtures/monte_carlo/samples.csv

# Generate custom number of samples
python tools/scripts/generate_mock_data.py \
    --iterations 5000 \
    --output data/raw/my_samples.csv
```

**Parameters:**
- `--iterations` - Number of Monte Carlo iterations (default: 1000)
- `--output` - Output CSV file path (default: `data/fixtures/monte_carlo/samples.csv`)

---

## Data Analysis & Visualization

### Generate Plots

Create scatter plot visualizations from Monte Carlo simulation data.

**Script:** `analysis/scripts/generate_plots.py`

```bash
# Using default CSV file
python analysis/scripts/generate_plots.py

# Using custom CSV file
python analysis/scripts/generate_plots.py \
    --csv data/raw/my_samples.csv
```

**Parameters:**
- `--csv` - Path to CSV file (default: `data/fixtures/monte_carlo/samples.csv`)

---

### Generate LaTeX Tables

Generate summary statistics tables in LaTeX format.

**Script:** `analysis/scripts/generate_latex_tables.py`

```bash
# Using default CSV file
python analysis/scripts/generate_latex_tables.py

# Using custom CSV file
python analysis/scripts/generate_latex_tables.py \
    --csv data/raw/my_samples.csv
```

**Parameters:**
- `--csv` - Path to CSV file (default: `data/fixtures/monte_carlo/samples.csv`)

---

## Prerequisites

### Python Dependencies

```bash
python3.13 -m pip install -r requirements.txt
```

---

## Complete Workflow Example

End-to-end example from data generation to visualization:

```bash
# 1. Generate Monte Carlo samples
python tools/scripts/generate_mock_data.py \
    --iterations 2000 \
    --output data/fixtures/monte_carlo/samples.csv

# 2. Generate visualization
python analysis/scripts/generate_plots.py \
    --csv data/fixtures/monte_carlo/samples.csv

# 3. Generate statistics table
python analysis/scripts/generate_latex_tables.py \
    --csv data/fixtures/monte_carlo/samples.csv

# 4. View outputs
ls -lh /tmp/monte_carlo_*
```

---

## Troubleshooting

### Common Issues

**"Module not found" error**
- Cause: Running from wrong directory
- Solution: Always run from project root

**"File not found" error**
- Cause: CSV file doesn't exist or wrong path
- Solution: Generate data first or verify path

**"Permission denied" writing to /tmp/**
- Cause: No write permissions
- Solution: Check permissions or modify script output directory

**Import errors in scripts**
- Cause: Missing dependencies
- Solution: `python3.13 -m pip install -r requirements.txt`

---

## Related Documentation

- `docs/DATASET_SPECIFICATION.md` - Data format specifications
- `docs/RESULTS_ANALYSIS.md` - Analysis methodology
- `analysis/README.md` - Detailed analysis module documentation
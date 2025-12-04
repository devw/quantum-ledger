# Scripts Guide

Guide to all executable scripts in the project. Run all commands from the project root.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Data Generation](#data-generation)
- [Data Analysis & Visualization](#data-analysis--visualization)
- [Testing](#testing)
- [Complete Workflow Example](#complete-workflow-example)
- [Troubleshooting](#troubleshooting)
- [Related Documentation](#related-documentation)

---

## Prerequisites

Install project dependencies:

```bash
python3.13 -m pip install -r requirements.txt         # runtime deps
python3.13 -m pip install -r requirements-dev.txt     # dev & test deps
````

---

## Data Generation

Generate synthetic Monte Carlo data:

**Script:** `tools/scripts/generate_mock_data.py`

```bash
# Default: 1000 samples
python tools/scripts/generate_mock_data.py --iterations 1000 --output data/fixtures/monte_carlo/samples.csv

# Custom samples
python tools/scripts/generate_mock_data.py --iterations 5000 --output data/raw/my_samples.csv
```

---

## Data Analysis & Visualization

### Generate Plots

**Script:** `analysis/scripts/generate_plots.py`

```bash
# Default CSV
python analysis/scripts/generate_plots.py

# Custom CSV
python analysis/scripts/generate_plots.py --csv data/raw/my_samples.csv
```

### Generate LaTeX Tables

**Script:** `analysis/scripts/generate_latex_tables.py`

```bash
python analysis/scripts/generate_latex_tables.py --csv data/raw/my_samples.csv
```

---

## Testing

Run all tests using pytest:

```bash
# Run all tests with verbose output
pytest -v

# Run a single test file
pytest -v tests/unit/tools/data_generation/test_distributions.py
```

Tests use **fixtures** for configuration and are automatically compatible with pytest.

---

## Complete Workflow Example

```bash
# 1. Generate data
python tools/scripts/generate_mock_data.py --iterations 2000 --output data/fixtures/monte_carlo/samples.csv

# 2. Generate plots
python analysis/scripts/generate_plots.py --csv data/fixtures/monte_carlo/samples.csv

# 3. Generate LaTeX tables
python analysis/scripts/generate_latex_tables.py --csv data/fixtures/monte_carlo/samples.csv

# 4. Optional: run tests
pytest -v
```

---

## Troubleshooting

* **Module not found** → run from project root
* **File not found** → generate data first or verify path
* **Permission denied** → check output directory permissions
* **Import errors** → install missing dependencies (`requirements.txt` / `requirements-dev.txt`)

---

## Related Documentation

* `docs/DATASET_SPECIFICATION.md` – Data format
* `docs/RESULTS_ANALYSIS.md` – Analysis methodology
* `analysis/README.md` – Analysis module details

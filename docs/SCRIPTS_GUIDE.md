# Scripts Guide

Guide to all executable scripts in the project. Run all commands from the project root.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Data Generation](#data-generation)
- [Data Analysis & Visualization](#data-analysis--visualization)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt         # runtime deps
pip install -r requirements-dev.txt     # dev & test deps
```

---

## Data Generation

**Script:** `tools/scripts/generate_benchmark_data.py`

### Quick Examples

```bash
# Minimal test (2 files, 10 seconds)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA \
    --load-profiles LOWLOAD \
    --runs 2 \
    --duration 10 \
    --output-dir data/fixtures/monte_carlo/test/

# Workshop dataset (18 files, 5 minutes each)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA DILITHIUM3 HYBRID \
    --load-profiles LOWLOAD HIGHLOAD \
    --runs 3 \
    --duration 300 \
    --output-dir data/fixtures/monte_carlo/workshop/

# Complete dataset (60 files, 10 minutes each)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA DILITHIUM3 HYBRID \
    --load-profiles LOWLOAD MEDIUMLOAD HIGHLOAD SUSTAINED \
    --runs 5 \
    --duration 600 \
    --output-dir data/raw/complete/

# Reproducible (same data every time)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA DILITHIUM3 HYBRID \
    --load-profiles LOWLOAD HIGHLOAD \
    --runs 3 \
    --duration 300 \
    --seed 42 \
    --output-dir data/fixtures/monte_carlo/reproducible/
```

### CLI Options

| Option | Values | Description |
|--------|--------|-------------|
| `--crypto-modes` | `ECDSA DILITHIUM3 HYBRID` | Cryptographic algorithms |
| `--load-profiles` | `LOWLOAD MEDIUMLOAD HIGHLOAD SUSTAINED` | Workload patterns |
| `--runs` | `1-N` | Repetitions per combination |
| `--duration` | seconds | Samples = duration (1/sec) |
| `--output-dir` | path | CSV output directory |
| `--seed` | integer | Fixed seed for reproducibility |
| `--quiet` | flag | Suppress output |

**Output:** `{CRYPTO_MODE}_{LOAD_PROFILE}_RUN{N}.csv` (13 columns per file)

**Note:** CSV files are NOT committed to git (regenerate with `--seed 42` for reproducibility).

---

## Data Analysis & Visualization

**Generate Plots:** `analysis/scripts/generate_plots.py`

```bash
python analysis/scripts/generate_plots.py --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv
```

**Generate LaTeX Tables:** `analysis/scripts/generate_latex_tables.py`

```bash
python analysis/scripts/generate_latex_tables.py --csv data/raw/my_samples.csv
```

---

## Testing

```bash
pytest -v                                                    # All tests
pytest -v tests/unit/data_generation/                       # Data generation only
pytest -v tests/unit/scripts/test_generate_benchmark_data.py     # CLI script tests
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run from project root |
| Import errors | `pip install -r requirements.txt` |
| Invalid mode/profile | See CLI options table above |

**Verify installation:**
```bash
python -c "from tools.data_generation import samplers; print('✅ OK')"
```

---

**See also:** `docs/DATASET_SPECIFICATION.md` for CSV format details
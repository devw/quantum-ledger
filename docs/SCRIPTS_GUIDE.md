# Scripts Guide

Executable scripts for data generation, analysis, and reporting. Run from project root.

---

## Prerequisites

```bash
pip install -r requirements.txt         # runtime
pip install -r requirements-dev.txt     # dev/test
```

---

## Data Generation

**Script:** `tools/scripts/generate_benchmark_data.py`

```bash
# Quick test (2 files, 10s each)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA --load-profiles LOWLOAD --runs 2 --duration 10 \
    --output-dir data/fixtures/monte_carlo/test/

# Workshop dataset (18 files, 5min each)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA DILITHIUM3 HYBRID \
    --load-profiles LOWLOAD HIGHLOAD --runs 3 --duration 300 \
    --output-dir data/fixtures/monte_carlo/workshop/

# Reproducible (fixed seed)
python tools/scripts/generate_benchmark_data.py \
    --crypto-modes ECDSA DILITHIUM3 HYBRID \
    --load-profiles LOWLOAD HIGHLOAD --runs 3 --duration 300 \
    --seed 42 --output-dir data/fixtures/monte_carlo/reproducible/
```

**Options:**
- `--crypto-modes`: `ECDSA DILITHIUM3 HYBRID`
- `--load-profiles`: `LOWLOAD MEDIUMLOAD HIGHLOAD SUSTAINED`
- `--runs`: repetitions per combination
- `--duration`: seconds (samples = duration)
- `--seed`: for reproducibility
- `--quiet`: suppress output

**Output:** `{CRYPTO}_{LOAD}_RUN{N}.csv` (13 columns/file)

---

## Reporting & Visualization

### Plot Generators

**Performance Curve (TPS vs P95 Latency):**
```bash
python tools/reporting/generate_performance_curve.py \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv \
    --output /tmp/performance_curve.png
```

**Time-Series Plots:**
```bash
python tools/reporting/generate_plots.py \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv
```

### Table Generators

**LaTeX Tables:**
```bash
python tools/reporting/generate_latex_tables.py \
    --csv data/raw/my_samples.csv
```

---

## Testing

```bash
pytest -v                                             # all tests
pytest -v tests/unit/data_generation/                # data generation
pytest -v tests/unit/scripts/                        # CLI scripts
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Module not found | Run from project root |
| Import errors | `pip install -r requirements.txt` |
| Invalid mode/profile | Check options above |

**Verify:**
```bash
python -c "from tools.data_generation import samplers; print('✅')"
```
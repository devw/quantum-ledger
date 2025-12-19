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

**Options:** `--crypto-modes` (ECDSA|DILITHIUM3|HYBRID), `--load-profiles` (LOWLOAD|MEDIUMLOAD|HIGHLOAD|SUSTAINED), `--runs` (repetitions), `--duration` (seconds), `--seed` (reproducibility), `--quiet`

**Output:** `{CRYPTO}_{LOAD}_RUN{N}.csv` (13 columns/file)

---

## Visualization

### Performance Curve (TPS vs P95 Latency)
```bash
python -m tools.reporting.generate_performance_curve \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv \
    --output /tmp/performance_curve.png
```

### Box Plot Comparison
```bash
python -m tools.reporting.generate_box_plot \
    --csv data/fixtures/monte_carlo/workshop/*.csv \
    --metric latency_avg \
    --output /tmp/latency_boxplot.png

# Custom title
python -m tools.reporting.generate_box_plot \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_*.csv \
          data/fixtures/monte_carlo/workshop/DILITHIUM3_*.csv \
          data/fixtures/monte_carlo/workshop/HYBRID_*.csv \
    --metric sig_gen_time \
    --output /tmp/sig_gen_comparison.png \
    --title "Signature Generation: ECDSA vs Dilithium3 vs Hybrid"
```

**Supported metrics:** `latency_avg`, `latency_p95`, `tx_rate`, `cpu_util`, `mem_util`, `sig_gen_time`, `sig_verify_time`, `block_commit_time`, `block_size`

### LaTeX Tables
```bash
python -m tools.reporting.generate_latex_tables \
    --csv data/raw/my_samples.csv
```

---

## Testing

```bash
pytest -v                                    # all tests
pytest -v tests/unit/data_generation/        # data generation only
pytest -v tests/unit/scripts/                # CLI scripts only
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Module not found | Run from project root |
| Import errors | `pip install -r requirements.txt` |
| Invalid parameters | Check options in sections above |

**Verify installation:**
```bash
python -c "from tools.data_generation import samplers; print('✅')"
```
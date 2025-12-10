# Reporting Tools

Generate plots and tables from benchmark CSV data. All outputs to `/tmp/`.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt  # pandas, numpy, matplotlib

# Run from project root
python tools/reporting/generate_performance_curve.py \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv

python tools/reporting/generate_overhead_breakdown.py \
    --csv data/fixtures/monte_carlo/workshop/*_LOWLOAD_RUN1.csv

python tools/reporting/generate_plots.py \
    --csv data/fixtures/monte_carlo/workshop/ECDSA_LOWLOAD_RUN1.csv

python tools/reporting/generate_latex_tables.py \
    --csv data/raw/my_samples.csv
```

## Available Reports

| Script | Output | Description |
|--------|--------|-------------|
| `generate_performance_curve.py` | PNG | TPS vs P95 Latency scatter plot with trend line |
| `generate_overhead_breakdown.py` | PNG | Stacked bar chart: sig_gen + sig_verify by crypto mode |
| `generate_plots.py` | PNG | Time-series analysis plots |
| `generate_latex_tables.py` | TEX | Statistical summary tables |

## Common Options

```bash
--csv PATH       # Input CSV file(s), supports wildcards for multi-file
--output PATH    # Output path (default: /tmp/)
--title TEXT     # Custom plot title
```

## Development

**Shared utilities:** `utils/csv_loader.py`, `utils/file_utils.py`

**Adding new reports:**
1. Create script in `tools/reporting/`
2. Use utilities for CSV loading and output management
3. Follow CLI pattern: `--csv`, `--output`, `--title`

## Troubleshooting

**Module not found:** Run from project root  
**CSV not found:** Check path, verify file exists  
**Permission denied:** Verify `/tmp/` write access
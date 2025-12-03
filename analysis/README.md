# Data Analysis & Visualization

Scripts for analyzing Monte Carlo simulation data and generating visualizations and statistical reports.

## Quick Start

### Installation

```bash
pip install -r requirements.txt  # pandas, numpy, matplotlib
```

### Usage

**Run from project root:**

```bash
# Generate scatter plot → /tmp/monte_carlo_analysis.png
python analysis/scripts/generate_plots.py

# Generate LaTeX table → /tmp/monte_carlo_statistics.tex
python analysis/scripts/generate_latex_tables.py

# Custom CSV file
python analysis/scripts/generate_plots.py --csv path/to/data.csv
python analysis/scripts/generate_latex_tables.py --csv path/to/data.csv
```

**Default CSV:** `data/fixtures/monte_carlo/samples.csv`

## Development

Code follows SOLID/DRY principles:
- `CSVLoader` - CSV loading
- `OutputManager` - File output
- `LaTeXFormatter` - LaTeX formatting
- `SummaryStatisticsCalculator` - Statistics
- `MonteCarloPlotter` - Plotting

**Adding new plots:** Add method to `MonteCarloPlotter` class  
**Adding new tables:** Create calculator class, add to `LaTeXTableGenerator`

## Troubleshooting

**Module not found:** Run from project root, not `analysis/` directory  
**File not found:** Verify `data/fixtures/monte_carlo/samples.csv` exists  
**Permission denied:** Check write access to `/tmp/`
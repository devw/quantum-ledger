"""Generate box plots for benchmark data comparison.
Usage:
    python -m tools.reporting.generate_box_plot \\
        --csv data/fixtures/monte_carlo/workshop/*.csv \\
        --metric latency_avg \\
        --output /tmp/latency_boxplot.png \\
        --fontsize 14
"""
import argparse
import glob
from pathlib import Path
from .utils.data_aggregator import DataAggregator
from .utils.plot_config import create_metric_config
from .utils.box_plotter import BoxPlotter

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate box plot comparisons')
    parser.add_argument('--csv', nargs='+', required=True, help='CSV file paths (supports glob)')
    parser.add_argument('--metric', required=True, help='Metric to plot')
    parser.add_argument('--output', required=True, help='Output PNG path')
    parser.add_argument('--title', help='Custom plot title')
    parser.add_argument('--fontsize', type=int, default=14, help='Font size for labels (default: 14)')
    parser.add_argument('--title-fontsize', type=int, default=16, help='Font size for title (default: 16)')
    return parser.parse_args()

def expand_paths(patterns):
    """Expand glob patterns to file paths."""
    files = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if not matches:
            print(f"⚠ Warning: No files match pattern: {pattern}")
        files.extend(matches)
    return sorted(files)

def main():
    """Main execution flow."""
    args = parse_args()
    
    # Expand glob patterns
    csv_files = expand_paths(args.csv)
    if not csv_files:
        print("✗ Error: No CSV files found")
        return 1
    
    print(f"\n{'='*60}")
    print(f"Box Plot Generator - {args.metric}")
    print(f"{'='*60}\n")
    
    # Load and aggregate data
    aggregator = DataAggregator(csv_files)
    aggregator.load_all()
    grouped_data = aggregator.get_grouped_data(args.metric)
    
    # Create plot configuration
    config = create_metric_config(args.metric)
    if args.title:
        config.title = args.title
    
    # Generate and save plot with custom font sizes
    plotter = BoxPlotter(config)
    plotter.create_plot(
        grouped_data, 
        fontsize=args.fontsize,
        title_fontsize=args.title_fontsize
    )
    plotter.save(Path(args.output))
    
    print(f"\n{'='*60}")
    print("✓ Completed successfully")
    print(f"Font sizes: labels={args.fontsize}, title={args.title_fontsize}")
    print(f"{'='*60}\n")
    
    return 0

if __name__ == '__main__':
    exit(main())
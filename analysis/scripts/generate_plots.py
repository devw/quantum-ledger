#!/usr/bin/env python3
"""
Generate matplotlib scatter plot showing relationship between tx_rate and block_size.
Stores output in /tmp/ directory.

Usage:
    python analysis/scripts/generate_plots.py
    python analysis/scripts/generate_plots.py --csv path/to/data.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import CSVLoader, OutputManager


class MonteCarloPlotter:
    """Responsible for creating Monte Carlo simulation visualizations."""
    
    def __init__(self, df: pd.DataFrame, output_manager: OutputManager):
        self.df = df
        self.output_manager = output_manager
    
    def plot_txrate_vs_blocksize(self):
        """
        Create scatter plot showing relationship between transaction rate 
        and block size with network latency as color dimension.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scatter = ax.scatter(
            self.df['tx_rate'],
            self.df['block_size'],
            c=self.df['latency_avg'],
            cmap='viridis',
            alpha=0.6,
            s=50,
            edgecolors='black',
            linewidth=0.5
        )
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Network Latency (ms)', rotation=270, labelpad=20)
        
        # Labels and title
        ax.set_xlabel('Transaction Rate (tx/s)', fontsize=12)
        ax.set_ylabel('Block Size (KB)', fontsize=12)
        ax.set_title('Monte Carlo Simulation: Transaction Rate vs Block Size', 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # Save
        output_path = self.output_manager.get_path('monte_carlo_analysis.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_path}")


class PlotGenerator:
    """Orchestrates the plot generation process (Open/Closed Principle)."""
    
    def __init__(self, csv_path: str, output_dir: str = "/tmp"):
        self.csv_loader = CSVLoader(csv_path)
        self.output_manager = OutputManager(output_dir)
        self.df = None
    
    def run(self):
        """Execute plot generation workflow."""
        self._print_header()
        self.df = self.csv_loader.load()
        self._generate_plots()
        self._print_footer()
    
    def _generate_plots(self):
        """Generate all plots."""
        print(f"\n📁 Output directory: {self.output_manager.output_dir}")
        print("\n🎨 Generating plot...")
        
        plotter = MonteCarloPlotter(self.df, self.output_manager)
        plotter.plot_txrate_vs_blocksize()
    
    @staticmethod
    def _print_header():
        print("\n" + "="*60)
        print("📊 Generating Matplotlib Plot")
        print("="*60)
    
    @staticmethod
    def _print_footer():
        print("\n" + "="*60)
        print("✅ Plot generation complete!")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate PNG plot from Monte Carlo simulation CSV data'
    )
    parser.add_argument(
        '--csv',
        type=str,
        default='data/fixtures/monte_carlo/samples.csv',
        help='Path to CSV file (default: data/fixtures/monte_carlo/samples.csv)'
    )
    
    args = parser.parse_args()
    
    generator = PlotGenerator(csv_path=args.csv)
    generator.run()


if __name__ == "__main__":
    main()
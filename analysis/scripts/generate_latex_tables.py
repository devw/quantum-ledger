#!/usr/bin/env python3
"""
Generate LaTeX table with summary statistics from Monte Carlo simulation CSV.
Stores output in /tmp/ directory.

Usage:
    python analysis/scripts/generate_latex_tables.py
    python analysis/scripts/generate_latex_tables.py --csv path/to/data.csv
"""

import argparse
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from utils import CSVLoader, OutputManager


class LaTeXFormatter:
    """Responsible for LaTeX formatting (Single Responsibility Principle)."""
    
    @staticmethod
    def format_table(df: pd.DataFrame, caption: str, label: str, precision: int = 2) -> str:
        """
        Generate a well-formatted LaTeX table from a DataFrame.
        
        Args:
            df: DataFrame to convert
            caption: Table caption
            label: Table label for referencing
            precision: Number of decimal places for float formatting
        
        Returns:
            LaTeX table as string
        """
        df_formatted = df.copy()
        
        # Format numeric columns
        for col in df_formatted.columns:
            if df_formatted[col].dtype in ['float64', 'float32']:
                df_formatted[col] = df_formatted[col].apply(
                    lambda x: f"{x:.{precision}f}" if pd.notna(x) else "N/A"
                )
        
        # Column alignment
        num_cols = len(df.columns)
        alignment = 'l' + 'r' * num_cols
        
        # Build LaTeX table
        latex = [
            r"\begin{table}[htbp]",
            r"  \centering",
            f"  \\caption{{{caption}}}",
            f"  \\label{{{label}}}",
            f"  \\begin{{tabular}}{{{alignment}}}",
            r"    \toprule"
        ]
        
        # Header row
        header = " & ".join([df.index.name or "Metric"] + [str(col) for col in df.columns])
        latex.append(f"    {header} \\\\")
        latex.append(r"    \midrule")
        
        # Data rows
        for idx, row in df_formatted.iterrows():
            row_data = " & ".join([str(idx)] + [str(val) for val in row.values])
            latex.append(f"    {row_data} \\\\")
        
        # End table
        latex.extend([
            r"    \bottomrule",
            r"  \end{tabular}",
            r"\end{table}"
        ])
        
        return "\n".join(latex)


class SummaryStatisticsCalculator:
    """Responsible for calculating summary statistics (Single Responsibility)."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def calculate(self) -> pd.DataFrame:
        """Calculate comprehensive summary statistics."""
        numeric_df = self.df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            raise ValueError("No numeric columns found in DataFrame")
        
        # Calculate statistics
        stats = pd.DataFrame({
            'Mean': numeric_df.mean(),
            'Std Dev': numeric_df.std(),
            'Min': numeric_df.min(),
            'Q1 (25%)': numeric_df.quantile(0.25),
            'Median': numeric_df.median(),
            'Q3 (75%)': numeric_df.quantile(0.75),
            'Max': numeric_df.max(),
            'Count': numeric_df.count()
        })
        
        return stats.T


class LaTeXTableGenerator:
    """Orchestrates the LaTeX table generation process."""
    
    def __init__(self, csv_path: str, output_dir: str = "/tmp"):
        self.csv_loader = CSVLoader(csv_path)
        self.output_manager = OutputManager(output_dir)
        self.formatter = LaTeXFormatter()
        self.df = None
    
    def run(self):
        """Execute table generation workflow."""
        self._print_header()
        self.df = self.csv_loader.load()
        self._generate_table()
        self._print_footer()
    
    def _generate_table(self):
        """Generate summary statistics table."""
        print(f"\n📁 Output directory: {self.output_manager.output_dir}")
        print("\n📊 Generating LaTeX table...")
        
        try:
            # Calculate statistics
            calculator = SummaryStatisticsCalculator(self.df)
            stats = calculator.calculate()
            
            # Format as LaTeX
            latex_table = self.formatter.format_table(
                stats,
                caption="Summary Statistics of Monte Carlo Simulation Parameters",
                label="tab:monte_carlo_stats",
                precision=2
            )
            
            # Save
            self.output_manager.save_text(latex_table, "monte_carlo_statistics.tex")
            
        except ValueError as e:
            print(f"  ⚠ Error: {e}")
    
    @staticmethod
    def _print_header():
        print("\n" + "="*60)
        print("📋 Generating LaTeX Table")
        print("="*60)
    
    @staticmethod
    def _print_footer():
        print("\n" + "="*60)
        print("✅ LaTeX table generation complete!")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate LaTeX table with summary statistics from CSV data'
    )
    parser.add_argument(
        '--csv',
        type=str,
        default='data/fixtures/monte_carlo/samples.csv',
        help='Path to CSV file (default: data/fixtures/monte_carlo/samples.csv)'
    )
    
    args = parser.parse_args()
    
    generator = LaTeXTableGenerator(csv_path=args.csv)
    generator.run()


if __name__ == "__main__":
    main()
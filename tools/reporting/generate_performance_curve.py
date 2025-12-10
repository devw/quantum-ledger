#!/usr/bin/env python3
"""
Performance Curve Plot Generator
Plots Throughput (TPS) vs P95 Latency to visualize performance trade-offs.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def load_data(csv_path: str) -> pd.DataFrame:
    """Load and validate CSV data."""
    try:
        df = pd.read_csv(csv_path)
        required_cols = ['tx_rate', 'latency_p95']
        
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}", file=sys.stderr)
        sys.exit(1)


def create_performance_curve(df: pd.DataFrame, output_path: str, title: str = None):
    """
    Create scatter plot of TPS vs P95 Latency.
    
    Args:
        df: DataFrame with 'tx_rate' and 'latency_p95' columns
        output_path: Path to save the plot
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Scatter plot
    scatter = ax.scatter(
        df['tx_rate'], 
        df['latency_p95'],
        alpha=0.6,
        s=50,
        c=df.index,  # Color by time/sequence
        cmap='viridis',
        edgecolors='black',
        linewidth=0.5
    )
    
    # Calculate and plot trend line
    z = np.polyfit(df['tx_rate'], df['latency_p95'], 2)
    p = np.poly1d(z)
    x_trend = np.linspace(df['tx_rate'].min(), df['tx_rate'].max(), 100)
    ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend (polynomial)')
    
    # Styling
    ax.set_xlabel('Throughput (TPS)', fontsize=12, fontweight='bold')
    ax.set_ylabel('P95 Latency (ms)', fontsize=12, fontweight='bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title('Performance Curve: Throughput vs P95 Latency', 
                     fontsize=14, fontweight='bold', pad=20)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add statistics text box
    stats_text = (
        f"Statistics:\n"
        f"TPS: μ={df['tx_rate'].mean():.1f}, σ={df['tx_rate'].std():.1f}\n"
        f"P95: μ={df['latency_p95'].mean():.1f}, σ={df['latency_p95'].std():.1f}\n"
        f"Points: {len(df)}"
    )
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, label='Measurement Sequence')
    
    # Legend
    ax.legend(loc='upper right')
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Performance curve saved to: {output_path}")
    
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Generate Performance Curve plot (TPS vs P95 Latency)'
    )
    parser.add_argument(
        '--csv',
        required=True,
        help='Path to CSV file with benchmark data'
    )
    parser.add_argument(
        '--output',
        default='/tmp/performance_curve.png',
        help='Output path for plot (default: /tmp/performance_curve.png)'
    )
    parser.add_argument(
        '--title',
        help='Custom plot title'
    )
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from: {args.csv}")
    df = load_data(args.csv)
    print(f"Loaded {len(df)} data points")
    
    # Generate plot
    print("Generating performance curve...")
    create_performance_curve(df, args.output, args.title)
    
    print("Done!")


if __name__ == '__main__':
    main()
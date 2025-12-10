#!/usr/bin/env python3
"""
Overhead Breakdown Plot Generator
Stacked bar chart comparing sig_gen_time and sig_verify_time across crypto modes.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


def load_and_aggregate(csv_paths: List[str]) -> pd.DataFrame:
    """
    Load multiple CSVs and aggregate cryptographic overhead metrics.
    
    Returns DataFrame with columns: crypto_mode, gen_mean, gen_std, verify_mean, verify_std
    """
    all_data = []
    
    for csv_path in csv_paths:
        try:
            df = pd.read_csv(csv_path)
            required_cols = ['crypto_mode', 'sig_gen_time', 'sig_verify_time']
            
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                print(f"Warning: Skipping {csv_path}, missing columns: {missing}", file=sys.stderr)
                continue
            
            all_data.append(df[required_cols])
        except Exception as e:
            print(f"Warning: Could not load {csv_path}: {e}", file=sys.stderr)
            continue
    
    if not all_data:
        print("Error: No valid CSV files loaded", file=sys.stderr)
        sys.exit(1)
    
    # Combine all data
    combined = pd.concat(all_data, ignore_index=True)
    
    # Aggregate by crypto_mode
    aggregated = combined.groupby('crypto_mode').agg({
        'sig_gen_time': ['mean', 'std'],
        'sig_verify_time': ['mean', 'std']
    }).reset_index()
    
    # Flatten column names
    aggregated.columns = ['crypto_mode', 'gen_mean', 'gen_std', 'verify_mean', 'verify_std']
    
    # Fill NaN std with 0 (in case of single sample)
    aggregated = aggregated.fillna(0)
    
    return aggregated


def create_overhead_breakdown(df: pd.DataFrame, output_path: str, title: str = None):
    """
    Create stacked bar chart for cryptographic overhead breakdown.
    
    Args:
        df: DataFrame with columns [crypto_mode, gen_mean, gen_std, verify_mean, verify_std]
        output_path: Path to save the plot
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Prepare data
    crypto_modes = df['crypto_mode'].values
    gen_means = df['gen_mean'].values
    gen_stds = df['gen_std'].values
    verify_means = df['verify_mean'].values
    verify_stds = df['verify_std'].values
    
    x = np.arange(len(crypto_modes))
    width = 0.6
    
    # Color scheme
    color_gen = '#3498db'      # Blue for generation
    color_verify = '#e74c3c'   # Red for verification
    
    # Stacked bars
    bar1 = ax.bar(x, gen_means, width, label='Signature Generation',
                  color=color_gen, edgecolor='black', linewidth=1.2)
    bar2 = ax.bar(x, verify_means, width, bottom=gen_means, label='Signature Verification',
                  color=color_verify, edgecolor='black', linewidth=1.2)
    
    # Error bars
    # For stacked bars: gen error at gen_mean/2, verify error at gen_mean + verify_mean/2
    ax.errorbar(x, gen_means / 2, yerr=gen_stds, fmt='none', 
                ecolor='black', capsize=5, capthick=2, alpha=0.7)
    ax.errorbar(x, gen_means + verify_means / 2, yerr=verify_stds, fmt='none',
                ecolor='black', capsize=5, capthick=2, alpha=0.7)
    
    # Add value labels on bars
    for i, (gm, vm) in enumerate(zip(gen_means, verify_means)):
        # Generation label
        ax.text(i, gm / 2, f'{gm:.1f}ms', ha='center', va='center',
                fontweight='bold', fontsize=9, color='white')
        # Verification label
        ax.text(i, gm + vm / 2, f'{vm:.1f}ms', ha='center', va='center',
                fontweight='bold', fontsize=9, color='white')
        # Total label above
        total = gm + vm
        ax.text(i, total + max(verify_stds) * 0.3, f'Σ {total:.1f}ms', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Styling
    ax.set_ylabel('Time (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Cryptographic Mode', fontsize=12, fontweight='bold')
    
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title('Cryptographic Overhead Breakdown', fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(crypto_modes, fontsize=11)
    ax.legend(loc='upper left', fontsize=10)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.set_axisbelow(True)
    
    # Add insight text
    if len(crypto_modes) > 1:
        ecdsa_total = None
        pqc_totals = []
        
        for i, mode in enumerate(crypto_modes):
            total = gen_means[i] + verify_means[i]
            if 'ECDSA' in mode.upper():
                ecdsa_total = total
            else:
                pqc_totals.append((mode, total))
        
        if ecdsa_total and pqc_totals:
            insight_lines = ["PQC Overhead vs ECDSA:"]
            for mode, total in pqc_totals:
                overhead_pct = ((total - ecdsa_total) / ecdsa_total) * 100
                insight_lines.append(f"  {mode}: +{overhead_pct:.1f}%")
            
            insight_text = "\n".join(insight_lines)
            ax.text(0.98, 0.98, insight_text, transform=ax.transAxes,
                    fontsize=9, verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Overhead breakdown saved to: {output_path}")
    
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Generate Overhead Breakdown plot (stacked bar chart for crypto operations)'
    )
    parser.add_argument(
        '--csv',
        nargs='+',
        required=True,
        help='One or more CSV files with benchmark data'
    )
    parser.add_argument(
        '--output',
        default='/tmp/overhead_breakdown.png',
        help='Output path for plot (default: /tmp/overhead_breakdown.png)'
    )
    parser.add_argument(
        '--title',
        help='Custom plot title'
    )
    
    args = parser.parse_args()
    
    # Load and aggregate data
    print(f"Loading {len(args.csv)} CSV file(s)...")
    df = load_and_aggregate(args.csv)
    print(f"Aggregated data for {len(df)} crypto mode(s): {df['crypto_mode'].tolist()}")
    
    # Generate plot
    print("Generating overhead breakdown plot...")
    create_overhead_breakdown(df, args.output, args.title)
    
    print("Done!")


if __name__ == '__main__':
    main()
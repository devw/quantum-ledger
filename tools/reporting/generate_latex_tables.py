import argparse
import glob
import pandas as pd
from pathlib import Path


METRICS = [
    "tx_rate",
    "latency_avg",
    "latency_p95",
    "sig_gen_time",
    "sig_verify_time",
]


def load_csvs(patterns):
    frames = []
    for pattern in patterns:
        for path in glob.glob(pattern):
            frames.append(pd.read_csv(path))
    if not frames:
        raise ValueError("No CSV files found.")
    return pd.concat(frames, ignore_index=True)


def aggregate_stats(df):
    grouped = (
        df.groupby(["crypto_mode", "load_profile"])[METRICS]
        .agg(["mean", "std"])
        .reset_index()
    )
    return grouped


def format_mean_std(mean, std, precision=2):
    return f"{mean:.{precision}f} $\\pm$ {std:.{precision}f}"


def to_latex_table(df):
    rows = []

    for _, row in df.iterrows():
        # Fix: Access the scalar values directly from the first level
        crypto = row["crypto_mode"]
        load = row["load_profile"]
        
        # Convert to string if they're not already
        if isinstance(crypto, pd.Series):
            crypto = crypto.iloc[0]
        if isinstance(load, pd.Series):
            load = load.iloc[0]

        values = []
        for metric in METRICS:
            mean = row[(metric, "mean")]
            std = row[(metric, "std")]
            values.append(format_mean_std(mean, std))

        rows.append(
            " & ".join([str(crypto), str(load)] + values) + r" \\"
        )

    header = r"""
\begin{table*}[t]
\centering
\caption{Performance metrics aggregated over runs (mean $\pm$ standard deviation).}
\label{tab:crypto-performance}
\rowcolors{1}{white}{lightgray}
\begin{tabular}{llccccc}
\toprule
Crypto & Load &
Tx Rate &
Latency Avg &
Latency P95 &
Sig. Gen. Time &
Sig. Verif. Time \\
\midrule
""".strip()

    footer = r"""
\bottomrule
\end{tabular}
\end{table*}
""".strip()

    return "\n".join([header] + rows + [footer])


def main():
    parser = argparse.ArgumentParser(
        description="Generate LaTeX tables from PQC-Fabric benchmark CSVs"
    )
    parser.add_argument(
        "--csv",
        nargs="+",
        required=True,
        help="CSV file(s) or glob pattern(s)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="/tmp/performance_table.tex",
        help="Output LaTeX file path (default: /tmp/performance_table.tex)",
    )

    args = parser.parse_args()

    df = load_csvs(args.csv)
    stats = aggregate_stats(df)
    latex = to_latex_table(stats)

    # Write to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(latex)
    
    print(f"LaTeX table written to: {output_path}")


if __name__ == "__main__":
    main()
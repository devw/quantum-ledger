"""
CSV Utilities for PQC Benchmark Data

Contains reusable functions and the CSVExporter class for formatting,
quoting, and exporting benchmark data to CSV.
"""

import csv
import os
from pathlib import Path
from typing import Any, List, Dict


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def get_quoting_constant(quoting_str: str) -> int:
    """Map a string to csv.QUOTE_* constant."""
    mapping = {
        "minimal": csv.QUOTE_MINIMAL,
        "all": csv.QUOTE_ALL,
        "nonnumeric": csv.QUOTE_NONNUMERIC,
        "none": csv.QUOTE_NONE
    }
    return mapping.get(quoting_str.lower(), csv.QUOTE_MINIMAL)


def format_value(value: Any, decimal_precision: int = 3, column_name: str = None) -> str:
    """Format a value for CSV output with proper precision."""
    if isinstance(value, float):
        return f"{value:.{decimal_precision}f}"
    return str(value)


def generate_filename(
    crypto_mode: str,
    load_profile: str,
    run_number: int = 1,
    pattern: str = "{crypto_mode}_{load_profile}_RUN{run_number}.csv"
) -> str:
    """Generate CSV filename from pattern."""
    return pattern.format(
        crypto_mode=crypto_mode,
        load_profile=load_profile,
        run_number=run_number
    )


# ==============================================================================
# CSVExporter CLASS
# ==============================================================================

class CSVExporter:
    """Handles exporting benchmark data to CSV files using utility functions."""

    def __init__(self, config: Dict[str, Any], output_dir: str = None):
        self.config = config
        self.output_dir = output_dir or "."

        output_config = config.get("output", {})
        self.filename_pattern = output_config.get(
            "filename_pattern", "{crypto_mode}_{load_profile}_RUN{run_number}.csv"
        )
        self.decimal_precision = output_config.get("decimal_precision", 3)
        self.columns = output_config.get("columns", [])

        csv_options = output_config.get("csv_options", {})
        self.delimiter = csv_options.get("delimiter", ",")
        self.quoting = get_quoting_constant(csv_options.get("quoting", "minimal"))
        self.line_terminator = csv_options.get("line_terminator", "\n")
        self.encoding = csv_options.get("encoding", "utf-8")

    def generate_filename(self, crypto_mode: str, load_profile: str, run_number: int = 1) -> str:
        return generate_filename(
            crypto_mode, load_profile, run_number, pattern=self.filename_pattern
        )

    def ensure_output_directory(self) -> None:
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def format_value(self, value: Any, column_name: str = None) -> str:
        return format_value(value, decimal_precision=self.decimal_precision, column_name=column_name)

    def export_samples(self, samples: List[Dict[str, Any]], filename: str) -> str:
        if not samples:
            raise ValueError("Cannot export empty sample list")

        self.ensure_output_directory()
        filepath = os.path.join(self.output_dir, filename)

        sample_keys = set(samples[0].keys())
        if not set(self.columns).issubset(sample_keys):
            missing = set(self.columns) - sample_keys
            raise ValueError(f"Samples missing required columns: {missing}")

        with open(filepath, 'w', newline='', encoding=self.encoding) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.columns,
                delimiter=self.delimiter,
                quoting=self.quoting,
                lineterminator=self.line_terminator
            )
            writer.writeheader()
            for sample in samples:
                writer.writerow({col: self.format_value(sample[col], col) for col in self.columns})

        return filepath

    def export_run(self, samples: List[Dict[str, Any]], crypto_mode: str, load_profile: str, run_number: int = 1) -> str:
        return self.export_samples(samples, self.generate_filename(crypto_mode, load_profile, run_number))

    def export_multiple_runs(self, runs_data: Dict[str, List[Dict[str, Any]]], crypto_mode: str, load_profile: str) -> List[str]:
        created_files = []
        for run_id in sorted(runs_data.keys()):
            run_number = int(run_id.replace("RUN", ""))
            created_files.append(self.export_run(runs_data[run_id], crypto_mode, load_profile, run_number))
        return created_files

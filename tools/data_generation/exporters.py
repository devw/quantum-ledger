"""
CSV Exporters for PQC Benchmark Data

This module provides functions to export generated benchmark data to CSV files
following the specified format and naming conventions.

Version: 0.1.0 (MVP - Draft)
Strategy: Simple CSV writing with proper formatting and column ordering.
"""

import csv
import os
from typing import List, Dict, Any
from pathlib import Path


class CSVExporter:
    """
    Handles exporting benchmark data to CSV files.
    
    This class manages CSV file creation, formatting, and ensures proper
    column ordering according to the specification.
    
    Attributes:
        config: Configuration dictionary from config.yaml
        output_dir: Directory where CSV files will be saved
        decimal_precision: Number of decimal places for float values
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: str = None):
        """
        Initialize the CSV exporter.
        
        Args:
            config: Configuration dictionary from config.yaml
            output_dir: Output directory (if None, uses current directory)
        """
        self.config = config
        
        # Set output directory
        if output_dir is None:
            self.output_dir = "."
        else:
            self.output_dir = output_dir
        
        # Extract output configuration
        output_config = config.get("output", {})
        self.filename_pattern = output_config.get(
            "filename_pattern", 
            "{crypto_mode}_{load_profile}_RUN{run_number}.csv"
        )
        self.decimal_precision = output_config.get("decimal_precision", 3)
        self.columns = output_config.get("columns", [])
        
        # CSV formatting options
        csv_options = output_config.get("csv_options", {})
        self.delimiter = csv_options.get("delimiter", ",")
        self.quoting = self._get_quoting_constant(csv_options.get("quoting", "minimal"))
        self.line_terminator = csv_options.get("line_terminator", "\n")
        self.encoding = csv_options.get("encoding", "utf-8")
    
    def _get_quoting_constant(self, quoting_str: str) -> int:
        """
        Convert quoting string to csv.QUOTE_* constant.
        
        Args:
            quoting_str: "minimal", "all", "nonnumeric", or "none"
        
        Returns:
            Corresponding csv.QUOTE_* constant
        """
        quoting_map = {
            "minimal": csv.QUOTE_MINIMAL,
            "all": csv.QUOTE_ALL,
            "nonnumeric": csv.QUOTE_NONNUMERIC,
            "none": csv.QUOTE_NONE,
        }
        return quoting_map.get(quoting_str.lower(), csv.QUOTE_MINIMAL)
    
    def format_value(self, value: Any, column_name: str = None) -> str:
        """
        Format a value for CSV output with proper precision.
        
        Args:
            value: Value to format
            column_name: Name of the column (for special formatting rules)
        
        Returns:
            Formatted string representation
        """
        # Handle different types
        if isinstance(value, float):
            # Round to specified decimal precision
            return f"{value:.{self.decimal_precision}f}"
        elif isinstance(value, int):
            return str(value)
        else:
            # String values (crypto_mode, load_profile, run_id)
            return str(value)
    
    def generate_filename(
        self,
        crypto_mode: str,
        load_profile: str,
        run_number: int = 1
    ) -> str:
        """
        Generate filename according to naming convention.
        
        Args:
            crypto_mode: Crypto mode name (e.g., "ECDSA")
            load_profile: Load profile name (e.g., "LOWLOAD")
            run_number: Run number (e.g., 1, 2, 3)
        
        Returns:
            Filename string (e.g., "ECDSA_LOWLOAD_RUN1.csv")
        """
        return self.filename_pattern.format(
            crypto_mode=crypto_mode,
            load_profile=load_profile,
            run_number=run_number
        )
    
    def ensure_output_directory(self) -> None:
        """
        Create output directory if it doesn't exist.
        
        Raises:
            OSError: If directory cannot be created
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def export_samples(
        self,
        samples: List[Dict[str, Any]],
        filename: str
    ) -> str:
        """
        Export samples to a CSV file.
        
        Args:
            samples: List of sample dictionaries
            filename: Output filename
        
        Returns:
            Full path to the created CSV file
        
        Raises:
            ValueError: If samples is empty or columns don't match
            IOError: If file cannot be written
        """
        if not samples:
            raise ValueError("Cannot export empty sample list")
        
        # Ensure output directory exists
        self.ensure_output_directory()
        
        # Construct full file path
        filepath = os.path.join(self.output_dir, filename)
        
        # Validate that first sample has all required columns
        sample_keys = set(samples[0].keys())
        required_keys = set(self.columns)
        
        if not required_keys.issubset(sample_keys):
            missing = required_keys - sample_keys
            raise ValueError(f"Samples missing required columns: {missing}")
        
        # Write CSV file
        with open(filepath, 'w', newline='', encoding=self.encoding) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.columns,
                delimiter=self.delimiter,
                quoting=self.quoting,
                lineterminator=self.line_terminator
            )
            
            # Write header
            writer.writeheader()
            
            # Write rows with proper formatting
            for sample in samples:
                formatted_row = {}
                for col in self.columns:
                    formatted_row[col] = self.format_value(sample[col], col)
                writer.writerow(formatted_row)
        
        return filepath
    
    def export_run(
        self,
        samples: List[Dict[str, Any]],
        crypto_mode: str,
        load_profile: str,
        run_number: int = 1
    ) -> str:
        """
        Export a single run to CSV with automatic filename generation.
        
        Args:
            samples: List of sample dictionaries
            crypto_mode: Crypto mode name
            load_profile: Load profile name
            run_number: Run number
        
        Returns:
            Full path to the created CSV file
        """
        filename = self.generate_filename(crypto_mode, load_profile, run_number)
        return self.export_samples(samples, filename)
    
    def export_multiple_runs(
        self,
        runs_data: Dict[str, List[Dict[str, Any]]],
        crypto_mode: str,
        load_profile: str
    ) -> List[str]:
        """
        Export multiple runs to separate CSV files.
        
        Args:
            runs_data: Dictionary mapping run_id to sample lists
            crypto_mode: Crypto mode name
            load_profile: Load profile name
        
        Returns:
            List of created file paths
        
        Example:
            >>> runs_data = {"RUN1": samples1, "RUN2": samples2}
            >>> paths = exporter.export_multiple_runs(runs_data, "ECDSA", "LOWLOAD")
            >>> len(paths)
            2
        """
        created_files = []
        
        # Sort run_ids to ensure consistent ordering (RUN1, RUN2, RUN3, ...)
        sorted_run_ids = sorted(runs_data.keys())
        
        for run_id in sorted_run_ids:
            # Extract run number from run_id (e.g., "RUN1" -> 1)
            run_number = int(run_id.replace("RUN", ""))
            
            samples = runs_data[run_id]
            filepath = self.export_run(samples, crypto_mode, load_profile, run_number)
            created_files.append(filepath)
        
        return created_files


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def export_to_csv(
    samples: List[Dict[str, Any]],
    output_path: str,
    columns: List[str] = None,
    decimal_precision: int = 3
) -> None:
    """
    Quick utility function to export samples to CSV.
    
    This is a simplified interface for one-off exports without creating
    a CSVExporter instance.
    
    Args:
        samples: List of sample dictionaries
        output_path: Full path to output CSV file
        columns: List of column names (if None, uses all keys from first sample)
        decimal_precision: Number of decimal places for floats
    
    Example:
        >>> samples = [{"timestamp": 123.456, "tx_rate": 100.0, ...}]
        >>> export_to_csv(samples, "output.csv")
    """
    if not samples:
        raise ValueError("Cannot export empty sample list")
    
    # Determine columns
    if columns is None:
        columns = list(samples[0].keys())
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        
        for sample in samples:
            # Format float values
            formatted_sample = {}
            for key, value in sample.items():
                if key in columns:
                    if isinstance(value, float):
                        formatted_sample[key] = f"{value:.{decimal_precision}f}"
                    else:
                        formatted_sample[key] = value
            
            writer.writerow(formatted_sample)


def get_output_path(
    output_dir: str,
    crypto_mode: str,
    load_profile: str,
    run_number: int
) -> str:
    """
    Generate full output path for a CSV file.
    
    Args:
        output_dir: Output directory
        crypto_mode: Crypto mode name
        load_profile: Load profile name
        run_number: Run number
    
    Returns:
        Full file path
    """
    filename = f"{crypto_mode}_{load_profile}_RUN{run_number}.csv"
    return os.path.join(output_dir, filename)


def validate_csv_file(filepath: str, expected_columns: List[str]) -> bool:
    """
    Validate that a CSV file has the expected structure.
    
    Args:
        filepath: Path to CSV file to validate
        expected_columns: List of expected column names
    
    Returns:
        True if valid, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check header
            if reader.fieldnames != expected_columns:
                return False
            
            # Check at least one row exists
            first_row = next(reader, None)
            if first_row is None:
                return False
            
            return True
    
    except (FileNotFoundError, IOError, csv.Error):
        return False


# ==============================================================================
# MODULE METADATA
# ==============================================================================

__all__ = [
    "CSVExporter",
    "export_to_csv",
    "get_output_path",
    "validate_csv_file",
]
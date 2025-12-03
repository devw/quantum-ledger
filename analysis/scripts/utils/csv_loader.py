"""CSV loading utilities following Single Responsibility Principle."""

import pandas as pd
import sys
from pathlib import Path


class CSVLoader:
    """Responsible for loading and validating CSV files."""
    
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self._df = None
    
    def load(self) -> pd.DataFrame:
        """Load CSV file and return DataFrame."""
        try:
            self._df = pd.read_csv(self.csv_path)
            self._print_info()
            return self._df
        except FileNotFoundError:
            print(f"✗ Error: File not found: {self.csv_path}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            sys.exit(1)
    
    def _print_info(self):
        """Print basic information about loaded data."""
        print(f"✓ Loaded CSV: {self.csv_path}")
        print(f"  Shape: {self._df.shape}")
        print(f"  Columns: {list(self._df.columns)}")
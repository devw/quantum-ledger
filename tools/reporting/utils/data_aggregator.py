"""Data aggregation for multiple CSV files."""

import pandas as pd
from pathlib import Path
from typing import List, Dict
from .csv_loader import CSVLoader


class DataAggregator:
    """Aggregates data from multiple benchmark CSV files."""
    
    REQUIRED_COLUMNS = [
        'crypto_mode', 'load_profile', 'run_id'
    ]
    
    def __init__(self, csv_paths: List[str]):
        self.csv_paths = [Path(p) for p in csv_paths]
        self.df = None
    
    def load_all(self) -> pd.DataFrame:
        """Load and combine all CSV files."""
        dfs = []
        for path in self.csv_paths:
            loader = CSVLoader(str(path))
            df = loader.load()
            self._validate_schema(df, path)
            dfs.append(df)
        
        self.df = pd.concat(dfs, ignore_index=True)
        print(f"\n✓ Combined {len(dfs)} files")
        print(f"  Total rows: {len(self.df)}")
        return self.df
    
    def get_grouped_data(self, metric: str) -> Dict:
        """Group data by crypto_mode and load_profile."""
        if self.df is None:
            raise ValueError("No data loaded. Call load_all() first.")
        
        if metric not in self.df.columns:
            raise ValueError(f"Metric '{metric}' not found in data.")
        
        grouped = {}
        for crypto in self.df['crypto_mode'].unique():
            grouped[crypto] = {}
            crypto_df = self.df[self.df['crypto_mode'] == crypto]
            
            for load in crypto_df['load_profile'].unique():
                data = crypto_df[crypto_df['load_profile'] == load][metric]
                grouped[crypto][load] = data.tolist()
        
        return grouped
    
    def _validate_schema(self, df: pd.DataFrame, path: Path):
        """Validate CSV has required columns."""
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in {path.name}: {missing}")
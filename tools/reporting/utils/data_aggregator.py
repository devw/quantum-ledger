import pandas as pd
import numpy as np

class DataAggregator:
    """Aggregates data from multiple CSV files."""
    
    def __init__(self, csv_files):
        """Initialize with list of CSV file paths."""
        self.csv_files = csv_files
        self.dataframes = []
    
    def load_all(self):
        """Load all CSV files into dataframes."""
        for csv_file in self.csv_files:
            try:
                df = pd.read_csv(csv_file)
                self.dataframes.append(df)
                print(f"✓ Loaded: {csv_file} ({len(df)} rows)")
            except Exception as e:
                print(f"✗ Error loading {csv_file}: {e}")
    
    def get_grouped_data(self, metric):
        """Get data grouped by configuration for box plotting.
        
        Args:
            metric: Column name to extract
            
        Returns:
            Dictionary mapping group labels to numpy arrays of values
        """
        if not self.dataframes:
            raise ValueError("No data loaded. Call load_all() first.")
        
        # Concatenate all dataframes
        combined_df = pd.concat(self.dataframes, ignore_index=True)
        
        print(f"\n📊 Data Summary:")
        print(f"  Total rows: {len(combined_df)}")
        print(f"  Columns: {', '.join(combined_df.columns)}")
        
        # Check if metric exists
        if metric not in combined_df.columns:
            available = ', '.join(combined_df.columns)
            raise ValueError(f"Metric '{metric}' not found. Available: {available}")
        
        # Group by crypto_mode and load_profile
        grouped_data = {}
        
        # Check if grouping columns exist
        if 'crypto_mode' not in combined_df.columns:
            raise ValueError("Column 'crypto_mode' not found in data")
        if 'load_profile' not in combined_df.columns:
            raise ValueError("Column 'load_profile' not found in data")
        
        print(f"\n📈 Grouping by crypto_mode and load_profile:")
        
        for (crypto_mode, load_profile), group in combined_df.groupby(
            ['crypto_mode', 'load_profile'], dropna=False
        ):
            # Create label
            label = f"{crypto_mode}\n{load_profile}"
            
            # Extract metric values
            values = group[metric].values
            
            # Ensure it's a 1D array
            if values.ndim == 0:
                values = np.array([values])
            elif values.ndim > 1:
                values = values.flatten()
            
            # Convert to float and remove NaN
            values = values.astype(float)
            values = values[~np.isnan(values)]
            
            if len(values) > 0:
                grouped_data[label] = values
                print(f"  ✓ {label:30s}: {len(values):4d} values | "
                      f"mean={np.mean(values):8.2f} | "
                      f"std={np.std(values):8.2f}")
            else:
                print(f"  ⚠️  {label:30s}: No valid data")
        
        if not grouped_data:
            raise ValueError("No valid groups found after processing")
        
        return grouped_data
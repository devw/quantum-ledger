import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

class BoxPlotter:
    """Creates and saves box plots with configurable styling."""
    
    def __init__(self, config):
        """Initialize plotter with configuration."""
        self.config = config
        self.fig = None
        self.ax = None
    
    def create_plot(self, grouped_data, fontsize=14, title_fontsize=16):
        """Create box plot from grouped data with custom font sizes.
        
        Args:
            grouped_data: Dictionary mapping group names to data arrays
            fontsize: Font size for axis labels and ticks (default: 14)
            title_fontsize: Font size for plot title (default: 16)
        """
        # Validate input data
        if not grouped_data:
            raise ValueError("No data provided for plotting")
        
        # Set global font size
        matplotlib.rcParams.update({
            'font.size': fontsize,
            'axes.labelsize': fontsize,
            'axes.titlesize': title_fontsize,
            'xtick.labelsize': fontsize,
            'ytick.labelsize': fontsize,
            'legend.fontsize': fontsize,
            'figure.titlesize': title_fontsize
        })
        
        # Create figure with larger size for better readability
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        
        # Prepare data - ensure we have numpy arrays
        labels = []
        data = []
        
        for label, values in grouped_data.items():
            # Convert to numpy array if needed
            if not isinstance(values, np.ndarray):
                values = np.array(values)
            
            # Handle scalar values
            if values.ndim == 0:
                print(f"⚠️ Warning: '{label}' contains a scalar value: {values}")
                print(f"   Converting to single-element array")
                values = np.array([float(values)])
            
            # Flatten if multi-dimensional
            if values.ndim > 1:
                values = values.flatten()
            
            # Validate data type
            if values.dtype == 'object':
                print(f"✗ Error: Data for '{label}' contains non-numeric values")
                if len(values) > 0:
                    print(f"  Sample values: {values[:min(5, len(values))]}")
                raise TypeError(f"Non-numeric data in group '{label}'")
            
            # Remove NaN values
            values = values[~np.isnan(values)]
            
            if len(values) == 0:
                print(f"⚠️ Warning: No valid data for '{label}', skipping")
                continue
            
            data.append(values)
            labels.append(label)
            print(f"  ✓ {label}: {len(values)} values, range [{values.min():.2f}, {values.max():.2f}]")
        
        if not data:
            raise ValueError("No valid data to plot after filtering")
        
        # Color palette for different crypto modes
        colors = {
            'ECDSA': '#90EE90',      # Light green
            'DILITHIUM3': '#FFB6C6', # Light red/pink
            'HYBRID': '#87CEEB'      # Light blue
        }
        
        # Assign colors based on label
        box_colors = []
        for label in labels:
            if 'ECDSA' in label:
                box_colors.append(colors['ECDSA'])
            elif 'DILITHIUM3' in label:
                box_colors.append(colors['DILITHIUM3'])
            elif 'HYBRID' in label:
                box_colors.append(colors['HYBRID'])
            else:
                box_colors.append('lightblue')
        
        # Create box plot
        bp = self.ax.boxplot(
            data,
            labels=labels,
            patch_artist=True,
            showmeans=True,
            meanprops=dict(marker='D', markerfacecolor='red', markersize=8, 
                          markeredgecolor='darkred', markeredgewidth=1),
            boxprops=dict(alpha=0.7, linewidth=1.5),
            medianprops=dict(color='black', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5),
            flierprops=dict(marker='o', markerfacecolor='gray', markersize=6, 
                          alpha=0.5, markeredgecolor='none')
        )
        
        # Apply colors to boxes
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
        
        # Apply configuration
        self.ax.set_title(self.config.title, fontsize=title_fontsize, 
                         fontweight='bold', pad=20)
        self.ax.set_ylabel(self.config.ylabel, fontsize=fontsize, fontweight='bold')
        self.ax.set_xlabel(self.config.xlabel, fontsize=fontsize, fontweight='bold')
        
        # Rotate x-axis labels if needed
        if len(labels) > 3:
            plt.xticks(rotation=45, ha='right')
        
        # Add grid for better readability
        self.ax.yaxis.grid(True, linestyle='--', alpha=0.3, linewidth=0.8)
        self.ax.set_axisbelow(True)
        
        # Add light background
        self.ax.set_facecolor('#F8F8F8')
        
        # Tight layout to prevent label cutoff
        plt.tight_layout()
    
    def save(self, output_path, dpi=300):
        """Save plot to file with high DPI.
        
        Args:
            output_path: Path object or string for output file
            dpi: Dots per inch for output resolution (default: 300)
        """
        if self.fig is None:
            raise RuntimeError("No plot created yet. Call create_plot() first.")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.fig.savefig(
            output_path, 
            dpi=dpi, 
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )
        print(f"✓ Plot saved: {output_path}")
        plt.close(self.fig)
"""Box plot rendering using matplotlib."""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict
from pathlib import Path
from .plot_config import BoxPlotConfig


class BoxPlotter:
    """Creates box plots with customizable configuration."""
    
    def __init__(self, config: BoxPlotConfig):
        self.config = config
        self.fig = None
        self.ax = None
    
    def create_plot(self, grouped_data: Dict) -> plt.Figure:
        """Create box plot from grouped data."""
        self.fig, self.ax = plt.subplots(figsize=self.config.figsize)
        
        positions, labels, data_list, colors = self._prepare_data(grouped_data)
        
        # Create box plots
        bp = self.ax.boxplot(
            data_list,
            positions=positions,
            widths=self.config.box_width,
            patch_artist=True,
            showmeans=self.config.show_means,
            meanprops=dict(marker='D', markerfacecolor='red', markersize=6)
        )
        
        # Apply colors
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        self._configure_axes(positions, labels)
        
        return self.fig
    
    def _prepare_data(self, grouped_data: Dict):
        """Prepare data for plotting."""
        positions, labels, data_list, colors = [], [], [], []
        pos = 1
        
        for crypto, load_data in sorted(grouped_data.items()):
            for load_profile, values in sorted(load_data.items()):
                positions.append(pos)
                labels.append(f"{crypto}\n{load_profile}")
                data_list.append(values)
                colors.append(self.config.get_color(crypto))
                pos += 1
        
        return positions, labels, data_list, colors
    
    def _configure_axes(self, positions, labels):
        """Configure plot axes and styling."""
        self.ax.set_xticks(positions)
        self.ax.set_xticklabels(labels, fontsize=self.config.font_size_ticks)
        
        self.ax.set_title(self.config.title, fontsize=self.config.font_size_title, pad=20)
        self.ax.set_xlabel(self.config.xlabel, fontsize=self.config.font_size_labels)
        self.ax.set_ylabel(self.config.ylabel, fontsize=self.config.font_size_labels)
        
        if self.config.show_grid:
            self.ax.grid(axis='y', alpha=self.config.grid_alpha, linestyle='--')
        
        plt.tight_layout()
    
    def save(self, output_path: Path):
        """Save plot to file."""
        if self.fig is None:
            raise ValueError("No plot created. Call create_plot() first.")
        
        self.fig.savefig(output_path, dpi=self.config.dpi, bbox_inches='tight')
        print(f"✓ Plot saved: {output_path}")
        plt.close(self.fig)
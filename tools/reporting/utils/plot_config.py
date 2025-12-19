"""Plot configuration following Open/Closed Principle."""

from dataclasses import dataclass, field
from typing import Tuple, Dict


@dataclass
class BoxPlotConfig:
    """Configuration for box plot visualization."""
    
    figsize: Tuple[int, int] = (14, 8)
    
    colors: Dict[str, str] = field(default_factory=lambda: {
        'ECDSA': '#2ecc71',      # Green
        'DILITHIUM3': '#e74c3c',  # Red  
        'HYBRID': '#3498db'       # Blue
    })
    
    title: str = "Performance Comparison"
    xlabel: str = "Configuration"
    ylabel: str = "Value"
    
    show_means: bool = True
    show_grid: bool = True
    grid_alpha: float = 0.3
    
    box_width: float = 0.6
    font_size_title: int = 16
    font_size_labels: int = 12
    font_size_ticks: int = 10
    
    dpi: int = 300
    
    def get_color(self, crypto_mode: str) -> str:
        """Get color for specific crypto mode."""
        return self.colors.get(crypto_mode, '#95a5a6')  # Gray default


def create_metric_config(metric: str) -> BoxPlotConfig:
    """Create configuration based on metric type."""
    
    metric_labels = {
        'latency_avg': ('Avg Latency Comparison', 'Configuration', 'Latency (ms)'),
        'latency_p95': ('P95 Latency Comparison', 'Configuration', 'Latency (ms)'),
        'tx_rate': ('Transaction Rate Comparison', 'Configuration', 'Tx/sec'),
        'sig_gen_time': ('Signature Generation Time', 'Configuration', 'Time (ms)'),
        'sig_verify_time': ('Signature Verification Time', 'Configuration', 'Time (ms)'),
        'cpu_util': ('CPU Utilization', 'Configuration', 'Usage (%)'),
        'mem_util': ('Memory Utilization', 'Configuration', 'Usage (%)'),
    }
    
    title, xlabel, ylabel = metric_labels.get(
        metric, 
        ('Performance Metric', 'Configuration', 'Value')
    )
    
    return BoxPlotConfig(title=title, xlabel=xlabel, ylabel=ylabel)
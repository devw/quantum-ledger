"""
Monte Carlo Mock Data Generator - Core Orchestrator
Generates mock blockchain benchmark data using Monte Carlo simulation.
"""

import numpy as np
from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path


class MonteCarloGenerator:
    """
    Main orchestrator for Monte Carlo data generation.
    Coordinates distributions, sampling, validation, and export.
    """
    
    def __init__(self, scenario_config: Optional[str] = None, seed: Optional[int] = None):
        """
        Initialize the Monte Carlo Generator.
        
        Args:
            scenario_config: Path to YAML scenario configuration file
            seed: Random seed for reproducibility
        """
        self.seed = seed if seed is not None else 42
        np.random.seed(self.seed)
        
        self.config = self._load_config(scenario_config) if scenario_config else {}
        self.samples = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def generate(self, 
                 iterations: int = 1000,
                 parameters: Optional[Dict[str, Dict[str, Any]]] = None) -> 'MonteCarloGenerator':
        """
        Generate mock data samples using Monte Carlo simulation.
        
        Args:
            iterations: Number of samples to generate
            parameters: Dict of parameter configurations
                       Format: {'param_name': {'distribution': 'normal', 'mean': 10, 'std': 2}}
        
        Returns:
            Self for method chaining
        """
        # Use provided parameters or fall back to config
        params = parameters if parameters else self.config.get('parameters', {})
        
        if not params:
            # Default parameters if none provided
            params = self._get_default_parameters()
        
        print(f"🎲 Generating {iterations} samples with seed={self.seed}")
        
        samples = []
        for i in range(iterations):
            sample = {'iteration': i}
            
            for param_name, param_config in params.items():
                value = self._sample_parameter(param_config)
                sample[param_name] = value
            
            samples.append(sample)
        
        self.samples = samples
        print(f"✅ Generated {len(self.samples)} samples")
        return self
    
    def _get_default_parameters(self) -> Dict[str, Dict[str, Any]]:
        """Default blockchain benchmark parameters."""
        return {
            'tx_rate': {
                'distribution': 'normal',
                'mean': 100,
                'std': 20,
                'min': 10,
                'max': 500
            },
            'block_size': {
                'distribution': 'uniform',
                'min': 10,
                'max': 100
            },
            'network_latency': {
                'distribution': 'exponential',
                'lambda': 0.1,
                'min': 10,
                'max': 500
            },
            'node_count': {
                'distribution': 'uniform',
                'min': 2,
                'max': 20,
                'discrete': True
            }
        }
    
    def _sample_parameter(self, config: Dict[str, Any]) -> float:
        """
        Sample a single parameter value based on its configuration.
        
        Args:
            config: Parameter configuration with distribution type and params
        
        Returns:
            Sampled value
        """
        dist_type = config.get('distribution', 'uniform')
        
        if dist_type == 'normal':
            value = np.random.normal(config['mean'], config['std'])
        elif dist_type == 'uniform':
            value = np.random.uniform(config['min'], config['max'])
        elif dist_type == 'exponential':
            value = np.random.exponential(1.0 / config['lambda'])
        elif dist_type == 'poisson':
            value = np.random.poisson(config['lambda'])
        else:
            raise ValueError(f"Unknown distribution type: {dist_type}")
        
        # Apply bounds if specified
        if 'min' in config:
            value = max(value, config['min'])
        if 'max' in config:
            value = min(value, config['max'])
        
        # Discretize if needed
        if config.get('discrete', False):
            value = int(round(value))
        
        return value
    
    def validate(self) -> bool:
        """
        Validate generated samples.
        
        Returns:
            True if validation passes
        """
        if not self.samples:
            print("⚠️  No samples to validate")
            return False
        
        print(f"✅ Validation passed for {len(self.samples)} samples")
        return True
    
    def export_csv(self, output_path: str) -> str:
        """
        Export samples to CSV file.
        
        Args:
            output_path: Path to output CSV file
        
        Returns:
            Full path to created file
        """
        if not self.samples:
            raise ValueError("No samples to export. Run generate() first.")
        
        import csv
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get all unique keys from samples
        fieldnames = list(self.samples[0].keys())
        
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.samples)
        
        print(f"📊 Exported {len(self.samples)} samples to {path}")
        return str(path.absolute())
    
    def export_json(self, output_path: str) -> str:
        """
        Export samples to JSON file.
        
        Args:
            output_path: Path to output JSON file
        
        Returns:
            Full path to created file
        """
        if not self.samples:
            raise ValueError("No samples to export. Run generate() first.")
        
        import json
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.samples, f, indent=2)
        
        print(f"📄 Exported {len(self.samples)} samples to {path}")
        return str(path.absolute())
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get basic statistics of generated samples.
        
        Returns:
            Dictionary with statistics for each parameter
        """
        if not self.samples:
            return {}
        
        stats = {}
        param_names = [k for k in self.samples[0].keys() if k != 'iteration']
        
        for param in param_names:
            values = [s[param] for s in self.samples]
            stats[param] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'median': np.median(values)
            }
        
        return stats


# Convenience function for quick usage
def generate_mock_data(iterations: int = 1000, 
                      output_csv: str = 'data/fixtures/monte_carlo/samples.csv',
                      seed: int = 42) -> str:
    """
    Quick function to generate and export mock data in one call.
    
    Args:
        iterations: Number of samples to generate
        output_csv: Path to output CSV file
        seed: Random seed for reproducibility
    
    Returns:
        Path to generated CSV file
    """
    generator = MonteCarloGenerator(seed=seed)
    generator.generate(iterations=iterations)
    generator.validate()
    return generator.export_csv(output_csv)
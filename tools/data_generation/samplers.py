"""
Data Samplers for PQC Benchmark Data Generation

This module provides classes for generating complete data samples (rows) with
all required metrics. Each sampler combines multiple distribution functions to
produce realistic, correlated data points.

Version: 0.1.0 (MVP - Draft)
Strategy: Generate one complete row at a time with basic parameter passing.
         Advanced correlations will be added in refinement phase.
"""

from typing import Dict, Any, List
from . import distributions


class BenchmarkSampler:
    """
    Generates complete benchmark data samples for PQC Hyperledger Fabric.
    
    This class orchestrates the generation of all metrics for a single data point,
    ensuring consistency between related metrics (e.g., latency_p95 > latency_avg).
    
    Attributes:
        config: Full configuration dictionary from config.yaml
        crypto_mode_name: Name of crypto mode (ECDSA, DILITHIUM3, HYBRID)
        load_profile_name: Name of load profile (LOWLOAD, MEDIUMLOAD, etc.)
        run_id: Run identifier (e.g., "RUN1", "RUN2")
        start_timestamp: Starting Unix epoch timestamp
    """
    
    def __init__(
        self,
        config: Dict[str, Any],
        crypto_mode_name: str,
        load_profile_name: str,
        run_id: str,
        start_timestamp: float = None
    ):
        """
        Initialize the sampler with configuration and experiment parameters.
        
        Args:
            config: Configuration dictionary from config.yaml
            crypto_mode_name: "ECDSA", "DILITHIUM3", or "HYBRID"
            load_profile_name: "LOWLOAD", "MEDIUMLOAD", "HIGHLOAD", or "SUSTAINED"
            run_id: Run identifier (e.g., "RUN1")
            start_timestamp: Starting timestamp (if None, uses config default)
        
        Raises:
            KeyError: If crypto_mode_name or load_profile_name not in config
        """
        self.config = config
        self.crypto_mode_name = crypto_mode_name
        self.load_profile_name = load_profile_name
        self.run_id = run_id
        
        # Extract crypto mode and load profile configurations
        self.crypto_mode = config["crypto_modes"][crypto_mode_name]
        self.load_profile = config["load_profiles"][load_profile_name]
        
        # Extract performance factors
        self.crypto_performance_factor = self.crypto_mode["performance_factor"]
        self.crypto_latency_overhead = self.crypto_mode["latency_overhead"]
        self.crypto_cpu_overhead = self.crypto_mode["cpu_overhead"]
        
        # Timestamp configuration
        if start_timestamp is None:
            self.start_timestamp = config["sampling"]["start_timestamp"]
        else:
            self.start_timestamp = start_timestamp
        
        self.sampling_interval = config["sampling"]["interval"]
        
        # Metric configuration
        self.metrics_config = config["metrics"]
    
    def generate_sample(self, sample_index: int) -> Dict[str, Any]:
        """
        Generate a complete data sample (one CSV row).
        
        This method generates all 13 metrics for a single time point, ensuring
        proper relationships between dependent variables.
        
        Args:
            sample_index: Index of the sample (0, 1, 2, ...) for timestamp calculation
        
        Returns:
            Dictionary with all column values for one CSV row
            
        Example:
            >>> sampler = BenchmarkSampler(config, "ECDSA", "LOWLOAD", "RUN1")
            >>> row = sampler.generate_sample(0)
            >>> row.keys()
            dict_keys(['timestamp', 'crypto_mode', 'load_profile', 'run_id', 'tx_rate', ...])
        """
        # Generate timestamp
        timestamp = distributions.generate_timestamp(
            self.start_timestamp, 
            sample_index, 
            self.sampling_interval
        )
        
        # Generate transaction rate
        tx_rate = distributions.generate_tx_rate(
            self.load_profile,
            self.crypto_performance_factor
        )
        
        # Generate latency metrics (dependent on tx_rate and crypto mode)
        latency_avg = distributions.generate_latency_avg(
            self.load_profile,
            self.crypto_latency_overhead,
            tx_rate
        )
        
        latency_p95_config = self.metrics_config["latency_p95"]
        latency_p95 = distributions.generate_latency_p95(
            latency_avg,
            latency_p95_config["multiplier_mean"],
            latency_p95_config["multiplier_std"]
        )
        
        # Generate resource utilization
        cpu_util = distributions.generate_cpu_util(
            self.load_profile,
            self.crypto_cpu_overhead,
            tx_rate
        )
        
        mem_util_config = self.metrics_config["mem_util"]
        mem_util = distributions.generate_mem_util(
            self.load_profile,
            tx_rate,
            mem_util_config["tx_rate_sensitivity"]
        )
        
        # Generate block metrics
        block_size_config = self.metrics_config["block_size"]
        block_size = distributions.generate_block_size(
            tx_rate,
            block_size_config["base"],
            block_size_config["tx_rate_factor"]
        )
        
        block_commit_config = self.metrics_config["block_commit_time"]
        block_commit_time = distributions.generate_block_commit_time(
            block_size,
            block_commit_config["crypto_overhead_factor"],
            block_commit_config["base"],
            block_commit_config["block_size_sensitivity"]
        )
        
        # Generate cryptographic timing metrics
        sig_gen_time = distributions.generate_sig_gen_time(self.crypto_mode)
        sig_verify_time = distributions.generate_sig_verify_time(self.crypto_mode)
        
        # Assemble complete sample
        sample = {
            "timestamp": timestamp,
            "crypto_mode": self.crypto_mode_name,
            "load_profile": self.load_profile_name,
            "run_id": self.run_id,
            "tx_rate": tx_rate,
            "latency_avg": latency_avg,
            "latency_p95": latency_p95,
            "cpu_util": cpu_util,
            "mem_util": mem_util,
            "block_size": block_size,
            "block_commit_time": block_commit_time,
            "sig_gen_time": sig_gen_time,
            "sig_verify_time": sig_verify_time,
        }
        
        return sample
    
    def generate_samples(self, num_samples: int) -> List[Dict[str, Any]]:
        """
        Generate multiple data samples (multiple CSV rows).
        
        Args:
            num_samples: Number of samples to generate
        
        Returns:
            List of sample dictionaries
            
        Example:
            >>> sampler = BenchmarkSampler(config, "ECDSA", "LOWLOAD", "RUN1")
            >>> samples = sampler.generate_samples(300)  # 5 minutes at 1 sample/sec
            >>> len(samples)
            300
        """
        samples = []
        for i in range(num_samples):
            sample = self.generate_sample(i)
            samples.append(sample)
        
        return samples
    
    def get_column_order(self) -> List[str]:
        """
        Get the correct column order from config.
        
        Returns:
            List of column names in correct order
        """
        return self.config["output"]["columns"]
    
    def validate_sample(self, sample: Dict[str, Any]) -> bool:
        """
        Validate that a sample meets basic consistency requirements.
        
        Args:
            sample: Sample dictionary to validate
        
        Returns:
            True if sample is valid, False otherwise
            
        Validation checks:
            - latency_p95 > latency_avg
            - cpu_util in [0, 100]
            - mem_util in [0, 100]
            - All required columns present
        """
        try:
            # Check latency percentile ordering
            if sample["latency_p95"] <= sample["latency_avg"]:
                return False
            
            # Check resource utilization bounds
            if not (0 <= sample["cpu_util"] <= 100):
                return False
            if not (0 <= sample["mem_util"] <= 100):
                return False
            
            # Check all columns present
            required_columns = self.get_column_order()
            for col in required_columns:
                if col not in sample:
                    return False
            
            return True
        
        except (KeyError, TypeError):
            return False


class MultiRunSampler:
    """
    Generates data for multiple runs of the same experiment configuration.
    
    This is a convenience wrapper around BenchmarkSampler for generating
    multiple runs (e.g., RUN1, RUN2, RUN3) with the same crypto mode and
    load profile but different random seeds.
    """
    
    def __init__(
        self,
        config: Dict[str, Any],
        crypto_mode_name: str,
        load_profile_name: str,
        num_runs: int = 3
    ):
        """
        Initialize multi-run sampler.
        
        Args:
            config: Configuration dictionary
            crypto_mode_name: Crypto mode name
            load_profile_name: Load profile name
            num_runs: Number of runs to generate (default: 3)
        """
        self.config = config
        self.crypto_mode_name = crypto_mode_name
        self.load_profile_name = load_profile_name
        self.num_runs = num_runs
    
    def generate_run(self, run_number: int, num_samples: int) -> List[Dict[str, Any]]:
        """
        Generate samples for a single run.
        
        Args:
            run_number: Run number (1, 2, 3, ...)
            num_samples: Number of samples per run
        
        Returns:
            List of samples for this run
        """
        run_id = f"RUN{run_number}"
        
        # Create sampler for this run
        sampler = BenchmarkSampler(
            self.config,
            self.crypto_mode_name,
            self.load_profile_name,
            run_id
        )
        
        # Generate samples
        return sampler.generate_samples(num_samples)
    
    def generate_all_runs(self, num_samples_per_run: int) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate samples for all runs.
        
        Args:
            num_samples_per_run: Number of samples per run
        
        Returns:
            Dictionary mapping run_id to list of samples
            
        Example:
            >>> multi_sampler = MultiRunSampler(config, "ECDSA", "LOWLOAD", num_runs=3)
            >>> all_data = multi_sampler.generate_all_runs(300)
            >>> all_data.keys()
            dict_keys(['RUN1', 'RUN2', 'RUN3'])
        """
        all_runs = {}
        
        for run_num in range(1, self.num_runs + 1):
            run_id = f"RUN{run_num}"
            samples = self.generate_run(run_num, num_samples_per_run)
            all_runs[run_id] = samples
        
        return all_runs


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def create_sampler_from_config(
    config: Dict[str, Any],
    crypto_mode: str,
    load_profile: str,
    run_id: str = "RUN1"
) -> BenchmarkSampler:
    """
    Factory function to create a BenchmarkSampler from config.
    
    Args:
        config: Configuration dictionary
        crypto_mode: Crypto mode name
        load_profile: Load profile name
        run_id: Run identifier
    
    Returns:
        Configured BenchmarkSampler instance
    """
    return BenchmarkSampler(config, crypto_mode, load_profile, run_id)


# ==============================================================================
# MODULE METADATA
# ==============================================================================

__all__ = [
    "BenchmarkSampler",
    "MultiRunSampler",
    "create_sampler_from_config",
]
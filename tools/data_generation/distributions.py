"""
Statistical Distributions for PQC Benchmark Data Generation

This module provides functions to generate realistic values for performance metrics
using statistical distributions. Each function generates values within specified
ranges and follows expected patterns from the config.yaml specification.

Version: 0.1.0 (MVP - Draft)
Strategy: Simple random generation with basic constraints.
         Correlations will be added in refinement phase.
"""

import random
from typing import Dict, Any


def generate_tx_rate(load_profile: Dict[str, Any], crypto_performance_factor: float = 1.0) -> float:
    """
    Generate transaction rate (TPS) for a given load profile.
    
    Args:
        load_profile: Load profile configuration from config.yaml
        crypto_performance_factor: Performance multiplier for crypto mode (default: 1.0 for ECDSA)
        
    Returns:
        Transaction rate in TPS (Transactions Per Second)
        
    Example:
        >>> profile = {"target_tps": 100, "variance": 0.1, "min_tps": 50, "max_tps": 150}
        >>> tx_rate = generate_tx_rate(profile, crypto_performance_factor=0.7)
        >>> 50 <= tx_rate <= 150
        True
    """
    target = load_profile["target_tps"] * crypto_performance_factor
    variance = load_profile["variance"]
    
    # Generate value with normal distribution around target
    value = random.gauss(target, target * variance)
    
    # Clamp to min/max bounds
    min_tps = load_profile["min_tps"]
    max_tps = load_profile["max_tps"]
    
    return max(min_tps, min(max_tps, value))


def generate_latency_avg(
    load_profile: Dict[str, Any],
    crypto_latency_overhead: float,
    tx_rate: float
) -> float:
    """
    Generate average latency based on load profile and crypto mode.
    
    Args:
        load_profile: Load profile configuration
        crypto_latency_overhead: Latency multiplier from crypto mode (e.g., 1.8 for DILITHIUM3)
        tx_rate: Current transaction rate (for future correlation refinement)
        
    Returns:
        Average latency in milliseconds
        
    Note:
        MVP version uses simple multiplication. Future refinement will add
        inverse correlation with tx_rate (higher load = higher latency).
    """
    base_latency = load_profile["latency_base"]
    variance = load_profile.get("latency_variance", 0.1)
    
    # Apply crypto overhead
    mean_latency = base_latency * crypto_latency_overhead
    
    # Add random variation
    value = random.gauss(mean_latency, mean_latency * variance)
    
    # Ensure positive and reasonable
    return max(10.0, value)


def generate_latency_p95(latency_avg: float, multiplier_mean: float = 2.0, multiplier_std: float = 0.25) -> float:
    """
    Generate 95th percentile latency based on average latency.
    
    Args:
        latency_avg: Average latency in milliseconds
        multiplier_mean: Mean multiplier for p95 (default: 2.0)
        multiplier_std: Standard deviation of multiplier (default: 0.25)
        
    Returns:
        P95 latency in milliseconds (guaranteed > latency_avg)
        
    Validation:
        Ensures latency_p95 >= latency_avg * 1.5 (from config validation rules)
    """
    # Generate multiplier with some variance
    multiplier = random.gauss(multiplier_mean, multiplier_std)
    
    # Clamp multiplier to validation rules (1.5x to 2.5x)
    multiplier = max(1.5, min(2.5, multiplier))
    
    return latency_avg * multiplier


def generate_cpu_util(
    load_profile: Dict[str, Any],
    crypto_cpu_overhead: float,
    tx_rate: float
) -> float:
    """
    Generate CPU utilization percentage.
    
    Args:
        load_profile: Load profile configuration
        crypto_cpu_overhead: CPU multiplier from crypto mode
        tx_rate: Current transaction rate
        
    Returns:
        CPU utilization as percentage (0-100)
    """
    base_cpu = load_profile["cpu_base"]
    
    # Apply crypto overhead
    mean_cpu = base_cpu * crypto_cpu_overhead
    
    # Add noise
    noise_std = 3.0  # ±3% from config
    value = random.gauss(mean_cpu, noise_std)
    
    # Clamp to valid percentage range
    return max(20.0, min(95.0, value))


def generate_mem_util(
    load_profile: Dict[str, Any],
    tx_rate: float,
    tx_rate_sensitivity: float = 0.04
) -> float:
    """
    Generate memory utilization percentage.
    
    Args:
        load_profile: Load profile configuration
        tx_rate: Current transaction rate
        tx_rate_sensitivity: Memory increase per 100 TPS (default: 0.04 = 4%)
        
    Returns:
        Memory utilization as percentage (0-100)
    """
    base_mem = load_profile["mem_base"]
    
    # Memory increases with transaction rate
    tx_factor = (tx_rate / 100.0) * tx_rate_sensitivity * 100
    mean_mem = base_mem + tx_factor
    
    # Add noise
    noise_std = 2.0  # ±2% from config
    value = random.gauss(mean_mem, noise_std)
    
    # Clamp to valid range
    return max(30.0, min(80.0, value))


def generate_block_size(tx_rate: float, base: int = 1024, tx_rate_factor: float = 1.5) -> int:
    """
    Generate block size in bytes.
    
    Args:
        tx_rate: Current transaction rate
        base: Base block size in bytes (default: 1024)
        tx_rate_factor: Scaling factor for tx_rate impact
        
    Returns:
        Block size in bytes
        
    Note:
        Higher tx_rate leads to larger blocks due to batching.
    """
    # Block size increases with transaction rate
    mean_size = base + (tx_rate / 100.0) * tx_rate_factor * 100
    
    # Add noise
    noise_std = 50.0  # ±50 bytes
    value = random.gauss(mean_size, noise_std)
    
    # Clamp to valid range and convert to integer
    return int(max(500, min(2500, value)))


def generate_block_commit_time(
    block_size: int,
    crypto_overhead_factor: float,
    base: float = 50.0,
    block_size_sensitivity: float = 0.08
) -> float:
    """
    Generate block commit time in milliseconds.
    
    Args:
        block_size: Block size in bytes
        crypto_overhead_factor: Overhead from crypto operations
        base: Base commit time in ms (default: 50.0)
        block_size_sensitivity: Time increase per KB (default: 0.08ms/KB)
        
    Returns:
        Block commit time in milliseconds
    """
    # Commit time increases with block size
    block_kb = block_size / 1024.0
    mean_time = base + (block_kb * block_size_sensitivity * 1000) + (crypto_overhead_factor * 10)
    
    # Add noise
    noise_std = 5.0  # ±5ms
    value = random.gauss(mean_time, noise_std)
    
    # Clamp to valid range
    return max(30.0, min(200.0, value))


def generate_sig_gen_time(crypto_mode: Dict[str, Any]) -> float:
    """
    Generate signature generation time in microseconds.
    
    Args:
        crypto_mode: Crypto mode configuration from config.yaml
        
    Returns:
        Signature generation time in microseconds (μs)
        
    Example:
        For ECDSA: ~100μs (50-150μs range)
        For DILITHIUM3: ~350μs (200-500μs range)
    """
    sig_gen_config = crypto_mode["sig_gen_time"]
    mean = sig_gen_config["mean"]
    std = sig_gen_config["std"]
    min_val = sig_gen_config["min"]
    max_val = sig_gen_config["max"]
    
    value = random.gauss(mean, std)
    
    return max(min_val, min(max_val, value))


def generate_sig_verify_time(crypto_mode: Dict[str, Any]) -> float:
    """
    Generate signature verification time in microseconds.
    
    Args:
        crypto_mode: Crypto mode configuration from config.yaml
        
    Returns:
        Signature verification time in microseconds (μs)
        
    Example:
        For ECDSA: ~180μs (100-250μs range)
        For DILITHIUM3: ~1100μs (800-1500μs range)
    """
    sig_verify_config = crypto_mode["sig_verify_time"]
    mean = sig_verify_config["mean"]
    std = sig_verify_config["std"]
    min_val = sig_verify_config["min"]
    max_val = sig_verify_config["max"]
    
    value = random.gauss(mean, std)
    
    return max(min_val, min(max_val, value))


def generate_timestamp(start_timestamp: float, sample_index: int, interval: float = 1.0) -> float:
    """
    Generate monotonically increasing timestamp.
    
    Args:
        start_timestamp: Starting Unix epoch timestamp
        sample_index: Index of current sample (0, 1, 2, ...)
        interval: Seconds between samples (default: 1.0)
        
    Returns:
        Unix epoch timestamp (float)
        
    Example:
        >>> generate_timestamp(1735920000.0, 0)
        1735920000.0
        >>> generate_timestamp(1735920000.0, 5)
        1735920005.0
    """
    return start_timestamp + (sample_index * interval)


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def validate_range(value: float, min_val: float, max_val: float, metric_name: str = "value") -> None:
    """
    Validate that a value is within expected range.
    
    Args:
        value: Value to validate
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
        metric_name: Name of metric for error messages
        
    Raises:
        ValueError: If value is outside range
    """
    if not (min_val <= value <= max_val):
        raise ValueError(f"{metric_name} = {value:.2f} is outside range [{min_val}, {max_val}]")


def set_random_seed(seed: int = None) -> None:
    """
    Set random seed for reproducibility.
    
    Args:
        seed: Random seed (None = truly random)
    """
    if seed is not None:
        random.seed(seed)


# ==============================================================================
# MODULE METADATA
# ==============================================================================

__all__ = [
    "generate_tx_rate",
    "generate_latency_avg",
    "generate_latency_p95",
    "generate_cpu_util",
    "generate_mem_util",
    "generate_block_size",
    "generate_block_commit_time",
    "generate_sig_gen_time",
    "generate_sig_verify_time",
    "generate_timestamp",
    "validate_range",
    "set_random_seed",
]
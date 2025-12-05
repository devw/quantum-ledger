"""
Unit tests for samplers.py module

Test coverage:
- BenchmarkSampler initialization
- Single sample generation
- Multiple samples generation
- Sample validation
- MultiRunSampler functionality
- Column ordering
"""

import pytest
import yaml
from tools.data_generation import samplers


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture(scope="module")
def config():
    """Load configuration from config.yaml"""
    with open("tools/data_generation/config.yaml") as f:
        return yaml.safe_load(f)


@pytest.fixture
def sampler_ecdsa_lowload(config):
    """Create a sampler for ECDSA + LOWLOAD"""
    return samplers.BenchmarkSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        run_id="RUN1"
    )


@pytest.fixture
def sampler_dilithium_highload(config):
    """Create a sampler for DILITHIUM3 + HIGHLOAD"""
    return samplers.BenchmarkSampler(
        config,
        crypto_mode_name="DILITHIUM3",
        load_profile_name="HIGHLOAD",
        run_id="RUN2"
    )


@pytest.fixture
def sampler_hybrid_mediumload(config):
    """Create a sampler for HYBRID + MEDIUMLOAD"""
    return samplers.BenchmarkSampler(
        config,
        crypto_mode_name="HYBRID",
        load_profile_name="MEDIUMLOAD",
        run_id="RUN3"
    )


# ==============================================================================
# TEST: INITIALIZATION
# ==============================================================================

def test_sampler_initialization(sampler_ecdsa_lowload):
    """Test that sampler initializes correctly"""
    assert sampler_ecdsa_lowload.crypto_mode_name == "ECDSA"
    assert sampler_ecdsa_lowload.load_profile_name == "LOWLOAD"
    assert sampler_ecdsa_lowload.run_id == "RUN1"
    assert sampler_ecdsa_lowload.crypto_performance_factor == 1.0
    assert sampler_ecdsa_lowload.crypto_latency_overhead == 1.0


def test_sampler_initialization_dilithium(sampler_dilithium_highload):
    """Test that DILITHIUM3 sampler has correct performance factors"""
    assert sampler_dilithium_highload.crypto_mode_name == "DILITHIUM3"
    assert sampler_dilithium_highload.crypto_performance_factor == 0.70
    assert sampler_dilithium_highload.crypto_latency_overhead == 1.8
    assert sampler_dilithium_highload.crypto_cpu_overhead == 1.6


def test_sampler_initialization_invalid_crypto_mode(config):
    """Test that invalid crypto mode raises KeyError"""
    with pytest.raises(KeyError):
        samplers.BenchmarkSampler(
            config,
            crypto_mode_name="INVALID_MODE",
            load_profile_name="LOWLOAD",
            run_id="RUN1"
        )


def test_sampler_initialization_invalid_load_profile(config):
    """Test that invalid load profile raises KeyError"""
    with pytest.raises(KeyError):
        samplers.BenchmarkSampler(
            config,
            crypto_mode_name="ECDSA",
            load_profile_name="INVALID_PROFILE",
            run_id="RUN1"
        )


# ==============================================================================
# TEST: SINGLE SAMPLE GENERATION
# ==============================================================================

def test_generate_single_sample(sampler_ecdsa_lowload):
    """Test generating a single sample"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    # Check all required columns are present
    required_columns = [
        "timestamp", "crypto_mode", "load_profile", "run_id", "tx_rate",
        "latency_avg", "latency_p95", "cpu_util", "mem_util", "block_size",
        "block_commit_time", "sig_gen_time", "sig_verify_time"
    ]
    
    for col in required_columns:
        assert col in sample, f"Column {col} missing from sample"


def test_sample_has_correct_metadata(sampler_ecdsa_lowload):
    """Test that sample contains correct metadata"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    assert sample["crypto_mode"] == "ECDSA"
    assert sample["load_profile"] == "LOWLOAD"
    assert sample["run_id"] == "RUN1"


def test_sample_timestamp_increments(sampler_ecdsa_lowload):
    """Test that timestamp increments correctly"""
    sample_0 = sampler_ecdsa_lowload.generate_sample(0)
    sample_5 = sampler_ecdsa_lowload.generate_sample(5)
    
    # Should increment by 5 seconds (5 * 1 second interval)
    assert sample_5["timestamp"] == sample_0["timestamp"] + 5.0


def test_sample_metric_ranges_ecdsa_lowload(sampler_ecdsa_lowload):
    """Test that ECDSA + LOWLOAD metrics are in expected ranges"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    # Transaction rate
    assert 50 <= sample["tx_rate"] <= 150, f"tx_rate out of range: {sample['tx_rate']}"
    
    # Latency
    assert 50 <= sample["latency_avg"] <= 200, f"latency_avg out of range: {sample['latency_avg']}"
    assert sample["latency_p95"] > sample["latency_avg"], "latency_p95 must be > latency_avg"
    
    # Resource utilization
    assert 20 <= sample["cpu_util"] <= 95, f"cpu_util out of range: {sample['cpu_util']}"
    assert 30 <= sample["mem_util"] <= 80, f"mem_util out of range: {sample['mem_util']}"
    
    # Block metrics
    assert 500 <= sample["block_size"] <= 2500, f"block_size out of range: {sample['block_size']}"
    assert 30 <= sample["block_commit_time"] <= 200, f"block_commit_time out of range"
    
    # Crypto timing (ECDSA is fast)
    assert 50 <= sample["sig_gen_time"] <= 150, f"sig_gen_time out of range: {sample['sig_gen_time']}"
    assert 100 <= sample["sig_verify_time"] <= 250, f"sig_verify_time out of range: {sample['sig_verify_time']}"


def test_sample_metric_ranges_dilithium_highload(sampler_dilithium_highload):
    """Test that DILITHIUM3 + HIGHLOAD metrics are in expected ranges"""
    sample = sampler_dilithium_highload.generate_sample(0)
    
    # Transaction rate (lower due to crypto overhead)
    assert 300 <= sample["tx_rate"] <= 800, f"tx_rate out of range: {sample['tx_rate']}"
    
    # Latency (higher due to PQC overhead)
    assert 100 <= sample["latency_avg"] <= 600, f"latency_avg out of range: {sample['latency_avg']}"
    
    # Crypto timing (DILITHIUM3 is slower)
    assert 200 <= sample["sig_gen_time"] <= 500, f"sig_gen_time out of range: {sample['sig_gen_time']}"
    assert 800 <= sample["sig_verify_time"] <= 1500, f"sig_verify_time out of range: {sample['sig_verify_time']}"


# ==============================================================================
# TEST: MULTIPLE SAMPLES GENERATION
# ==============================================================================

def test_generate_multiple_samples(sampler_ecdsa_lowload):
    """Test generating multiple samples"""
    num_samples = 10
    samples = sampler_ecdsa_lowload.generate_samples(num_samples)
    
    assert len(samples) == num_samples
    assert all(isinstance(s, dict) for s in samples)


def test_samples_have_monotonic_timestamps(sampler_ecdsa_lowload):
    """Test that timestamps are monotonically increasing"""
    samples = sampler_ecdsa_lowload.generate_samples(10)
    
    timestamps = [s["timestamp"] for s in samples]
    
    # Check monotonic increase
    for i in range(len(timestamps) - 1):
        assert timestamps[i+1] > timestamps[i], "Timestamps not monotonically increasing"


def test_samples_variability(sampler_ecdsa_lowload):
    """Test that samples have variability (not all identical)"""
    samples = sampler_ecdsa_lowload.generate_samples(10)
    
    # Extract tx_rate from all samples
    tx_rates = [s["tx_rate"] for s in samples]
    
    # Should have some variability
    assert len(set(tx_rates)) > 1, "All tx_rate values are identical (no variability)"


# ==============================================================================
# TEST: SAMPLE VALIDATION
# ==============================================================================

def test_validate_sample_valid(sampler_ecdsa_lowload):
    """Test validation of a valid sample"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    assert sampler_ecdsa_lowload.validate_sample(sample) is True


def test_validate_sample_invalid_latency_ordering(sampler_ecdsa_lowload):
    """Test validation catches incorrect latency ordering"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    # Break latency ordering
    sample["latency_p95"] = sample["latency_avg"] - 10
    
    assert sampler_ecdsa_lowload.validate_sample(sample) is False


def test_validate_sample_invalid_cpu_util(sampler_ecdsa_lowload):
    """Test validation catches invalid CPU utilization"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    # Set invalid CPU value
    sample["cpu_util"] = 150  # Over 100%
    
    assert sampler_ecdsa_lowload.validate_sample(sample) is False


def test_validate_sample_missing_column(sampler_ecdsa_lowload):
    """Test validation catches missing columns"""
    sample = sampler_ecdsa_lowload.generate_sample(0)
    
    # Remove a required column
    del sample["tx_rate"]
    
    assert sampler_ecdsa_lowload.validate_sample(sample) is False


# ==============================================================================
# TEST: COLUMN ORDERING
# ==============================================================================

def test_get_column_order(sampler_ecdsa_lowload):
    """Test that column order matches config"""
    columns = sampler_ecdsa_lowload.get_column_order()
    
    expected_columns = [
        "timestamp", "crypto_mode", "load_profile", "run_id", "tx_rate",
        "latency_avg", "latency_p95", "cpu_util", "mem_util", "block_size",
        "block_commit_time", "sig_gen_time", "sig_verify_time"
    ]
    
    assert columns == expected_columns


# ==============================================================================
# TEST: MULTI-RUN SAMPLER
# ==============================================================================

def test_multi_run_sampler_initialization(config):
    """Test MultiRunSampler initialization"""
    multi_sampler = samplers.MultiRunSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        num_runs=3
    )
    
    assert multi_sampler.crypto_mode_name == "ECDSA"
    assert multi_sampler.load_profile_name == "LOWLOAD"
    assert multi_sampler.num_runs == 3


def test_multi_run_generate_single_run(config):
    """Test generating a single run with MultiRunSampler"""
    multi_sampler = samplers.MultiRunSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        num_runs=3
    )
    
    samples = multi_sampler.generate_run(run_number=1, num_samples=10)
    
    assert len(samples) == 10
    assert all(s["run_id"] == "RUN1" for s in samples)


def test_multi_run_generate_all_runs(config):
    """Test generating all runs with MultiRunSampler"""
    multi_sampler = samplers.MultiRunSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        num_runs=3
    )
    
    all_data = multi_sampler.generate_all_runs(num_samples_per_run=10)
    
    assert len(all_data) == 3
    assert "RUN1" in all_data
    assert "RUN2" in all_data
    assert "RUN3" in all_data
    
    # Check each run has correct number of samples
    for run_id, samples in all_data.items():
        assert len(samples) == 10
        assert all(s["run_id"] == run_id for s in samples)


# ==============================================================================
# TEST: FACTORY FUNCTION
# ==============================================================================

def test_create_sampler_from_config(config):
    """Test factory function"""
    sampler = samplers.create_sampler_from_config(
        config,
        crypto_mode="ECDSA",
        load_profile="LOWLOAD",
        run_id="RUN1"
    )
    
    assert isinstance(sampler, samplers.BenchmarkSampler)
    assert sampler.crypto_mode_name == "ECDSA"
    assert sampler.load_profile_name == "LOWLOAD"
    assert sampler.run_id == "RUN1"


# ==============================================================================
# TEST: CRYPTO MODE COMPARISON
# ==============================================================================

def test_dilithium_slower_than_ecdsa(config):
    """Test that DILITHIUM3 generates slower crypto times than ECDSA"""
    sampler_ecdsa = samplers.BenchmarkSampler(config, "ECDSA", "LOWLOAD", "RUN1")
    sampler_dilithium = samplers.BenchmarkSampler(config, "DILITHIUM3", "LOWLOAD", "RUN1")
    
    # Generate multiple samples for statistical comparison
    samples_ecdsa = sampler_ecdsa.generate_samples(50)
    samples_dilithium = sampler_dilithium.generate_samples(50)
    
    # Calculate averages
    avg_verify_ecdsa = sum(s["sig_verify_time"] for s in samples_ecdsa) / 50
    avg_verify_dilithium = sum(s["sig_verify_time"] for s in samples_dilithium) / 50
    
    # DILITHIUM3 should be at least 3x slower for verification
    assert avg_verify_dilithium > avg_verify_ecdsa * 2.5, \
        f"DILITHIUM3 verify ({avg_verify_dilithium:.1f}) not significantly slower than ECDSA ({avg_verify_ecdsa:.1f})"


def test_highload_higher_latency_than_lowload(config):
    """Test that HIGHLOAD has higher latency than LOWLOAD"""
    sampler_low = samplers.BenchmarkSampler(config, "ECDSA", "LOWLOAD", "RUN1")
    sampler_high = samplers.BenchmarkSampler(config, "ECDSA", "HIGHLOAD", "RUN1")
    
    samples_low = sampler_low.generate_samples(50)
    samples_high = sampler_high.generate_samples(50)
    
    avg_latency_low = sum(s["latency_avg"] for s in samples_low) / 50
    avg_latency_high = sum(s["latency_avg"] for s in samples_high) / 50
    
    assert avg_latency_high > avg_latency_low, \
        f"HIGHLOAD latency ({avg_latency_high:.1f}) not higher than LOWLOAD ({avg_latency_low:.1f})"
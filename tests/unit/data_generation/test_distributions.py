# tests/unit/tools/data_generation/test_distributions.py
import pytest
import yaml
from tools.data_generation import distributions

# Fixture per caricare il config una sola volta
@pytest.fixture(scope="module")
def config():
    with open("tools/data_generation/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="module")
def load_profile(config):
    return config["load_profiles"]["LOWLOAD"]

@pytest.fixture(scope="module")
def crypto_ecdsa(config):
    return config["crypto_modes"]["ECDSA"]

@pytest.fixture(scope="module")
def crypto_dilithium(config):
    return config["crypto_modes"]["DILITHIUM3"]

# Test 1: generate_tx_rate
def test_generate_tx_rate(load_profile):
    tx_rate = distributions.generate_tx_rate(load_profile, crypto_performance_factor=1.0)
    assert 50 <= tx_rate <= 150, f"tx_rate out of range: {tx_rate}"

# Test 2: generate_latency_avg
def test_generate_latency_avg(load_profile):
    latency_avg = distributions.generate_latency_avg(load_profile, crypto_latency_overhead=1.0, tx_rate=100)
    assert 50 <= latency_avg <= 150, f"latency_avg out of range: {latency_avg}"

# Test 3: generate_latency_p95
def test_generate_latency_p95(load_profile):
    latency_avg = distributions.generate_latency_avg(load_profile, crypto_latency_overhead=1.0, tx_rate=100)
    latency_p95 = distributions.generate_latency_p95(latency_avg)
    assert latency_p95 > latency_avg, f"latency_p95 <= latency_avg"
    assert latency_p95 >= latency_avg * 1.5, f"latency_p95 ratio too low"

# Test 4: generate_cpu_util
def test_generate_cpu_util(load_profile):
    cpu_util = distributions.generate_cpu_util(load_profile, crypto_cpu_overhead=1.0, tx_rate=100)
    assert 20 <= cpu_util <= 95, f"cpu_util out of range: {cpu_util}"

# Test 5: generate_mem_util
def test_generate_mem_util(load_profile):
    mem_util = distributions.generate_mem_util(load_profile, tx_rate=100)
    assert 30 <= mem_util <= 80, f"mem_util out of range: {mem_util}"

# Test 6: generate_block_size
def test_generate_block_size():
    block_size = distributions.generate_block_size(tx_rate=100)
    assert 500 <= block_size <= 2500, f"block_size out of range: {block_size}"

# Test 7: generate_block_commit_time
def test_generate_block_commit_time():
    block_size = distributions.generate_block_size(tx_rate=100)
    block_commit_time = distributions.generate_block_commit_time(block_size, crypto_overhead_factor=0.3)
    assert 30 <= block_commit_time <= 200, f"block_commit_time out of range: {block_commit_time}"

# Test 8: generate_sig_gen_time (ECDSA)
def test_generate_sig_gen_time(crypto_ecdsa):
    sig_gen_time = distributions.generate_sig_gen_time(crypto_ecdsa)
    assert 50 <= sig_gen_time <= 150, f"sig_gen_time out of range: {sig_gen_time}"

# Test 9: generate_sig_verify_time (ECDSA)
def test_generate_sig_verify_time(crypto_ecdsa):
    sig_verify_time = distributions.generate_sig_verify_time(crypto_ecdsa)
    assert 100 <= sig_verify_time <= 250, f"sig_verify_time out of range: {sig_verify_time}"

# Test 10: PQC DILITHIUM3 slower than ECDSA
def test_dilithium3_slower(crypto_ecdsa, crypto_dilithium):
    sig_gen_ecdsa = distributions.generate_sig_gen_time(crypto_ecdsa)
    sig_verify_ecdsa = distributions.generate_sig_verify_time(crypto_ecdsa)
    sig_gen_dilithium = distributions.generate_sig_gen_time(crypto_dilithium)
    sig_verify_dilithium = distributions.generate_sig_verify_time(crypto_dilithium)

    assert sig_gen_dilithium > sig_gen_ecdsa * 1.5, "DILITHIUM3 not slower enough"
    assert sig_verify_dilithium > sig_verify_ecdsa * 2.0, "DILITHIUM3 verify not slower enough"

# Test 11: generate_timestamp
def test_generate_timestamp():
    ts1 = distributions.generate_timestamp(1735920000.0, 0)
    ts2 = distributions.generate_timestamp(1735920000.0, 5)
    assert ts2 == ts1 + 5.0, "Timestamp not monotonic"

# Test 12: Random seed reproducibility
def test_random_seed_reproducibility(load_profile):
    distributions.set_random_seed(42)
    val1 = distributions.generate_tx_rate(load_profile)
    distributions.set_random_seed(42)
    val2 = distributions.generate_tx_rate(load_profile)
    assert val1 == val2, "Random seed not working"

"""
Unit tests for generate_benchmark_data.py script

Test coverage:
- Config loading
- Argument validation  
- Data generation workflow
- File creation
"""

import pytest
import yaml
import os
import tempfile
import shutil
from pathlib import Path

from tools.scripts import generate_benchmark_data


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture(scope="module")
def config():
    """Load configuration from config.yaml"""
    with open("tools/data_generation/config.yaml") as f:
        return yaml.safe_load(f)


@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory for tests"""
    temp_dir = tempfile.mkdtemp(prefix="test_generate_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_args():
    """Create mock command-line arguments"""
    class Args:
        crypto_modes = ["ECDSA"]
        load_profiles = ["LOWLOAD"]
        runs = 2
        duration = 5
        output_dir = None
        config = "tools/data_generation/config.yaml"
        seed = None
        quiet = False
    return Args()


# ==============================================================================
# TEST: CONFIG LOADING
# ==============================================================================

def test_load_config():
    """Test loading configuration file"""
    config = generate_benchmark_data.load_config("tools/data_generation/config.yaml")
    assert isinstance(config, dict)
    assert "crypto_modes" in config
    assert "load_profiles" in config


def test_load_config_nonexistent():
    """Test loading nonexistent config raises error"""
    with pytest.raises(FileNotFoundError):
        generate_benchmark_data.load_config("nonexistent.yaml")


# ==============================================================================
# TEST: ARGUMENT VALIDATION
# ==============================================================================

def test_validate_arguments_valid(mock_args, config):
    """Test validation with valid arguments"""
    generate_benchmark_data.validate_arguments(mock_args, config)


def test_validate_arguments_invalid_crypto_mode(mock_args, config):
    """Test validation catches invalid crypto mode"""
    mock_args.crypto_modes = ["INVALID_MODE"]
    with pytest.raises(ValueError, match="Invalid crypto mode"):
        generate_benchmark_data.validate_arguments(mock_args, config)


def test_validate_arguments_invalid_load_profile(mock_args, config):
    """Test validation catches invalid load profile"""
    mock_args.crypto_modes = ["ECDSA"]
    mock_args.load_profiles = ["INVALID_PROFILE"]
    with pytest.raises(ValueError, match="Invalid load profile"):
        generate_benchmark_data.validate_arguments(mock_args, config)


# ==============================================================================
# TEST: SAMPLE CALCULATION
# ==============================================================================

def test_calculate_num_samples():
    """Test sample calculation"""
    assert generate_benchmark_data.calculate_num_samples(300) == 300
    assert generate_benchmark_data.calculate_num_samples(300, 2.0) == 150


# ==============================================================================
# TEST: DATA GENERATION
# ==============================================================================

def test_generate_data_basic(config, temp_output_dir):
    """Test basic data generation"""
    stats = generate_benchmark_data.generate_data(
        config=config,
        crypto_modes=["ECDSA"],
        load_profiles=["LOWLOAD"],
        runs=2,
        duration=5,
        output_dir=temp_output_dir,
        verbose=False
    )
    
    assert stats['total_files'] == 2
    assert len(stats['files_created']) == 2
    
    # Verify files exist
    for filepath in stats['files_created']:
        assert os.path.exists(filepath)


def test_generate_data_multiple_combinations(config, temp_output_dir):
    """Test generating multiple combinations"""
    stats = generate_benchmark_data.generate_data(
        config=config,
        crypto_modes=["ECDSA", "DILITHIUM3"],
        load_profiles=["LOWLOAD", "HIGHLOAD"],
        runs=2,
        duration=5,
        output_dir=temp_output_dir,
        verbose=False
    )
    
    assert stats['total_combinations'] == 4
    assert stats['total_files'] == 8
    assert len(stats['files_created']) == 8
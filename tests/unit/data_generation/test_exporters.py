"""
Unit tests for exporters.py module

Test coverage:
- CSVExporter initialization
- Filename generation
- CSV export functionality
- Format validation
- Multiple runs export
- Utility functions
"""

import pytest
import yaml
import csv
import os
import tempfile
import shutil
from pathlib import Path
from tools.data_generation import exporters, samplers


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
    temp_dir = tempfile.mkdtemp(prefix="test_export_")
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def exporter(config, temp_output_dir):
    """Create a CSVExporter instance"""
    return exporters.CSVExporter(config, output_dir=temp_output_dir)


@pytest.fixture
def sample_data(config):
    """Generate sample data for testing"""
    sampler = samplers.BenchmarkSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        run_id="RUN1"
    )
    return sampler.generate_samples(10)


@pytest.fixture
def multi_run_data(config):
    """Generate multi-run sample data"""
    multi_sampler = samplers.MultiRunSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        num_runs=3
    )
    return multi_sampler.generate_all_runs(num_samples_per_run=5)


# ==============================================================================
# TEST: CSV EXPORT UTILITIES 
# ==============================================================================

def test_export_run_with_csvexporter(sample_data, temp_output_dir, config):
    """Test exporting a single run using CSVExporter only"""
    exporter = exporters.CSVExporter(config, output_dir=temp_output_dir)
    filepath = exporter.export_run(sample_data, "ECDSA", "LOWLOAD", 1)
    
    assert os.path.exists(filepath)
    assert os.path.basename(filepath) == "ECDSA_LOWLOAD_RUN1.csv"


def test_export_run_auto_columns(sample_data, temp_output_dir, config):
    """Test export with automatic column detection via CSVExporter"""
    exporter = exporters.CSVExporter(config, output_dir=temp_output_dir)
    filepath = exporter.export_run(sample_data, "DILITHIUM3", "HIGHLOAD", 2)
    
    # Read back CSV
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
    
    # Deve avere tutte le colonne dei sample
    assert set(header) == set(exporter.columns)


def test_export_multiple_runs_csvexporter(multi_run_data, temp_output_dir, config):
    """Test multiple runs export via CSVExporter"""
    exporter = exporters.CSVExporter(config, output_dir=temp_output_dir)
    created_files = exporter.export_multiple_runs(
        multi_run_data,
        crypto_mode="ECDSA",
        load_profile="LOWLOAD"
    )
    
    assert len(created_files) == len(multi_run_data)
    for fpath in created_files:
        assert os.path.exists(fpath)


def test_filename_generation_only_csvexporter(config):
    """Test filename generation via CSVExporter only"""
    exporter = exporters.CSVExporter(config)
    filename = exporter.generate_filename("HYBRID", "MEDIUMLOAD", 3)
    assert filename == "HYBRID_MEDIUMLOAD_RUN3.csv"





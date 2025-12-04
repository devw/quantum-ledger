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
# TEST: INITIALIZATION
# ==============================================================================

def test_exporter_initialization(exporter, temp_output_dir):
    """Test that exporter initializes correctly"""
    assert exporter.output_dir == temp_output_dir
    assert exporter.decimal_precision == 3
    assert len(exporter.columns) == 13
    assert exporter.delimiter == ","


def test_exporter_initialization_default_dir(config):
    """Test exporter with default output directory"""
    exporter = exporters.CSVExporter(config)
    assert exporter.output_dir == "."


def test_exporter_columns_order(exporter):
    """Test that columns are in correct order"""
    expected_columns = [
        "timestamp", "crypto_mode", "load_profile", "run_id", "tx_rate",
        "latency_avg", "latency_p95", "cpu_util", "mem_util", "block_size",
        "block_commit_time", "sig_gen_time", "sig_verify_time"
    ]
    assert exporter.columns == expected_columns


# ==============================================================================
# TEST: FILENAME GENERATION
# ==============================================================================

def test_generate_filename(exporter):
    """Test filename generation"""
    filename = exporter.generate_filename("ECDSA", "LOWLOAD", 1)
    assert filename == "ECDSA_LOWLOAD_RUN1.csv"


def test_generate_filename_different_params(exporter):
    """Test filename generation with different parameters"""
    filename = exporter.generate_filename("DILITHIUM3", "HIGHLOAD", 5)
    assert filename == "DILITHIUM3_HIGHLOAD_RUN5.csv"


def test_generate_filename_hybrid(exporter):
    """Test filename generation for HYBRID mode"""
    filename = exporter.generate_filename("HYBRID", "MEDIUMLOAD", 2)
    assert filename == "HYBRID_MEDIUMLOAD_RUN2.csv"


# ==============================================================================
# TEST: VALUE FORMATTING
# ==============================================================================

def test_format_value_float(exporter):
    """Test formatting of float values"""
    formatted = exporter.format_value(123.456789)
    assert formatted == "123.457"  # 3 decimal places


def test_format_value_integer(exporter):
    """Test formatting of integer values"""
    formatted = exporter.format_value(1024)
    assert formatted == "1024"


def test_format_value_string(exporter):
    """Test formatting of string values"""
    formatted = exporter.format_value("ECDSA")
    assert formatted == "ECDSA"


# ==============================================================================
# TEST: DIRECTORY MANAGEMENT
# ==============================================================================

def test_ensure_output_directory(config):
    """Test that output directory is created if it doesn't exist"""
    temp_dir = tempfile.mktemp(prefix="test_dir_")
    
    try:
        exporter = exporters.CSVExporter(config, output_dir=temp_dir)
        exporter.ensure_output_directory()
        
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)
    
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


# ==============================================================================
# TEST: CSV EXPORT
# ==============================================================================

def test_export_samples_basic(exporter, sample_data, temp_output_dir):
    """Test basic CSV export"""
    filepath = exporter.export_samples(sample_data, "test_output.csv")
    
    # Check file was created
    assert os.path.exists(filepath)
    assert filepath == os.path.join(temp_output_dir, "test_output.csv")


def test_export_samples_content(exporter, sample_data, temp_output_dir):
    """Test that exported CSV has correct content"""
    filepath = exporter.export_samples(sample_data, "test_output.csv")
    
    # Read back the CSV
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Check number of rows
    assert len(rows) == 10
    
    # Check first row has all columns
    assert set(rows[0].keys()) == set(exporter.columns)


def test_export_samples_header(exporter, sample_data, temp_output_dir):
    """Test that CSV has correct header"""
    filepath = exporter.export_samples(sample_data, "test_output.csv")
    
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
    
    assert header == exporter.columns


def test_export_samples_empty_raises_error(exporter):
    """Test that exporting empty list raises ValueError"""
    with pytest.raises(ValueError, match="Cannot export empty sample list"):
        exporter.export_samples([], "test.csv")


def test_export_samples_missing_columns_raises_error(exporter, sample_data):
    """Test that samples with missing columns raise ValueError"""
    # Remove a required column from samples
    incomplete_samples = [
        {k: v for k, v in sample.items() if k != "tx_rate"}
        for sample in sample_data
    ]
    
    with pytest.raises(ValueError, match="missing required columns"):
        exporter.export_samples(incomplete_samples, "test.csv")


def test_export_samples_decimal_precision(exporter, sample_data, temp_output_dir):
    """Test that float values are formatted with correct precision"""
    filepath = exporter.export_samples(sample_data, "test_output.csv")
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        first_row = next(reader)
    
    # Check that tx_rate has 3 decimal places
    tx_rate = first_row["tx_rate"]
    decimal_part = tx_rate.split('.')[1] if '.' in tx_rate else ""
    assert len(decimal_part) == 3


# ==============================================================================
# TEST: EXPORT RUN
# ==============================================================================

def test_export_run(exporter, sample_data, temp_output_dir):
    """Test exporting a single run with automatic filename"""
    filepath = exporter.export_run(sample_data, "ECDSA", "LOWLOAD", 1)
    
    # Check file exists
    assert os.path.exists(filepath)
    
    # Check filename is correct
    expected_filename = "ECDSA_LOWLOAD_RUN1.csv"
    assert os.path.basename(filepath) == expected_filename


def test_export_run_different_params(exporter, sample_data, temp_output_dir):
    """Test export_run with different parameters"""
    # Modify sample data to have correct metadata
    for sample in sample_data:
        sample["crypto_mode"] = "DILITHIUM3"
        sample["load_profile"] = "HIGHLOAD"
        sample["run_id"] = "RUN3"
    
    filepath = exporter.export_run(sample_data, "DILITHIUM3", "HIGHLOAD", 3)
    
    expected_filename = "DILITHIUM3_HIGHLOAD_RUN3.csv"
    assert os.path.basename(filepath) == expected_filename


# ==============================================================================
# TEST: EXPORT MULTIPLE RUNS
# ==============================================================================

def test_export_multiple_runs(exporter, multi_run_data, temp_output_dir):
    """Test exporting multiple runs"""
    created_files = exporter.export_multiple_runs(
        multi_run_data,
        "ECDSA",
        "LOWLOAD"
    )
    
    # Check correct number of files created
    assert len(created_files) == 3
    
    # Check all files exist
    for filepath in created_files:
        assert os.path.exists(filepath)


def test_export_multiple_runs_filenames(exporter, multi_run_data, temp_output_dir):
    """Test that multiple runs have correct filenames"""
    created_files = exporter.export_multiple_runs(
        multi_run_data,
        "ECDSA",
        "LOWLOAD"
    )
    
    filenames = [os.path.basename(f) for f in created_files]
    
    expected_filenames = [
        "ECDSA_LOWLOAD_RUN1.csv",
        "ECDSA_LOWLOAD_RUN2.csv",
        "ECDSA_LOWLOAD_RUN3.csv"
    ]
    
    assert filenames == expected_filenames


def test_export_multiple_runs_content(exporter, multi_run_data, temp_output_dir):
    """Test that each exported run has correct content"""
    created_files = exporter.export_multiple_runs(
        multi_run_data,
        "ECDSA",
        "LOWLOAD"
    )
    
    # Check first file
    with open(created_files[0], 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Should have 5 samples
    assert len(rows) == 5
    
    # All rows should have run_id = "RUN1"
    assert all(row["run_id"] == "RUN1" for row in rows)


# ==============================================================================
# TEST: UTILITY FUNCTIONS
# ==============================================================================

def test_export_to_csv_utility(sample_data, temp_output_dir):
    """Test utility function export_to_csv"""
    output_path = os.path.join(temp_output_dir, "utility_test.csv")
    
    columns = ["timestamp", "crypto_mode", "tx_rate", "latency_avg"]
    exporters.export_to_csv(sample_data, output_path, columns=columns)
    
    assert os.path.exists(output_path)


def test_export_to_csv_auto_columns(sample_data, temp_output_dir):
    """Test export_to_csv with automatic column detection"""
    output_path = os.path.join(temp_output_dir, "auto_columns.csv")
    
    exporters.export_to_csv(sample_data, output_path)
    
    # Read and check columns
    with open(output_path, 'r') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
    
    # Should have all columns from first sample
    assert len(header) == len(sample_data[0].keys())


def test_get_output_path_utility():
    """Test get_output_path utility function"""
    path = exporters.get_output_path(
        "/tmp/data",
        "ECDSA",
        "LOWLOAD",
        1
    )
    
    assert path == "/tmp/data/ECDSA_LOWLOAD_RUN1.csv"


def test_validate_csv_file_valid(exporter, sample_data, temp_output_dir):
    """Test validate_csv_file with valid CSV"""
    filepath = exporter.export_samples(sample_data, "valid.csv")
    
    is_valid = exporters.validate_csv_file(filepath, exporter.columns)
    assert is_valid is True


def test_validate_csv_file_invalid_columns(exporter, sample_data, temp_output_dir):
    """Test validate_csv_file with wrong columns"""
    filepath = exporter.export_samples(sample_data, "test.csv")
    
    wrong_columns = ["wrong", "column", "names"]
    is_valid = exporters.validate_csv_file(filepath, wrong_columns)
    assert is_valid is False


def test_validate_csv_file_nonexistent():
    """Test validate_csv_file with nonexistent file"""
    is_valid = exporters.validate_csv_file("/nonexistent/file.csv", [])
    assert is_valid is False


# ==============================================================================
# TEST: INTEGRATION
# ==============================================================================

def test_full_export_workflow(config, temp_output_dir):
    """Test complete workflow: generate + export"""
    # Generate data
    sampler = samplers.BenchmarkSampler(
        config,
        crypto_mode_name="ECDSA",
        load_profile_name="LOWLOAD",
        run_id="RUN1"
    )
    samples = sampler.generate_samples(20)
    
    # Export
    exporter = exporters.CSVExporter(config, output_dir=temp_output_dir)
    filepath = exporter.export_run(samples, "ECDSA", "LOWLOAD", 1)
    
    # Validate
    assert os.path.exists(filepath)
    
    # Read and verify
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 20
    assert rows[0]["crypto_mode"] == "ECDSA"
    assert rows[0]["load_profile"] == "LOWLOAD"


def test_multiple_crypto_modes_export(config, temp_output_dir):
    """Test exporting data for multiple crypto modes"""
    exporter = exporters.CSVExporter(config, output_dir=temp_output_dir)
    
    crypto_modes = ["ECDSA", "DILITHIUM3", "HYBRID"]
    created_files = []
    
    for crypto_mode in crypto_modes:
        sampler = samplers.BenchmarkSampler(
            config,
            crypto_mode_name=crypto_mode,
            load_profile_name="LOWLOAD",
            run_id="RUN1"
        )
        samples = sampler.generate_samples(5)
        filepath = exporter.export_run(samples, crypto_mode, "LOWLOAD", 1)
        created_files.append(filepath)
    
    # Check all files created
    assert len(created_files) == 3
    
    # Check filenames
    filenames = [os.path.basename(f) for f in created_files]
    assert "ECDSA_LOWLOAD_RUN1.csv" in filenames
    assert "DILITHIUM3_LOWLOAD_RUN1.csv" in filenames
    assert "HYBRID_LOWLOAD_RUN1.csv" in filenames
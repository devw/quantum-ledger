#!/usr/bin/env python3
"""
Generate Mock Benchmark Data for PQC Hyperledger Fabric

This script generates realistic mock benchmark data for Post-Quantum Cryptography
(PQC) performance evaluation on Hyperledger Fabric. It supports multiple crypto
modes (ECDSA, DILITHIUM3, HYBRID) and load profiles (LOWLOAD, MEDIUMLOAD, 
HIGHLOAD, SUSTAINED).

Usage:
    python tools/scripts/generate_benchmark_data.py \\
        --crypto-modes ECDSA DILITHIUM3 HYBRID \\
        --load-profiles LOWLOAD HIGHLOAD \\
        --runs 3 \\
        --duration 300 \\
        --output-dir data/fixtures/monte_carlo/

Version: 0.1.0 (MVP - Draft)
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import List

# Add parent directory to path to import data_generation modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.data_generation import samplers, exporters, distributions


def load_config(config_path: str = "tools/data_generation/config.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config.yaml file
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def validate_arguments(args, config: dict) -> None:
    """
    Validate command-line arguments against config.
    
    Args:
        args: Parsed command-line arguments
        config: Configuration dictionary
    
    Raises:
        ValueError: If arguments are invalid
    """
    # Validate crypto modes
    available_crypto_modes = list(config['crypto_modes'].keys())
    for mode in args.crypto_modes:
        if mode not in available_crypto_modes:
            raise ValueError(
                f"Invalid crypto mode: {mode}. "
                f"Available modes: {available_crypto_modes}"
            )
    
    # Validate load profiles
    available_load_profiles = list(config['load_profiles'].keys())
    for profile in args.load_profiles:
        if profile not in available_load_profiles:
            raise ValueError(
                f"Invalid load profile: {profile}. "
                f"Available profiles: {available_load_profiles}"
            )
    
    # Validate runs
    if args.runs < 1:
        raise ValueError(f"Number of runs must be >= 1, got: {args.runs}")
    
    # Validate duration
    if args.duration < 1:
        raise ValueError(f"Duration must be >= 1 second, got: {args.duration}")


def calculate_num_samples(duration: int, sampling_interval: float = 1.0) -> int:
    """
    Calculate number of samples from duration.
    
    Args:
        duration: Duration in seconds
        sampling_interval: Seconds between samples
    
    Returns:
        Number of samples to generate
    """
    return int(duration / sampling_interval)


def generate_data(
    config: dict,
    crypto_modes: List[str],
    load_profiles: List[str],
    runs: int,
    duration: int,
    output_dir: str,
    verbose: bool = True
) -> dict:
    """
    Generate mock benchmark data for all combinations.
    
    Args:
        config: Configuration dictionary
        crypto_modes: List of crypto mode names
        load_profiles: List of load profile names
        runs: Number of runs per combination
        duration: Duration in seconds
        output_dir: Output directory for CSV files
        verbose: Print progress messages
    
    Returns:
        Dictionary with generation statistics
    """
    # Calculate number of samples
    sampling_interval = config['sampling']['interval']
    num_samples = calculate_num_samples(duration, sampling_interval)
    
    if verbose:
        print(f"🔧 Configuration:")
        print(f"   Crypto modes: {', '.join(crypto_modes)}")
        print(f"   Load profiles: {', '.join(load_profiles)}")
        print(f"   Runs per combination: {runs}")
        print(f"   Duration: {duration}s ({num_samples} samples at {sampling_interval}s interval)")
        print(f"   Output directory: {output_dir}")
        print()
    
    # Create exporter
    exporter = exporters.CSVExporter(config, output_dir=output_dir)
    
    # Ensure output directory exists
    exporter.ensure_output_directory()
    
    # Statistics
    stats = {
        'total_combinations': len(crypto_modes) * len(load_profiles),
        'total_files': len(crypto_modes) * len(load_profiles) * runs,
        'files_created': [],
        'samples_per_file': num_samples,
        'total_samples': len(crypto_modes) * len(load_profiles) * runs * num_samples,
    }
    
    if verbose:
        print(f"📊 Generation plan:")
        print(f"   Total combinations: {stats['total_combinations']}")
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total samples: {stats['total_samples']:,}")
        print()
        print("🚀 Starting generation...\n")
    
    # Generate data for each combination
    file_counter = 0
    for crypto_mode in crypto_modes:
        for load_profile in load_profiles:
            if verbose:
                print(f"📁 Generating: {crypto_mode} × {load_profile}")
            
            # Create multi-run sampler
            multi_sampler = samplers.MultiRunSampler(
                config,
                crypto_mode_name=crypto_mode,
                load_profile_name=load_profile,
                num_runs=runs
            )
            
            # Generate all runs
            all_runs_data = multi_sampler.generate_all_runs(num_samples)
            
            # Export each run
            created_files = exporter.export_multiple_runs(
                all_runs_data,
                crypto_mode,
                load_profile
            )
            
            # Update statistics
            stats['files_created'].extend(created_files)
            file_counter += len(created_files)
            
            if verbose:
                for filepath in created_files:
                    filename = Path(filepath).name
                    print(f"   ✅ {filename}")
            
            if verbose:
                print()
    
    if verbose:
        print("=" * 70)
        print(f"✨ Generation complete!")
        print(f"   Files created: {len(stats['files_created'])}")
        print(f"   Total samples: {stats['total_samples']:,}")
        print(f"   Output directory: {output_dir}")
        print("=" * 70)
    
    return stats


def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Generate mock benchmark data for PQC Hyperledger Fabric",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate for ECDSA with LOWLOAD (3 runs, 5 minutes each)
  python tools/scripts/generate_benchmark_data.py \\
      --crypto-modes ECDSA \\
      --load-profiles LOWLOAD \\
      --runs 3 \\
      --duration 300 \\
      --output-dir data/fixtures/monte_carlo/

  # Generate all combinations for workshop
  python tools/scripts/generate_benchmark_data.py \\
      --crypto-modes ECDSA DILITHIUM3 HYBRID \\
      --load-profiles LOWLOAD HIGHLOAD \\
      --runs 3 \\
      --duration 300 \\
      --output-dir data/fixtures/monte_carlo/

  # Generate complete dataset for journal paper
  python tools/scripts/generate_benchmark_data.py \\
      --crypto-modes ECDSA DILITHIUM3 HYBRID \\
      --load-profiles LOWLOAD MEDIUMLOAD HIGHLOAD SUSTAINED \\
      --runs 5 \\
      --duration 600 \\
      --output-dir data/raw/
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--crypto-modes',
        nargs='+',
        required=True,
        help='Crypto modes to generate (e.g., ECDSA DILITHIUM3 HYBRID)'
    )
    
    parser.add_argument(
        '--load-profiles',
        nargs='+',
        required=True,
        help='Load profiles to generate (e.g., LOWLOAD MEDIUMLOAD HIGHLOAD SUSTAINED)'
    )
    
    parser.add_argument(
        '--runs',
        type=int,
        required=True,
        help='Number of runs per combination (e.g., 3 for RUN1, RUN2, RUN3)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        required=True,
        help='Duration of each run in seconds (e.g., 300 for 5 minutes)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='Output directory for CSV files'
    )
    
    # Optional arguments
    parser.add_argument(
        '--config',
        type=str,
        default='tools/data_generation/config.yaml',
        help='Path to config.yaml (default: tools/data_generation/config.yaml)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility (default: None = random)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0 (MVP)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Validate arguments
        validate_arguments(args, config)
        
        # Set random seed if specified
        if args.seed is not None:
            distributions.set_random_seed(args.seed)
            if not args.quiet:
                print(f"🎲 Random seed set to: {args.seed}\n")
        
        # Generate data
        stats = generate_data(
            config=config,
            crypto_modes=args.crypto_modes,
            load_profiles=args.load_profiles,
            runs=args.runs,
            duration=args.duration,
            output_dir=args.output_dir,
            verbose=not args.quiet
        )
        
        # Exit successfully
        sys.exit(0)
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
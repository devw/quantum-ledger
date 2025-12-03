#!/usr/bin/env python3
"""
CLI Script to generate Monte Carlo mock data for blockchain benchmarks.

Usage:
    python tools/scripts/generate_mock_data.py --iterations 1000 --output data/fixtures/monte_carlo/samples.csv
"""

import argparse
import sys
from pathlib import Path

# Add tools directory to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.data_generation.monte_carlo_generator import MonteCarloGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Generate Monte Carlo mock data for blockchain benchmarks'
    )
    
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=1000,
        help='Number of samples to generate (default: 1000)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/fixtures/monte_carlo/samples.csv',
        help='Output CSV file path (default: data/fixtures/monte_carlo/samples.csv)'
    )
    
    parser.add_argument(
        '--seed', '-s',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to scenario configuration YAML file (optional)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Also export to JSON format'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print statistics of generated data'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎲 Monte Carlo Mock Data Generator")
    print("=" * 60)
    
    try:
        # Initialize generator
        generator = MonteCarloGenerator(
            scenario_config=args.config,
            seed=args.seed
        )
        
        # Generate samples
        generator.generate(iterations=args.iterations)
        
        # Validate
        if not generator.validate():
            print("❌ Validation failed")
            sys.exit(1)
        
        # Export to CSV
        csv_path = generator.export_csv(args.output)
        
        # Export to JSON if requested
        if args.json:
            json_path = args.output.replace('.csv', '.json')
            generator.export_json(json_path)
        
        # Print statistics if requested
        if args.stats:
            print("\n📊 Statistics:")
            print("-" * 60)
            stats = generator.get_statistics()
            for param, values in stats.items():
                print(f"\n{param}:")
                for stat_name, stat_value in values.items():
                    print(f"  {stat_name:8s}: {stat_value:10.2f}")
        
        print("\n" + "=" * 60)
        print("✅ Generation completed successfully!")
        print(f"📁 Output: {csv_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
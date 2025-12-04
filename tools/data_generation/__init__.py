"""
PQC Hyperledger Fabric Mock Data Generation Package

This package provides tools for generating realistic mock benchmark data
for Post-Quantum Cryptography (PQC) performance evaluation on Hyperledger Fabric.

Modules:
    - distributions: Statistical distributions for metric generation
    - samplers: Data sampling and generation logic
    - exporters: CSV export functionality
    - validators: Data validation and consistency checks
    - monte_carlo_generator: Main orchestrator for data generation

Version: 0.1.0 (MVP - Draft)
"""

__version__ = "0.1.0"
__author__ = "PQC Hyperledger Fabric Benchmark Team"

# Package metadata
__all__ = [
    "distributions",
    "samplers", 
    "exporters",
    "validators",
    "monte_carlo_generator"
]
"""
PQC Hyperledger Fabric Mock Data Generation Package

This package provides tools for generating realistic mock benchmark data
for Post-Quantum Cryptography (PQC) performance evaluation on Hyperledger Fabric.

Modules:
    - distributions: Statistical distributions for metric generation
    - samplers: Data sampling and generation logic
    - exporters: CSV export functionality

Version: 0.1.0 (MVP - Draft)
"""

__version__ = "0.1.0"
__author__ = "PQC Hyperledger Fabric Benchmark Team"

# Import existing modules to make them available when importing the package
from . import distributions
from . import samplers
from . import exporters

# Package metadata - only list modules that actually exist
__all__ = [
    "distributions",
    "samplers", 
    "exporters",
]
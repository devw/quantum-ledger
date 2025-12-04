from setuptools import setup, find_packages

setup(
    name="quantum_ledger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # runtime dependencies, copiate da requirements.txt
        "numpy>=1.21.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "pyyaml>=6.0",
    ],
)

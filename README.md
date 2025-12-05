# 🚀 Post-Quantum Hyperledger Fabric Benchmark

A research-oriented framework for evaluating the **performance impact of post-quantum cryptography (PQC)** on **Hyperledger Fabric**.

This repository supports experiments with **ECDSA**, **PQC-only**, and **Hybrid (ECDSA + PQC)** signing schemes to assess quantum-resilient transaction flows.

---

## 🎯 Purpose

This project provides a reproducible environment to:

* Benchmark PQC algorithms (Dilithium, Falcon, etc.) integrated into Fabric
* Measure performance impact on transaction latency, throughput, endorsement, and ordering
* Test hybrid cryptographic models for quantum-secure enterprise blockchains
* Support rigorous academic research with statistical analysis and reproducible experiments

---

## 📦 Key Features

* Docker-based reproducible Hyperledger Fabric network
* Pluggable cryptographic modules (ECDSA, PQC, Hybrid)
* Automated benchmarking through Hyperledger Caliper
* Multi-VM orchestration for distributed testing
* Comprehensive data collection and analysis pipeline
* Research-grade documentation and experiment protocols

---

## 📁 Project Structure

```
.
├── .gitignore                     # 🗑️ Files to ignore in Git
├── README.md                      # 📄 Project overview and entry point
├── requirements.txt               # 📦 Python dependencies for the project
│
├── analysis/                      # 📈 Data Analysis & Visualization
│   ├── figures/                   # Generated charts and graphs
│   ├── notebooks/                 # Jupyter notebooks for exploratory analysis
│   ├── README.md                  # Documentation for the analysis process
│   └── scripts/                   # Statistical analysis and table generation scripts
│
├── artifacts/                     # 📦 Build Outputs (gitignored)
│   # Empty, reserved for temporary build files
│
├── data/                          # 📊 Dataset Management
│   ├── fixtures/                  # Test data, config, and Monte Carlo seed configurations
│   ├── processed/                 # Cleaned and aggregated analysis-ready data
│   └── raw/                       # Raw benchmark outputs (CSV, logs)
│
├── docker/                        # 🐳 Container Infrastructure
│   ├── compose/                   # Docker Compose orchestration files
│   ├── configs/                   # Fabric network configurations
│   └── images/                    # Custom Dockerfiles (Fabric+PQC, Caliper)
│
├── docs/                          # 📚 Technical Documentation
│   ├── ARCHITECTURE.md            # System design and PQC integration points
│   ├── BENCHMARK_PROTOCOL.md      # Experimental methodology
│   ├── CRYPTOGRAPHIC_MODES.md     # ECDSA, PQC-only, and Hybrid specifications
│   ├── DATASET_SPECIFICATION.md   # Data format and naming conventions
│   ├── DEPLOYMENT_GUIDE.md        # Setup and installation instructions
│   ├── IMPLEMENTATION_NOTES.md    # Technical challenges and solutions
│   ├── METRICS_SPECIFICATION.md   # Performance metrics definitions
│   ├── README.md                  # Index for documentation
│   ├── RESULTS_ANALYSIS.md        # Statistical analysis guidelines
│   └── SCRIPTS_GUIDE.md           # Guide for custom scripts
│
├── simulations/                   # 🧪 Experimental Scenarios
│   ├── networks/                  # Network topology configurations
│   ├── README.md                  # Documentation for running simulations
│   ├── results/                   # Simulation outputs and preliminary data
│   └── scenarios/                 # Workload definitions (low/medium/high load)
│
├── src/                           # 💻 Core Application Code
│   ├── fabric/                    # Hyperledger Fabric modifications and chaincode
│   ├── pqc/                       # Post-quantum cryptographic implementations
│   └── sdk/                       # Client SDK extensions for PQC signing
│
├── tests/                         # ✅ Test Suites
│   ├── e2e/                       # End-to-end scenario validation tests
│   ├── integration/               # Integration tests for Fabric + PQC workflows
│   ├── README.md                  # Documentation for the test suite
│   └── unit/                      # Unit tests for PQC modules
│
├── tools/                         # ⚙️ Automation & Data Generation
│   ├── benchmark/                 # Caliper configurations and workload generators
│   ├── data_generation/           # Utilities for creating synthetic datasets (e.g., Monte Carlo)
│   ├── monitoring/                # Performance monitoring and logging utilities
│   └── scripts/                   # Deployment and utility scripts (e.g., generate_benchmark_data)
│
└── vm/                            # 🖥️ Virtual Machine Orchestration
    ├── ansible/                   # Ansible playbooks for automated deployment
    ├── inventory/                 # VM inventory and network topology definitions
    ├── provisioning/              # Vagrant/Terraform scripts for VM infrastructure
    └── README.md                  # Documentation for VM setup
```

---

## 🚀 Quick Start

### Prerequisites

* Docker 20.10+ and Docker Compose 2.0+
* Python 3.8+ (for analysis scripts)
* 16GB RAM minimum (32GB recommended for multi-node experiments)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pqc-fabric-benchmark.git
cd pqc-fabric-benchmark

# Deploy the Fabric network with ECDSA baseline
./tools/scripts/deploy-network.sh --mode ecdsa

# Run benchmark
./tools/scripts/run-benchmark.sh --workload low --duration 300

# Collect results
./tools/scripts/collect-data.sh --output data/raw/
```

For detailed setup instructions, see [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md).

---

## 🔬 Experimental Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **ECDSA** | Classical elliptic curve signatures | Performance baseline |
| **PQC-Only** | Pure post-quantum signatures (Dilithium, Falcon) | End-state quantum resistance |
| **Hybrid** | Dual ECDSA + PQC verification | Transition strategy evaluation |

See [`docs/CRYPTOGRAPHIC_MODES.md`](docs/CRYPTOGRAPHIC_MODES.md) for detailed specifications.

---

## 📊 Performance Metrics

* **Transaction throughput** (TPS)
* **End-to-end latency** (ms)
* **Signature generation/verification time** (μs)
* **Resource utilization** (CPU, RAM)
* **Block size and commit time**
* **Network overhead** (payload size)

Full metric definitions: [`docs/METRICS_SPECIFICATION.md`](docs/METRICS_SPECIFICATION.md)

---

## 📈 Data Analysis

Analysis workflows are available in [`analysis/`](analysis/):

```bash
# Generate summary statistics
python analysis/scripts/compute_statistics.py --input data/raw/ --output data/processed/

# Create visualizations
jupyter notebook analysis/notebooks/performance_comparison.ipynb
```

---

## 🧪 Running Experiments

```bash
# Run all cryptographic modes with multiple load profiles
./tools/scripts/run-experiments.sh --modes all --loads all --runs 5

# Analyze results
python analysis/scripts/generate_report.py --data data/raw/ --output analysis/figures/
```

See [`docs/BENCHMARK_PROTOCOL.md`](docs/BENCHMARK_PROTOCOL.md) for the complete experimental methodology.

---

## 📚 Documentation

Comprehensive technical documentation is available in [`docs/`](docs/):

* **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and integration approach
* **[CRYPTOGRAPHIC_MODES.md](docs/CRYPTOGRAPHIC_MODES.md)** - Detailed algorithm specifications
* **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Step-by-step setup instructions
* **[BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md)** - Experimental methodology
* **[DATASET_SPECIFICATION.md](docs/DATASET_SPECIFICATION.md)** - Data format and structure
* **[RESULTS_ANALYSIS.md](docs/RESULTS_ANALYSIS.md)** - Statistical analysis guidelines

---

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines and code of conduct.

---

## 📧 Contact

For questions or collaboration inquiries:

* **Email**: antonio.pierro@gmail.com
* **Issues**: [GitHub Issues](https://github.com/devw/quantum-ledger/issues)

<!-- ---

## 🎓 Citation

If you use this framework in your research, please cite:

```bibtex
@article{yourname2025pqc,
  title={Performance Analysis of Post-Quantum Cryptography in Hyperledger Fabric},
  author={Your Name and Co-authors},
  journal={Journal Name},
  year={2025}
}
``` -->

---

## 🙏 Acknowledgments

* Hyperledger Fabric community
* Open Quantum Safe (liboqs) project
* NIST Post-Quantum Cryptography Standardization initiative

---

## 📜 License

**CC BY-NC 4.0** – Free for non-commercial use. Commercial use requires written permission.

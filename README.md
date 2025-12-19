# 🚀 Post-Quantum Hyperledger Fabric Benchmark

A framework for evaluating the **performance impact of post-quantum cryptography (PQC)** on **Hyperledger Fabric**, supporting **ECDSA**, **PQC-only**, and **Hybrid** signing schemes.

---

## 🎯 Purpose

This project provides a reproducible environment to benchmark PQC algorithms, measure transaction performance, test hybrid cryptographic models, and support research with robust data and statistical analysis.

---

## 📦 Key Features

* Docker-based reproducible Fabric network
* Pluggable ECDSA, PQC, and Hybrid modules
* Automated benchmarking with Hyperledger Caliper
* Multi-VM orchestration
* Full data collection + analysis pipeline
* Academic-grade documentation

---

## 📁 Project Structure

```
.
├── README.md                     # 📄 Project overview
├── requirements*.txt             # 📦 Python dependencies
├── data/                         # 📊 Datasets and inputs
│   ├── fixtures/                 # 🧪 Test configs
│   ├── processed/                # 📈 Cleaned data
│   └── raw/                      # 📉 Raw benchmark outputs
├── docker/                       # 🐳 Fabric + Caliper containers
│   ├── compose/                  # ⚙️ Orchestration files
│   └── images/                   # 🧩 Custom Docker images
├── docs/                         # 📚 Technical documentation
├── simulations/                  # 🧪 Experimental setups
├── src/                          # 💻 Core source code
│   ├── fabric/                   # 🔗 Chaincode + Fabric mods
│   ├── pqc/                      # 🔐 PQC cryptographic modules
│   └── sdk/                      # 🛠️ Client SDK extensions
├── tests/                        # ✅ Unit + integration tests
└── tools/                        # 🔧 Benchmarking + analysis tools
```

---

## 🚀 Quick Start

**Prerequisites**: Docker 20.10+, Docker Compose 2.0+, Python 3.8+, 16GB RAM.

---

## 🔬 Experimental Modes

| Mode         | Description                     |
| ------------ | ------------------------------- |
| **ECDSA**    | Classical signatures (baseline) |
| **PQC-Only** | Dilithium, Falcon               |
| **Hybrid**   | Dual ECDSA + PQC verification   |

More details in `docs/CRYPTOGRAPHIC_MODES.md`.

---

## 📚 Documentation

Technical documentation available in `docs/`:

* [ARCHITECTURE.md](docs/ARCHITECTURE.md) – System design
* [BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md) – Experimental workflow
* [CRYPTOGRAPHIC_MODES.md](docs/CRYPTOGRAPHIC_MODES.md) – PQC schemes
* [DATASET_SPECIFICATION.md](docs/DATASET_SPECIFICATION.md) – Dataset structure
* [METRICS_SPECIFICATION.md](docs/METRICS_SPECIFICATION.md) – Metrics definitions
* [RESULTS_ANALYSIS.md](docs/RESULTS_ANALYSIS.md) – Statistical methods
* [SCRIPTS_GUIDE.md](docs/SCRIPTS_GUIDE.md) – Script usage

---

## 🤝 Contributing

Contributions are welcome via PRs and Issues.

---

## 📧 Contact

Email: [antonio.pierro@gmail.com](mailto:antonio.pierro@gmail.com)

---

## 📜 License

**CC BY-NC 4.0** – Free for non-commercial use.

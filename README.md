# 🚀 Post-Quantum Hyperledger Fabric Benchmark

Research framework for evaluating **Post-Quantum Cryptography (PQC)** performance impact on **Hyperledger Fabric**.

---

## 🎯 Overview

Reproducible environment for benchmarking quantum-resilient cryptographic schemes:

| Mode | Description | Use Case |
|:-----|:------------|:---------|
| 🔵 **ECDSA** | Baseline (P-256) | Performance reference |
| 🟣 **PQC-only** | Dilithium/Falcon | Pure quantum-resistant |
| 🟢 **Hybrid** | ECDSA + PQC | Transition strategy |

**→** Full methodology: [docs/BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md)

---

## 📊 Key Metrics

- **Throughput** (TPS), **Latency** (mean, P95)
- **Signature timings** (generation/verification)
- **Resource usage** (CPU/RAM), **Block size**

**→** Complete specifications: [docs/METRICS_SPECIFICATION.md](docs/METRICS_SPECIFICATION.md)

---

## 📚 Documentation

**Complete documentation available in [`docs/`](docs/README.md)**

| Document | Purpose |
|:---------|:--------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & PQC integration |
| [CRYPTOGRAPHIC_MODES.md](docs/CRYPTOGRAPHIC_MODES.md) | Crypto scheme comparison |
| [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Step-by-step setup |
| [BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md) | Testing methodology |
| [METRICS_SPECIFICATION.md](docs/METRICS_SPECIFICATION.md) | Performance metrics |
| [IMPLEMENTATION_NOTES.md](docs/IMPLEMENTATION_NOTES.md) | Technical details |
| [RESULTS_ANALYSIS.md](docs/RESULTS_ANALYSIS.md) | Data interpretation |

---

## 🧪 Research Context

This framework supports research on:
- Quantum-resilient signatures in permissioned blockchains
- Hybrid cryptography performance trade-offs
- PQC scalability in enterprise environments

*Paper reference will be added upon publication.*

---

## 🤝 Contributing

Contributions welcome! Areas of interest:
- New PQC algorithm integrations
- Additional benchmark scenarios
- Performance optimization techniques

---

## 📜 License

**CC BY-NC 4.0** – Free for non-commercial use. Commercial use requires written permission.

---

**🔗 Start here:** [docs/README.md](docs/README.md) | **🚀 Deploy:** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
# 🚀 Post-Quantum Hyperledger Fabric Benchmark

A research-oriented framework for evaluating the **performance impact of post-quantum cryptography (PQC)** on **Hyperledger Fabric**.
This repository supports experiments with **ECDSA**, **PQC-only**, and **Hybrid (ECDSA + PQC)** signing schemes to assess quantum-resilient transaction flows.

---

## 🎯 Purpose of This Project

This project provides a reproducible environment to:

* benchmark PQC algorithms (Dilithium, Falcon, etc.) integrated into Fabric
* measure performance impact on transaction latency, throughput, endorsement, and ordering
* test hybrid cryptographic models for quantum-secure enterprise blockchains
* support the experiments described in the associated research paper

---

## 📦 Features

* Docker-based reproducible Hyperledger Fabric network
* Pluggable cryptographic modules (ECDSA, PQC, Hybrid)
* Benchmarking through Hyperledger Caliper
* Scripts for automated data collection
* Preliminary PQC verification chaincode examples
* Experimental mode for testing PQC-only signatures

---

## 🧪 Experimental Architecture

### 🔐 Cryptographic Modes

* **ECDSA (baseline)**
* **Post-quantum signatures** (Dilithium / Falcon via liboqs or custom modules)
* **Hybrid signatures**: ECDSA + PQC verification inside chaincode

### 📊 Metrics Collected

* Transaction throughput (TPS)
* Transaction latency
* Peer and orderer CPU/RAM usage
* Signature generation and verification times
* Block size and commit time impact

---

## 🏗️ Repository Structure

```
/docs/              – Paper notes, architecture diagrams, design docs  
/network/           – Docker-based Fabric network configuration  
/crypto/            – PQC libraries, hybrid signing utilities  
/chaincode/         – Sample chaincodes including PQC verification  
/caliper/           – Benchmarking configurations and workload files  
/scripts/           – Automation scripts for experiments and data collection  
/results/           – Experimental results and plots  
```

---

## 🐳 Deployment (Quick Start)

1. Install Docker + Docker Compose
2. Launch the Fabric network
3. Deploy chaincode with PQC or hybrid verification
4. Run benchmarks with Caliper
5. Collect and analyze performance data

(Detailed instructions coming soon.)

---

## 📚 Research Context

This repository supports the experiments for a research study on:

* the feasibility of quantum-resilient signatures in Fabric
* the performance trade-offs of hybrid cryptography
* the scalability of PQC in enterprise blockchain environments

A link to the paper will be added once published.

---

## 🤝 Contributing

Contributions, suggestions, and extensions are welcome—especially new PQC integrations, chaincodes, or Caliper scenarios.

---

## 📜 License

This project is licensed under the **Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)** license.

You are free to use, modify, and share the code for **non-commercial purposes**.  
Commercial use requires **explicit written permission from the author**.




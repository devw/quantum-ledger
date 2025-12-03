# 📜 BENCHMARK PROTOCOL

This protocol defines the **standardized methodology** for performance evaluation of Post-Quantum Cryptography (PQC) integration into Hyperledger Fabric, ensuring **reproducibility** and **comparability** of results.

---

## ⚙️ Testbed & Configuration

The benchmark uses a controlled, standardized Fabric network deployed via Docker.

### Network Components
| Component | Count | Role/Configuration |
| :--- | :--- | :--- |
| **Organization** | 1 | Org1 |
| **Peer Nodes** | 2 | Endorsing peers (`peer0`, `peer1`). Endorsement Policy: $\text{AND}(\text{'Org1.peer'})$. |
| **Orderer** | 1 | Raft Orderer. |
| **Chaincode** | 1 | Simple Key-Value Store with PQC verification hooks. |

### Cryptographic Test Modes
All runs are performed across the following three modes (detailed in `CRYPTOGRAPHIC_MODES.md`):

1.  **Baseline (ECDSA):** Standard ECDSA (e.g., P-256).
2.  **PQC-only:** Pure Post-Quantum signing (e.g., Dilithium-3 or Falcon-512).
3.  **Hybrid:** Dual signing scheme (ECDSA + PQC).

### Workload Generator
**Hyperledger Caliper** is the mandated workload generator.

* **Workload:** Read-Write transactions (e.g., 50% reads, 50% writes).
* **Duration:** Minimum **300 seconds** of steady-state transaction submission.
* **Rates:** Incremental loads (e.g., 100, 200, 500, 1000 TPS) to determine the saturation point.
* **Repetitions:** Each unique test condition (Mode + Rate) must be run **$N \ge 5$ times** for statistical validity.

---

## 🎯 Performance Metrics

This benchmark captures the following categories of metrics:
- **Client-side performance** (TPS, Latency)
- **Micro-timing** (Signature operations, Block commit)
- **System resources** (CPU, RAM)
- **Ledger impact** (Block size)

**→ For detailed metric definitions, units, and collection methodology, 
see [METRICS_SPECIFICATION.md](METRICS_SPECIFICATION.md)**

---

## 🛠️ Execution Procedure

1.  **Preparation:** Deploy the standardized Fabric network and relevant chaincode.
2.  **Warm-up:** Run a brief (e.g., 60s) low-rate workload to stabilize the system.
3.  **Execution Loop:** For each Cryptographic Mode and Transaction Rate:
    * Execute the Caliper benchmark for 300+ seconds.
    * Simultaneously collect system resource metrics (CPU/RAM).
    * Collect custom micro-timing data (Sig Gen/Verify) via Fabric instrumentation/logs.
    * Repeat the run **$N \ge 5$ times**.
4.  **Reporting:** Analyze and average results across repetitions. Report on mean, P95 latency, and standard deviation.

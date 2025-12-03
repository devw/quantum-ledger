# 📊 METRICS SPECIFICATION

This document defines the core performance and resource metrics utilized by the benchmark framework. All results are reported based on runs repeated $\text{N} \ge 5$ times.

---

## 🔬 Core Performance Indicators

The following table synthesizes the required metrics, their source, and their primary focus for evaluating Post-Quantum Cryptography (PQC) impact on Hyperledger Fabric.

| Metric | Category | Unit | Statistical Measure | PQC Analysis Focus |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction Throughput (TPS)** | Client-Side | TPS | Mean | Overall capacity degradation due to PQC. |
| **Transaction Latency** | Client-Side | Seconds (s) | Mean, **P95**, $\sigma$ | End-to-end performance and user experience. |
| **Signature Generation Time** | Micro-Timing | Milliseconds (ms) | Mean | Isolates computational cost of PQC signing algorithm. |
| **Signature Verification Time** | Micro-Timing | Milliseconds (ms) | Mean | Isolates the crucial overhead of PQC verification at Peer/Orderer. |
| **Block Commit Time** | Micro-Timing | Milliseconds (ms) | Mean | Latency specifically linked to final validation and ledger write. |
| **Average Block Size** | Ledger Impact | Kilobytes (KB) | Mean | Quantifies the serialization overhead from larger PQC signatures. |
| **Peer/Orderer CPU Usage** | System Resource | Percentage (%) | Mean, Peak | Resource demand of PQC cryptographic functions. |
| **Peer/Orderer RAM Usage** | System Resource | Megabytes (MB) | Mean, Peak | Memory overhead for handling PQC keys and large signature objects. |

---

## 🛠️ Data Collection and Output Flows

The framework utilizes a dual-path data collection strategy to meet both real-time operational monitoring and high-granularity scientific analysis requirements.

### 1. **Data Sources and Acquisition**

* **Client Metrics:** Derived exclusively from Hyperledger Caliper reports.
* **Micro-Metrics:** Collected via internal instrumentation of Fabric's cryptographic functions (CSP).
* **System Metrics:** Captured using Docker API (`docker stats`) targeting individual Peer and Orderer containers to ensure resource isolation.

### 2. **Dual Output Flows**

#### 📈 Flow A: Aggregate Time Series for Operational Monitoring

* **Purpose:** Real-time visibility, system health checks, and dashboarding.
* **Format:** Metrics are exposed in the **Prometheus format** (plaintext endpoint) at regular scrape intervals (e.g., 5 seconds).
* **Consumption:** Prometheus serves as the time-series database (TSDB) backend for **Grafana** dashboards.

#### 💾 Flow B: Raw Data Logging for Scientific Analysis

* **Purpose:** To generate a comprehensive, high-resolution **public dataset** ensuring scientific reproducibility and enabling advanced statistical analysis (e.g., latency distribution fitting, outlier detection).
* **Granularity:** Data for **Micro-Timing** (Signature Time, Verification Time) and **Transaction Latency** are logged on a **per-operation basis** (i.e., every event is recorded).
* **Output:** The raw data log is structured (e.g., **JSON Lines** or a direct high-resolution CSV dump) to include the following minimum fields for each recorded event:
    * `Timestamp`
    * `MetricName`
    * `Value`
    * `Cryptosystem` (e.g., `dilithium3`, `ecdsa`, `hybrid`)
    * `OperationPhase` (e.g., `signing`, `verification`, `commit`)

* **Post-Processing:** This raw data log serves as the single source for generating the final **CSV Dataset** intended for the scientific community (as detailed in `RESULTS_ANALYSIS.md`).
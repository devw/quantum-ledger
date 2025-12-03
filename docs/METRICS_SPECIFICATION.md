# 📊 METRICS SPECIFICATION

This document defines the core performance and resource metrics utilized by the benchmark framework. All results are reported based on runs repeated $\text{N} \ge 5$ times.

-----

## 🔬 Core Performance Indicators

The following table synthesizes the required metrics, their source, and their primary focus for evaluating PQC impact on Hyperledger Fabric.

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

-----

## 🛠️ Data Collection Methodology

  * **Client Metrics:** Derived exclusively from Hyperledger Caliper reports.
  * **Micro-Metrics:** Collected via internal instrumentation of Fabric's cryptographic functions.
  * **System Metrics:** Captured using Docker API (`docker stats`) targeting individual Peer and Orderer containers to ensure resource isolation.


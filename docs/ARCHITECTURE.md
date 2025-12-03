# 🏗️ ARCHITECTURAL DESIGN SPECIFICATION

This document outlines the architectural modifications and components of the Post-Quantum Hyperledger Fabric Benchmark framework. The design prioritizes modularity and isolation to enable performance analysis of distinct cryptographic schemes.

---

## 🔌 Cryptographic Modularity: PQC Integration

This section details the architectural approach adopted for integrating Post-Quantum Cryptography (PQC) into Hyperledger Fabric, isolating the cryptographic implementation to enable reproducible performance comparison.

### 🛡️ CSP Abstraction Layer

Integration is achieved by leveraging Fabric's **Cryptographic Service Provider (CSP)** interface. The CSP acts as an abstraction layer for signature generation and verification. 

* **Key Principle:** The core Fabric consensus protocols interact with the CSP interface; thus, the **underlying cryptographic algorithm can be swapped** (e.g., from ECDSA to Dilithium) without altering the critical consensus logic (Endorsement, Ordering).

### 🧪 Implementation Modes and Focus

The framework uses specialized CSP back-ends to implement the distinct test scenarios:

| Mode | Underlying Cryptography | Signature Logic | Benchmark Focus |
| :--- | :--- | :--- | :--- |
| **PQC-only** | PQC (e.g., Dilithium) | Exclusive use; replaces all classical signatures. | Measures **pure computational cost** of quantum resistance. |
| **Hybrid** | ECDSA + PQC | Generates and verifies **dual signatures** per transaction. | Measures **transition overhead** and cost of maximum security. |

### 💾 Serialization Overhead (Impact)

The architecture must explicitly address the negative consequences of larger PQC signatures.

* **Mechanism:** Increased PQC signature size significantly inflates the **transaction envelope payload**.
* **Impact:** This results in **Serialization Overhead**, directly increasing average **Block Size**. This overhead is a critical metric, as it impacts networking propagation time and commitment latency, contributing significantly to overall throughput degradation.

---

## 🌐 Component Modification Summary

The integration primarily targets Fabric components responsible for cryptographic operations (signing and verification). The entire network is orchestrated using **Docker Compose** to ensure deterministic and reproducible test environments.

| Fabric Component | Primary PQC Function | Impacted Process |
| :--- | :--- | :--- |
| **Client SDK/Application** | Signature Generation | Signs transaction proposals with PQC/Hybrid scheme. |
| **Peer (Endorser)** | Verification & Signature Generation | Verifies client signature; signs endorsement response. |
| **Orderer Service** | Verification | Verifies endorsement signatures before block packaging. |
| **Peer (Committer)** | Final Verification | Validates transaction signatures against endorsement policy before commit. |

---

## 📈 Transaction Flow Implications

The architectural adjustments shift the primary computational bottleneck from standard networking to cryptographic processing. Key latency points in the PQC-enabled transaction flow are:

1.  **Endorsement:** High overhead due to both **PQC Signature Verification** (client proposal) and **PQC Signature Generation** (endorsement response).
2.  **Commitment:** High overhead resulting from the final block-wise **PQC Signature Verification** step against the required policy, directly impacting the final commit time.
# 🏗️ ARCHITECTURAL DESIGN SPECIFICATION

This document outlines the architectural modifications and components of the Post-Quantum Hyperledger Fabric Benchmark framework. The design prioritizes modularity and isolation to enable performance analysis of distinct cryptographic schemes.

---

## 🔌 Cryptographic Modularity

The framework achieves PQC integration by introducing a high-level **Cryptographic Service Provider (CSP)** abstraction layer. This layer encapsulates the signature generation and verification logic, allowing for the flexible interchange of cryptographic modes without altering the core Fabric consensus protocols.

* **PQC Implementation:** PQC algorithms (e.g., Dilithium, Falcon) are integrated as a specialized CSP implementation, managing the larger key and signature sizes inherent to lattice-based schemes.
* **Hybrid Mode:** The **Hybrid** scheme utilizes the CSP to generate and manage **dual signatures** (ECDSA + PQC) during the transaction endorsement and commitment stages.
* **Serialization Overhead:** The architecture specifically accounts for the increased data payload—particularly in the transaction envelopes—caused by larger PQC signatures, which directly impacts networking and block size. 

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
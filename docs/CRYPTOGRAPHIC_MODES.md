# 🔐 Cryptographic Modes

This document specifies the cryptographic configurations supported by the framework for evaluating post-quantum cryptography (PQC) integration in Hyperledger Fabric.

---

## 🎯 Overview

The framework implements three distinct cryptographic modes to assess the performance and security implications of quantum-resistant signatures in enterprise blockchain environments:

1. **ECDSA Baseline** - Classical elliptic curve signatures
2. **PQC-Only** - Pure post-quantum cryptographic signatures
3. **Hybrid** - Dual-signature scheme combining ECDSA and PQC

---

## 📊 Mode Specifications

### 🔵 ECDSA Baseline

**Purpose**: Establish performance baseline using standard Hyperledger Fabric cryptography.

**Algorithm**: Elliptic Curve Digital Signature Algorithm (ECDSA)
- **Curve**: secp256r1 (NIST P-256)
- **Key Size**: 256-bit private key
- **Signature Size**: ~72 bytes (DER-encoded)
- **Security Level**: 128-bit classical security

**Implementation**: Native Fabric BCCSP (Blockchain Cryptographic Service Provider) with software-based ECDSA.

**Use Case**: Reference point for measuring PQC overhead.

---

### 🟣 PQC-Only Mode

**Purpose**: Evaluate pure post-quantum signature schemes without classical cryptography.

**Supported Algorithms**:

#### Dilithium (CRYSTALS-Dilithium)
- **Dilithium2**: 
  - Public key: 1,312 bytes
  - Signature: ~2,420 bytes
  - Security: NIST Level 2 (~128-bit quantum security)
- **Dilithium3**: 
  - Public key: 1,952 bytes
  - Signature: ~3,293 bytes
  - Security: NIST Level 3 (~192-bit quantum security)
- **Dilithium5**: 
  - Public key: 2,592 bytes
  - Signature: ~4,595 bytes
  - Security: NIST Level 5 (~256-bit quantum security)

#### Falcon (Fast Fourier Lattice-based Compact Signatures)
- **Falcon-512**: 
  - Public key: 897 bytes
  - Signature: ~666 bytes
  - Security: NIST Level 1 (~128-bit quantum security)
- **Falcon-1024**: 
  - Public key: 1,793 bytes
  - Signature: ~1,280 bytes
  - Security: NIST Level 5 (~256-bit quantum security)

**Implementation**: Integration via liboqs (Open Quantum Safe) library or custom Fabric BCCSP plugin.

**Use Case**: Assess end-state quantum-resistant blockchain performance.

---

### 🟢 Hybrid Mode

**Purpose**: Enable gradual migration path with backward compatibility and defense-in-depth security.

**Design**: Dual-signature verification requiring **both** ECDSA and PQC signatures for transaction validity.

**Security Rationale**:
- Protection against quantum attacks (via PQC component)
- Resilience against potential PQC algorithm breaks (via ECDSA component)
- Maintains classical security guarantees during transition period

**Implementation Architecture**:

1. **Transaction Signing**: Client generates two signatures
   - ECDSA signature via standard Fabric SDK
   - PQC signature via extended signing module

2. **Chaincode Verification**: Custom chaincode logic validates both signatures
   - Extract transaction payload and dual signatures
   - Verify ECDSA signature against signer's classical public key
   - Verify PQC signature against signer's post-quantum public key
   - Transaction succeeds only if **both verifications pass**

3. **Identity Management**: Extended MSP (Membership Service Provider) structure
   - Traditional X.509 certificate with ECDSA public key
   - Additional PQC public key stored in certificate extension or separate registry

**Signature Format**:
```
HybridSignature = {
  ecdsa_signature: <72 bytes>,
  pqc_signature: <2420-4595 bytes depending on algorithm>,
  algorithm_id: <identifier>
}
```

**Total Signature Size**: ~2,500–4,700 bytes (vs. 72 bytes for ECDSA-only)

**Use Case**: Practical deployment scenario for enterprises requiring immediate quantum resistance without abandoning existing infrastructure.

---

## ⚙️ Configuration Parameters

Each mode is configurable via environment variables and Fabric configuration files:

| Parameter | ECDSA | PQC-Only | Hybrid |
|-----------|-------|----------|--------|
| `CRYPTO_MODE` | `ecdsa` | `pqc` | `hybrid` |
| `PQC_ALGORITHM` | N/A | `dilithium2/3/5` or `falcon512/1024` | Same as PQC-Only |
| `BCCSP_PROVIDER` | `SW` | `LIBOQS` | `HYBRID` |
| `SIGNATURE_POLICY` | Standard | PQC-native | Dual-verification |

---

## 🔬 Security Considerations

**ECDSA Baseline**: Vulnerable to quantum attacks via Shor's algorithm. Estimated to be broken by sufficiently large quantum computers (>4000 logical qubits).

**PQC-Only**: Quantum-resistant but relies on relatively new cryptographic assumptions. Potential for future cryptanalytic breakthroughs.

**Hybrid**: Secure if **at least one** signature scheme remains unbroken. Provides maximum security assurance during the post-quantum transition.

---

## 📈 Performance Trade-offs

| Metric | ECDSA | PQC-Only | Hybrid |
|--------|-------|----------|--------|
| Signature Size | ✅ Smallest | ⚠️ 30-60× larger | ⚠️ 35-65× larger |
| Verification Speed | ✅ Fastest | ⚠️ 2-10× slower | ❌ Slowest (dual) |
| Key Generation | ✅ Fast | ⚠️ Moderate | ⚠️ Moderate |
| Network Overhead | ✅ Minimal | ⚠️ Significant | ❌ Maximum |
| Quantum Security | ❌ None | ✅ Strong | ✅ Strong |
| Migration Risk | ❌ High | ⚠️ Moderate | ✅ Low |

---

## 🔄 Migration Path

Recommended enterprise adoption sequence:

1. **Phase 1**: ECDSA baseline (current state)
2. **Phase 2**: Hybrid deployment (transition period, 5-10 years)
3. **Phase 3**: PQC-only (post-quantum era, when quantum threat materializes)

The hybrid mode enables organizations to achieve quantum resistance immediately while maintaining operational continuity.

---

## 📚 References

- NIST Post-Quantum Cryptography Standardization (2024)
- CRYSTALS-Dilithium Specification (FIPS 204)
- Falcon Specification
- liboqs Documentation: https://openquantumsafe.org
- Hyperledger Fabric BCCSP Architecture
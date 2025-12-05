# 💾 DATASET SPECIFICATION FOR PQC BENCHMARK

## 📂 File Naming Convention

This specification defines the structure and naming protocol for the high-granularity **CSV Dataset** (Flow B), ensuring scientific traceability and reproducibility.

* **Format:** Compressed **CSV** (Comma Separated Values) file.
* **Protocol:** Files strictly adhere to: `<CRYPTO_MODE>_<LOAD_PROFILE>_RUN<N>.csv`.
    *Example File Names:* `ECDSA_LOWLOAD_RUN1.csv`, `DILITHIUM3_SUSTAINED_RUN5.csv`, `HYBRID_HIGHLOAD_RUN3.csv`.

### 🏷️ File Naming Component Specification

The following table defines the allowed categorical values used to construct the file names.

| Name | Role / Data Type | Possible Values (Examples) | Description |
| :--- | :--- | :--- | :--- |
| **`<CRYPTO_MODE>`** | File Name / Categorical String | `ECDSA`, `DILITHIUM3`, `HYBRID` | Cryptographic algorithm under test (Baseline or PQC Target). |
| **`<LOAD_PROFILE>`** | File Name / Categorical String | `LOWLOAD`, `MEDIUMLOAD`, `HIGHLOAD`, `SUSTAINED` | Concurrency and duration scenario used during the test. |
| **`RUN<N>`** | File Name / Integer | `RUN1` through `RUN5` ($\text{N} \ge 5$) | Sequential number of the benchmark repetition for statistical analysis. |

---

## 🎯 Load Profile Specifications

Load profiles define workload intensity in terms of target transactions per second (TPS).

| Load Profile | Target TPS | Range (TPS) | Variance | Duration | Use Case |
|--------------|------------|-------------|----------|----------|----------|
| **LOWLOAD** | 100 | 50-150 | ±10% | 5-10 min | Baseline performance measurement |
| **MEDIUMLOAD** | 300 | 200-400 | ±15% | 5-10 min | Normal operating conditions |
| **HIGHLOAD** | 600 | 500-800 | ±20% | 5-10 min | Peak capacity testing |
| **SUSTAINED** | 400 | 300-500 | ±15% | 30+ min | Long-term stability evaluation |

**Note:** Actual TPS achieved depends on `crypto_mode`:
- ECDSA: ~100% of target (baseline)
- DILITHIUM3: ~70% of target (PQC overhead)
- HYBRID: ~85% of target (combined overhead)

---

## 📊 Core Dataset Schema (Data Fields)

The published dataset is based on **per-operation log entries**. Each row represents a single cryptographic or transaction event. The following table defines the fields and their allowed values within the CSV file content.

| Column Name | Data Type | Unit | Description & **Allowed Values (Examples)** |
| :--- | :--- | :--- | :--- |
| **`timestamp_epoch_ms`** | Integer | Milliseconds (ms) | UNIX epoch time of the event recording. |
| **`latency_e2e_ms`** | Float | Milliseconds (ms) | End-to-end transaction latency (client submission to final commit). |
| **`time_sign_us`** | Float | Microseconds ($\mu s$) | Time taken for signature generation (**per-transaction average**). |
| **`time_verify_us`** | Float | Microseconds ($\mu s$) | Time taken for signature verification (**per-transaction average**). |
| **`payload_size_bytes`** | Integer | Bytes | Final size of the transaction payload (including signature). |
| **`run_id`** | Integer | N/A | Index of the benchmark run, corresponding to the `<N>` in the file name. |
| **`cryptosystem`** | Categorical String | N/A | Cryptographic algorithm used (Data Field). **Allowed Values:** `ECDSA`, `DILITHIUM3`, `HYBRID`. |
| **`operation_phase`** | Categorical String | N/A | Fabric processing stage. **Allowed Values:** `endorsement`, `validation`, `commit`. |

---

## 🔬 Cryptographic Timing Metrics

### Measurement Methodology

**`time_sign_us`** and **`time_verify_us`** represent **per-transaction averages** measured in microseconds (μs).

**Calculation:**
- For each sampling interval (typically 1 second):
  - Record all signature generation/verification operations
  - Compute mean timing per transaction
  - Report average in the CSV row

**Example calculation for ECDSA @ 100 TPS:**
```
tx_rate = 100 transactions/second
sig_gen_time = 85 μs (average per transaction)
sig_verify_time = 180 μs (average per transaction)

Total overhead per second:
  Generation: 100 × 85 = 8,500 μs = 8.5 ms
  Verification: 100 × 180 = 18,000 μs = 18 ms
```

### Expected Ranges by Crypto Mode

| Crypto Mode | `time_sign_us` | `time_verify_us` | Overhead vs ECDSA |
|-------------|----------------|------------------|-------------------|
| **ECDSA** | 50-150 | 100-250 | Baseline (1.0×) |
| **DILITHIUM3** | 200-500 | 800-1500 | 3-6× slower |
| **HYBRID** | 250-650 | 900-1750 | 4-7× slower |

**Crypto Tax Formula:**
```
crypto_tax (%) = (time_sign_us + time_verify_us) / (latency_e2e_ms × 1000) × 100
```

Expected values:
- ECDSA: 0.3-1.5% of total latency
- DILITHIUM3: 1-3% of total latency
- HYBRID: 1.5-3.5% of total latency
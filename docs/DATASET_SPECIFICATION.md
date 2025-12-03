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

## 📊 Core Dataset Schema (Data Fields)

The published dataset is based on **per-operation log entries**. Each row represents a single cryptographic or transaction event. The following table defines the fields and their allowed values within the CSV file content.

| Column Name | Data Type | Unit | Description & **Allowed Values (Examples)** |
| :--- | :--- | :--- | :--- |
| **`timestamp_epoch_ms`** | Integer | Milliseconds (ms) | UNIX epoch time of the event recording. |
| **`latency_e2e_ms`** | Float | Milliseconds (ms) | End-to-end transaction latency (client submission to final commit). |
| **`time_sign_us`** | Float | Microseconds ($\mu s$) | Time taken for signature generation. |
| **`time_verify_us`** | Float | Microseconds ($\mu s$) | Time taken for signature verification. |
| **`payload_size_bytes`** | Integer | Bytes | Final size of the transaction payload (including signature). |
| **`run_id`** | Integer | N/A | Index of the benchmark run, corresponding to the `<N>` in the file name. |
| **`cryptosystem`** | Categorical String | N/A | Cryptographic algorithm used (Data Field). **Allowed Values:** `ECDSA`, `DILITHIUM3`, `HYBRID`. |
| **`operation_phase`** | Categorical String | N/A | Fabric processing stage. **Allowed Values:** `endorsement`, `validation`, `commit`. |

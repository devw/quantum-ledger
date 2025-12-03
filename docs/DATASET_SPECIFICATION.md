# 💾 DATASET SPECIFICATION FOR PQC BENCHMARK

## 📂 File Naming Convention and Storage

This specification defines the structure of the high-granularity raw data log (Flow B) intended for public release to ensure scientific reproducibility and ease of analysis.

  * **Output Format:** Data is provided as a compressed **Comma Separated Values (CSV)** file.
  * **Encoding:** UTF-8 encoding is mandatory, with commas (`,`) as the field separator.
  * **Naming Protocol:** Files strictly adhere to the following convention to ensure traceability:
    ```
    <CRYPTO_MODE>_<LOAD_PROFILE>_RUN<N>.csv
    ```
    *Example:* `DILITHIUM3_STRESS_RUN3.csv`

-----

## 📊 Dataset Structure: Core Fields and Schema

The published dataset is based on **per-operation log entries**, capturing the full distribution of latency and overhead metrics. Each row in the CSV represents a single recorded cryptographic or transaction event.

| Column Name | Data Type | Unit | Description |
| :--- | :--- | :--- | :--- |
| **`timestamp_epoch_ms`** | Integer | Milliseconds (ms) | UNIX epoch time of the event recording. |
| **`latency_e2e_ms`** | Float | Milliseconds (ms) | End-to-end transaction latency (client submission to final commit). |
| **`time_sign_us`** | Float | Microseconds ($\mu s$) | Time taken for signature generation. |
| **`time_verify_us`** | Float | Microseconds ($\mu s$) | Time taken for signature verification. |
| **`cryptosystem`** | Categorical String | N/A | Algorithm used (`ECDSA`, `DILITHIUM3`, `HYBRID`). |
| **`operation_phase`** | Categorical String | N/A | Fabric processing stage (`endorsement`, `validation`, `commit`). |
| **`payload_size_bytes`** | Integer | Bytes | Final size of the transaction payload (including signature). |
| **`run_id`** | Integer | N/A | Index of the benchmark run ($\text{N}$). |

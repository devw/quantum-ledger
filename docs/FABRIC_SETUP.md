# 🏗️ Fabric Docker Setup Guide

Guide for setting up Hyperledger Fabric on Docker (Mac M4 / Apple Silicon).

---

## 📋 Prerequisites

- ✅ Docker Desktop installed and running
- ✅ Docker Compose v2+
- ✅ OpenSSL (pre-installed on Mac)

---

## 🔐 Step 1: Generate MSP Certificates

Hyperledger Fabric requires cryptographic material (certificates, keys) for authentication.

**What you need:**
- CA certificates (Certificate Authority)
- Private keys for peer and orderer
- Signed certificates for peer and orderer

**Generate with OpenSSL:**
```bash
# See scripts/setup-crypto.sh for detailed commands
./scripts/setup-crypto.sh
```

**Manual generation:** Use OpenSSL to create RSA 4096-bit keys and X.509 certificates for both peer and orderer organizations.

✅ **Verify:**
```bash
ls ./configs/peer0-org1/msp/{cacerts,keystore,signcerts}/
ls ./configs/orderer/msp/{cacerts,keystore,signcerts}/
```

⚠️ **Security:** Never commit `configs/*/msp/` to GitHub - these contain private keys!

---

## 📦 Step 2: Create Genesis Block

The genesis block initializes the orderer and defines the network configuration.

**Required file:** `configtx.yaml` - defines organizations, orderer settings, and channel policies.

**Generate genesis block:**
```bash
docker run --rm \
  -v $(pwd):/work \
  -w /work \
  hyperledger/fabric-tools:2.5 \
  configtxgen -profile Genesis \
  -channelID systemchannel \
  -outputBlock ./configs/orderer/genesis.block \
  -configPath .
```

🎯 This downloads `fabric-tools` image (~200MB, first time only) and generates the genesis block.

✅ **Verify:**
```bash
ls -lh ./configs/orderer/genesis.block
```

---

## ⚙️ Step 3: Configure Peer

**File:** `./configs/peer0-org1/core.yaml`

**Required configuration:**
- Peer identity and network settings
- **BCCSP (Blockchain Crypto Service Provider)** - defines cryptographic algorithms

**Key BCCSP settings:**
```yaml
peer:
  BCCSP:
    Default: SW
    SW:
      Hash: SHA2
      Security: 256
```

💡 Template files can be committed to GitHub - they contain no secrets.

---

## 🚀 Step 4: Launch Network

```bash
# Start the network
docker-compose -f fabric-baseline-ecdsa.yaml up -d

# Check status
docker ps

# View logs
docker logs peer0.org1.example.com
docker logs orderer.example.com
```

---

## 🛠️ Using fabric-tools

The `hyperledger/fabric-tools` image provides admin commands:

```bash
# Generic pattern
docker run --rm \
  -v $(pwd):/work \
  -w /work \
  hyperledger/fabric-tools:2.5 \
  <command> <args>
```

**Common tasks:**
- `configtxgen` - Generate genesis blocks and channel configs
- `cryptogen` - Generate crypto material (alternative to OpenSSL)
- `peer` - Peer admin commands
- `configtxlator` - Decode/encode Fabric configs

💡 Keep the image for future use or remove with: `docker rmi hyperledger/fabric-tools:2.5`

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot run peer because could not get peer BCCSP configuration` | Missing BCCSP in `core.yaml` | Add BCCSP section |
| `Setup error: nil conf reference` | Empty MSP directories | Regenerate certificates |
| `genesis block not found` | Missing genesis block | Run configtxgen |
| Containers stop immediately | Various config issues | Check logs: `docker logs <container>` |

**Debug commands:**
```bash
# View full logs
docker logs peer0.org1.example.com 2>&1 | grep -i error

# Verify certificate
openssl x509 -in ./configs/peer0-org1/msp/signcerts/*.pem -text -noout

# Check container mounts
docker inspect peer0.org1.example.com
```

---

## 📁 Directory Structure

```
compose/
├── configtx.yaml              # Network config (can commit)
├── fabric-baseline-ecdsa.yaml # Docker compose (can commit)
├── scripts/
│   └── setup-crypto.sh        # Crypto generation script (can commit)
└── configs/
    ├── peer0-org1/
    │   ├── core.yaml          # Peer config (can commit)
    │   └── msp/               # 🔒 NEVER COMMIT - contains private keys
    └── orderer/
        ├── genesis.block      # Generated - no need to commit
        └── msp/               # 🔒 NEVER COMMIT - contains private keys
```

**Add to `.gitignore`:**
```
configs/*/msp/
configs/orderer/genesis.block
```

---

## 🔄 Clean Up

```bash
# Stop and remove containers
docker-compose -f fabric-baseline-ecdsa.yaml down -v

# Remove generated crypto material (if needed)
rm -rf ./configs/*/msp/*
rm ./configs/orderer/genesis.block
```

---

## 📚 Resources

- [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/)
- [MSP Documentation](https://hyperledger-fabric.readthedocs.io/en/latest/msp.html)
- [Fabric CA](https://hyperledger-fabric-ca.readthedocs.io/)

---

**Platform:** Mac M4 (Apple Silicon) - using `platform: linux/amd64`  
**Fabric Version:** 2.5
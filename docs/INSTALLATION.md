Sì, ti suggerisco **`INSTALLATION.md`** nella root `docs/`.

# INSTALLATION.md

## Installation Guide

### Prerequisites

This project requires the following components:
- Go 1.22+
- liboqs (Open Quantum Safe library)
- Docker & Docker Compose
- CMake, Ninja, pkg-config

### Platform-Specific Installation

#### macOS (Apple Silicon M1/M2/M3/M4)

```bash
# Install dependencies via Homebrew
brew install go@1.22 cmake ninja openssl@3 pkg-config liboqs

# Configure environment
cat >> ~/.zshrc << 'EOF'
export PATH="/opt/homebrew/opt/go@1.22/bin:$PATH"
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
export CGO_ENABLED=1
export CGO_CFLAGS="-I/opt/homebrew/include"
export CGO_LDFLAGS="-L/opt/homebrew/lib"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
EOF

source ~/.zshrc
```

#### Linux (Ubuntu/Debian)

```bash
# Install Go
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Install build dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake ninja-build libssl-dev pkg-config

# Install liboqs from source
git clone --depth 1 --branch 0.10.1 https://github.com/open-quantum-safe/liboqs.git
cd liboqs && mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_SHARED_LIBS=ON ..
ninja && sudo ninja install && sudo ldconfig
```

### Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/quantum-ledger.git
cd quantum-ledger

# Initialize Go modules
go mod init github.com/yourusername/quantum-ledger

# Install Go dependencies
CGO_ENABLED=1 go get github.com/open-quantum-safe/liboqs-go/oqs@latest
go get github.com/hyperledger/fabric-protos-go-apiv2@latest
go get github.com/hyperledger/fabric-lib-go@latest
go mod tidy
```

### Verification

```bash
# Verify Go installation
go version

# Verify liboqs installation
pkg-config --modversion liboqs

# Test Dilithium3
go run -C tools/scripts verify_pqc.go
```

### Troubleshooting

**CGO errors on macOS:**
```bash
export CGO_ENABLED=1
export CGO_LDFLAGS="-L/opt/homebrew/lib"
export CGO_CFLAGS="-I/opt/homebrew/include"
```

**liboqs not found:**
```bash
# macOS
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"

# Linux
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
sudo ldconfig
```

### Next Steps

After successful installation, proceed to:
1. [FABRIC_SETUP.md](./FABRIC_SETUP.md) - Configure Hyperledger Fabric network
2. [CRYPTOGRAPHIC_MODES.md](./CRYPTOGRAPHIC_MODES.md) - Understand hybrid cryptography
3. [SCRIPTS_GUIDE.md](./SCRIPTS_GUIDE.md) - Run benchmarks
# Installation Guide

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Go | 1.22+ | Core runtime |
| liboqs | 0.10.1+ | Post-quantum cryptography |
| Docker | 20.10+ | Container orchestration |
| CMake | 3.18+ | Build system |
| pkg-config | - | Library configuration |

## Quick Start

### macOS (Apple Silicon)

```bash
# Install system dependencies
brew install go@1.22 cmake ninja openssl@3 pkg-config liboqs

# Configure environment (one-time)
tee -a ~/.zshrc << 'EOF'
export PATH="/opt/homebrew/opt/go@1.22/bin:$GOPATH/bin:$PATH"
export GOPATH=$HOME/go
export CGO_ENABLED=1
export CGO_CFLAGS="-I/opt/homebrew/include"
export CGO_LDFLAGS="-L/opt/homebrew/lib -loqs"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
EOF

# Create liboqs-go pkg-config wrapper
sudo tee /opt/homebrew/lib/pkgconfig/liboqs-go.pc << 'EOF'
prefix=/opt/homebrew
libdir=${prefix}/lib
includedir=${prefix}/include
Name: liboqs-go
Version: 0.15.0
Requires: liboqs
Cflags: -I${includedir}
Libs: -L${libdir} -loqs
EOF

source ~/.zshrc
```

### Linux (Ubuntu/Debian)

```bash
# Install Go
wget -qO- https://go.dev/dl/go1.22.0.linux-amd64.tar.gz | sudo tar -C /usr/local -xz
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc

# Install build tools
sudo apt-get update && sudo apt-get install -y \
    build-essential cmake ninja-build libssl-dev pkg-config git

# Build and install liboqs
git clone --depth 1 --branch 0.10.1 https://github.com/open-quantum-safe/liboqs.git /tmp/liboqs
cmake -S /tmp/liboqs -B /tmp/liboqs/build -GNinja \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DBUILD_SHARED_LIBS=ON
sudo cmake --build /tmp/liboqs/build --target install
sudo ldconfig

source ~/.bashrc
```

## Project Setup

```bash
# Clone and initialize
git clone https://github.com/yourusername/quantum-ledger.git
cd quantum-ledger

# Install Go dependencies
go mod download
go mod verify

# Build project
go build ./bccsp/hybrid/
go build ./...
```

## Verification

```bash
# System checks
go version                    # Expected: go1.22+
pkg-config --modversion liboqs # Expected: 0.10.1+
docker --version              # Expected: 20.10+

# Build verification
go build ./bccsp/hybrid/ && echo "✓ Hybrid BCCSP compiled"
go test ./bccsp/hybrid/ -v   # Run unit tests

# Runtime verification
go run -tags verify tools/scripts/verify_install.go
```

## Troubleshooting

### CGO Compilation Errors

```bash
# macOS: Verify Homebrew paths
ls -la /opt/homebrew/include/oqs/
ls -la /opt/homebrew/lib/liboqs.dylib

# Linux: Verify system paths
ldconfig -p | grep liboqs
pkg-config --cflags --libs liboqs

# Force rebuild with verbose output
CGO_ENABLED=1 go build -x ./bccsp/hybrid/
```

### Package Not Found

```bash
# Refresh pkg-config cache
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"  # macOS
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"    # Linux

# Verify liboqs-go.pc exists
pkg-config --list-all | grep liboqs
```

### Docker Issues

```bash
# Verify Docker daemon
docker info

# Check Docker Compose
docker-compose version

# Test container build
docker build -f docker/compose/Dockerfile.peer -t test-peer .
```

## Environment Variables Reference

| Variable | Value | Required For |
|----------|-------|--------------|
| `CGO_ENABLED` | `1` | All builds |
| `CGO_CFLAGS` | `-I/path/to/include` | liboqs headers |
| `CGO_LDFLAGS` | `-L/path/to/lib -loqs` | liboqs linking |
| `PKG_CONFIG_PATH` | `/path/to/pkgconfig` | pkg-config resolution |
| `GOPATH` | `$HOME/go` | Go workspace |

## Next Steps

| Documentation | Purpose |
|---------------|---------|
| [FABRIC_SETUP.md](./FABRIC_SETUP.md) | Deploy Hyperledger Fabric network |
| [CRYPTOGRAPHIC_MODES.md](./CRYPTOGRAPHIC_MODES.md) | Understand hybrid cryptography |
| [SCRIPTS_GUIDE.md](./SCRIPTS_GUIDE.md) | Run benchmarks and tests |

## Support

- **Issues**: Open GitHub issue with `[INSTALL]` prefix
- **Logs**: Include output from `go build -x` and `pkg-config --debug`
- **Environment**: Run `go env` and attach output
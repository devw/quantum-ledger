package hybrid

import (
	"fmt"
	"os"
	"hash"
	"github.com/hyperledger/fabric-lib-go/bccsp"
	"github.com/hyperledger/fabric-lib-go/bccsp/sw"
)

// HybridBCCSP implements BCCSP with hybrid ECDSA + ML-DSA-65 cryptography
type HybridBCCSP struct {
	sw bccsp.BCCSP
}

// New creates a new HybridBCCSP instance
func New() (bccsp.BCCSP, error) {
	swBCCSP, err := sw.NewDefaultSecurityLevel(os.TempDir())
	if err != nil {
		return nil, fmt.Errorf("failed to create SW BCCSP: %w", err)
	}
	return &HybridBCCSP{sw: swBCCSP}, nil
}

// KeyDeriv delegates to SW BCCSP
func (h *HybridBCCSP) KeyDeriv(k bccsp.Key, opts bccsp.KeyDerivOpts) (bccsp.Key, error) {
	return h.sw.KeyDeriv(k, opts)
}

// KeyImport delegates to SW BCCSP
func (h *HybridBCCSP) KeyImport(raw interface{}, opts bccsp.KeyImportOpts) (bccsp.Key, error) {
	return h.sw.KeyImport(raw, opts)
}

// GetKey delegates to SW BCCSP
func (h *HybridBCCSP) GetKey(ski []byte) (bccsp.Key, error) {
	return h.sw.GetKey(ski)
}

// Hash delegates to SW BCCSP
func (h *HybridBCCSP) Hash(msg []byte, opts bccsp.HashOpts) ([]byte, error) {
	return h.sw.Hash(msg, opts)
}

// GetHash delegates to SW BCCSP
func (h *HybridBCCSP) GetHash(opts bccsp.HashOpts) (hash.Hash, error) {
	return h.sw.GetHash(opts)
}

// Encrypt delegates to SW BCCSP
func (h *HybridBCCSP) Encrypt(k bccsp.Key, plaintext []byte, opts bccsp.EncrypterOpts) ([]byte, error) {
	return h.sw.Encrypt(k, plaintext, opts)
}

// Decrypt delegates to SW BCCSP
func (h *HybridBCCSP) Decrypt(k bccsp.Key, ciphertext []byte, opts bccsp.DecrypterOpts) ([]byte, error) {
	return h.sw.Decrypt(k, ciphertext, opts)
}
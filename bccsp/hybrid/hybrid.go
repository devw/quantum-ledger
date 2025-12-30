package hybrid

import (
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"fmt"

	"github.com/hyperledger/fabric-lib-go/bccsp"
	"github.com/hyperledger/fabric-lib-go/bccsp/sw"
	"github.com/open-quantum-safe/liboqs-go/oqs"
)

// HybridBCCSP implements BCCSP with hybrid ECDSA + Dilithium3 cryptography
type HybridBCCSP struct {
	sw bccsp.BCCSP // Software BCCSP for ECDSA operations
}

// hybridKey wraps both ECDSA and PQC keys
type hybridKey struct {
	ecdsaKey bccsp.Key
	pqcPub   []byte
	pqcPriv  []byte
}

func (k *hybridKey) Bytes() ([]byte, error) {
	return k.ecdsaKey.Bytes()
}

func (k *hybridKey) SKI() []byte {
	return k.ecdsaKey.SKI()
}

func (k *hybridKey) Symmetric() bool {
	return false
}

func (k *hybridKey) Private() bool {
	return k.ecdsaKey.Private()
}

func (k *hybridKey) PublicKey() (bccsp.Key, error) {
	ecdsaPub, err := k.ecdsaKey.PublicKey()
	if err != nil {
		return nil, err
	}
	return &hybridKey{
		ecdsaKey: ecdsaPub,
		pqcPub:   k.pqcPub,
		pqcPriv:  nil, // Public key has no private component
	}, nil
}

// New creates a new HybridBCCSP instance
func New() (bccsp.BCCSP, error) {
	swBCCSP, err := sw.NewDefaultSecurityLevel("")
	if err != nil {
		return nil, fmt.Errorf("failed to create SW BCCSP: %w", err)
	}
	return &HybridBCCSP{sw: swBCCSP}, nil
}

// KeyGen generates a hybrid key pair (ECDSA + Dilithium3)
func (h *HybridBCCSP) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
	// 1. Generate ECDSA key
	ecdsaKey, err := h.sw.KeyGen(opts)
	if err != nil {
		return nil, fmt.Errorf("ECDSA KeyGen failed: %w", err)
	}

	// 2. Generate Dilithium3 key pair
	signer := oqs.Signature{}
	defer signer.Clean()

	if err := signer.Init("Dilithium3", nil); err != nil {
		return nil, fmt.Errorf("Dilithium3 init failed: %w", err)
	}

	pqcPub, err := signer.GenerateKeypair()
	if err != nil {
		return nil, fmt.Errorf("Dilithium3 keygen failed: %w", err)
	}

	pqcPriv := signer.ExportSecretKey()

	return &hybridKey{
		ecdsaKey: ecdsaKey,
		pqcPub:   pqcPub,
		pqcPriv:  pqcPriv,
	}, nil
}

// KeyDeriv derives a key from another key
func (h *HybridBCCSP) KeyDeriv(k bccsp.Key, opts bccsp.KeyDerivOpts) (bccsp.Key, error) {
	return h.sw.KeyDeriv(k, opts)
}

// KeyImport imports a key from its raw representation
func (h *HybridBCCSP) KeyImport(raw interface{}, opts bccsp.KeyImportOpts) (bccsp.Key, error) {
	return h.sw.KeyImport(raw, opts)
}

// GetKey returns a key by its SKI
func (h *HybridBCCSP) GetKey(ski []byte) (bccsp.Key, error) {
	return h.sw.GetKey(ski)
}

// Hash hashes messages using the specified options
func (h *HybridBCCSP) Hash(msg []byte, opts bccsp.HashOpts) ([]byte, error) {
	return h.sw.Hash(msg, opts)
}

// GetHash returns a hash instance
func (h *HybridBCCSP) GetHash(opts bccsp.HashOpts) (hash.Hash, error) {
	return h.sw.GetHash(opts)
}

// Sign creates a hybrid signature (ECDSA + Dilithium3)
func (h *HybridBCCSP) Sign(k bccsp.Key, digest []byte, opts bccsp.SignerOpts) ([]byte, error) {
	hk, ok := k.(*hybridKey)
	if !ok {
		// Fallback to pure ECDSA for non-hybrid keys
		return h.sw.Sign(k, digest, opts)
	}

	// 1. Sign with ECDSA
	ecdsaSig, err := h.sw.Sign(hk.ecdsaKey, digest, opts)
	if err != nil {
		return nil, fmt.Errorf("ECDSA sign failed: %w", err)
	}

	// 2. Sign with Dilithium3
	signer := oqs.Signature{}
	defer signer.Clean()

	if err := signer.Init("Dilithium3", hk.pqcPriv); err != nil {
		return nil, fmt.Errorf("Dilithium3 init failed: %w", err)
	}

	pqcSig, err := signer.Sign(digest)
	if err != nil {
		return nil, fmt.Errorf("Dilithium3 sign failed: %w", err)
	}

	// 3. Combine signatures: [4 bytes ECDSA len][ECDSA sig][PQC sig]
	return combineSignatures(ecdsaSig, pqcSig), nil
}

// Verify verifies a hybrid signature
func (h *HybridBCCSP) Verify(k bccsp.Key, signature, digest []byte, opts bccsp.SignerOpts) (bool, error) {
	hk, ok := k.(*hybridKey)
	if !ok {
		// Fallback to pure ECDSA
		return h.sw.Verify(k, signature, digest, opts)
	}

	// 1. Parse combined signature
	ecdsaSig, pqcSig, err := parseHybridSignature(signature)
	if err != nil {
		return false, fmt.Errorf("parse signature failed: %w", err)
	}

	// 2. Verify ECDSA
	validECDSA, err := h.sw.Verify(hk.ecdsaKey, ecdsaSig, digest, opts)
	if err != nil || !validECDSA {
		return false, fmt.Errorf("ECDSA verify failed: %w", err)
	}

	// 3. Verify Dilithium3
	signer := oqs.Signature{}
	defer signer.Clean()

	if err := signer.Init("Dilithium3", nil); err != nil {
		return false, fmt.Errorf("Dilithium3 init failed: %w", err)
	}

	validPQC, err := signer.Verify(digest, pqcSig, hk.pqcPub)
	if err != nil {
		return false, fmt.Errorf("Dilithium3 verify failed: %w", err)
	}

	// Both must be valid
	return validECDSA && validPQC, nil
}

// Encrypt encrypts plaintext (delegates to SW BCCSP)
func (h *HybridBCCSP) Encrypt(k bccsp.Key, plaintext []byte, opts bccsp.EncrypterOpts) ([]byte, error) {
	return h.sw.Encrypt(k, plaintext, opts)
}

// Decrypt decrypts ciphertext (delegates to SW BCCSP)
func (h *HybridBCCSP) Decrypt(k bccsp.Key, ciphertext []byte, opts bccsp.DecrypterOpts) ([]byte, error) {
	return h.sw.Decrypt(k, ciphertext, opts)
}

// Helper functions

// combineSignatures creates: [4 bytes ECDSA len][ECDSA sig][PQC sig]
func combineSignatures(ecdsaSig, pqcSig []byte) []byte {
	lenBuf := make([]byte, 4)
	binary.BigEndian.PutUint32(lenBuf, uint32(len(ecdsaSig)))
	
	combined := make([]byte, 0, 4+len(ecdsaSig)+len(pqcSig))
	combined = append(combined, lenBuf...)
	combined = append(combined, ecdsaSig...)
	combined = append(combined, pqcSig...)
	
	return combined
}

// parseHybridSignature splits combined signature
func parseHybridSignature(signature []byte) (ecdsaSig, pqcSig []byte, err error) {
	if len(signature) < 4 {
		return nil, nil, errors.New("signature too short")
	}

	ecdsaLen := binary.BigEndian.Uint32(signature[:4])
	if len(signature) < int(4+ecdsaLen) {
		return nil, nil, errors.New("invalid signature format")
	}

	ecdsaSig = signature[4 : 4+ecdsaLen]
	pqcSig = signature[4+ecdsaLen:]

	return ecdsaSig, pqcSig, nil
}
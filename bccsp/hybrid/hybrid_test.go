package hybrid

import (
	"crypto/sha256"
	"testing"

	"github.com/hyperledger/fabric-lib-go/bccsp"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew(t *testing.T) {
	bccsp, err := New()
	require.NoError(t, err, "Failed to create HybridBCCSP")
	require.NotNil(t, bccsp, "HybridBCCSP should not be nil")
}

func TestKeyGen(t *testing.T) {
	h, err := New()
	require.NoError(t, err)

	// Use ECDSA P256 key generation
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}
	
	key, err := h.KeyGen(opts)
	require.NoError(t, err, "KeyGen should succeed")
	require.NotNil(t, key, "Generated key should not be nil")

	// Verify it's a hybrid key
	hk, ok := key.(*hybridKey)
	require.True(t, ok, "Key should be hybridKey type")
	assert.NotNil(t, hk.ecdsaKey, "ECDSA key should be present")
	assert.NotEmpty(t, hk.pqcPub, "PQC public key should be present")
	assert.NotEmpty(t, hk.pqcPriv, "PQC private key should be present")

	// Verify key properties
	assert.False(t, key.Symmetric(), "Key should be asymmetric")
	assert.True(t, key.Private(), "Key should be private")
	assert.NotEmpty(t, key.SKI(), "SKI should not be empty")
}

func TestSignVerify(t *testing.T) {
	h, err := New()
	require.NoError(t, err)

	// Generate key
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}
	key, err := h.KeyGen(opts)
	require.NoError(t, err)

	// Message to sign
	message := []byte("Hello, Post-Quantum World!")
	digest := sha256.Sum256(message)

	// Sign
	signature, err := h.Sign(key, digest[:], nil)
	require.NoError(t, err, "Sign should succeed")
	require.NotEmpty(t, signature, "Signature should not be empty")

	// Verify signature format: [4 bytes len][ECDSA sig][PQC sig]
	assert.GreaterOrEqual(t, len(signature), 4, "Signature should have at least length prefix")

	// Extract public key
	pubKey, _ := key.PublicKey()
	// Verify
	valid, err := h.Verify(pubKey, signature, digest[:], nil)
	if err != nil {
		t.Logf("Verify error: %v", err)
	}
	t.Logf("Valid: %v, Error: %v", valid, err)
	require.NoError(t, err, "Verify should not error")
	assert.True(t, valid, "Signature should be valid")

	// Test with tampered digest
	tamperedDigest := make([]byte, len(digest))
	copy(tamperedDigest, digest[:])
	tamperedDigest[0] ^= 0xFF

	valid, err = h.Verify(key, signature, tamperedDigest, nil)
	assert.False(t, valid, "Tampered digest should fail verification")

	// Test with tampered signature
	tamperedSig := make([]byte, len(signature))
	copy(tamperedSig, signature)
	tamperedSig[len(tamperedSig)-1] ^= 0xFF

	valid, err = h.Verify(key, tamperedSig, digest[:], nil)
	assert.False(t, valid, "Tampered signature should fail verification")
}

func TestPublicKey(t *testing.T) {
	h, err := New()
	require.NoError(t, err)

	// Generate private key
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}
	privKey, err := h.KeyGen(opts)
	require.NoError(t, err)

	// Extract public key
	pubKey, err := privKey.PublicKey()
	require.NoError(t, err, "PublicKey extraction should succeed")
	require.NotNil(t, pubKey, "Public key should not be nil")

	hk, ok := pubKey.(*hybridKey)
	require.True(t, ok, "Public key should be hybridKey type")
	assert.NotNil(t, hk.ecdsaKey, "ECDSA public key should be present")
	assert.NotEmpty(t, hk.pqcPub, "PQC public key should be present")
	assert.Nil(t, hk.pqcPriv, "PQC private key should be nil in public key")

	// Verify public key properties
	assert.False(t, pubKey.Private(), "Public key should not be private")
}

func TestSignatureFormat(t *testing.T) {
	// Test combineSignatures
	ecdsaSig := []byte("ecdsa_signature_data")
	pqcSig := []byte("pqc_signature_data")

	combined := combineSignatures(ecdsaSig, pqcSig)

	// Verify length prefix
	require.GreaterOrEqual(t, len(combined), 4, "Combined signature should have length prefix")

	// Parse and verify
	parsedECDSA, parsedPQC, err := parseHybridSignature(combined)
	require.NoError(t, err, "Parse should succeed")
	assert.Equal(t, ecdsaSig, parsedECDSA, "ECDSA signature should match")
	assert.Equal(t, pqcSig, parsedPQC, "PQC signature should match")
}

func TestParseInvalidSignature(t *testing.T) {
	// Test with too short signature
	_, _, err := parseHybridSignature([]byte{0x01, 0x02})
	assert.Error(t, err, "Should error on short signature")

	// Test with invalid length prefix
	invalidSig := []byte{0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x02}
	_, _, err = parseHybridSignature(invalidSig)
	assert.Error(t, err, "Should error on invalid length")
}

func TestHash(t *testing.T) {
	h, err := New()
	require.NoError(t, err)

	message := []byte("test message")
	opts := &bccsp.SHA256Opts{}

	hash, err := h.Hash(message, opts)
	require.NoError(t, err, "Hash should succeed")
	assert.NotEmpty(t, hash, "Hash should not be empty")

	// Verify hash length (SHA256 = 32 bytes)
	assert.Equal(t, 32, len(hash), "SHA256 hash should be 32 bytes")
}

func TestKeyGenDifferentKeys(t *testing.T) {
	h, err := New()
	require.NoError(t, err)

	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}

	// Generate two keys
	key1, err := h.KeyGen(opts)
	require.NoError(t, err)

	key2, err := h.KeyGen(opts)
	require.NoError(t, err)

	// Keys should be different
	assert.NotEqual(t, key1.SKI(), key2.SKI(), "Different keys should have different SKIs")

	hk1 := key1.(*hybridKey)
	hk2 := key2.(*hybridKey)
	assert.NotEqual(t, hk1.pqcPub, hk2.pqcPub, "PQC public keys should be different")
}

func BenchmarkKeyGen(b *testing.B) {
	h, _ := New()
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = h.KeyGen(opts)
	}
}

func BenchmarkSign(b *testing.B) {
	h, _ := New()
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}
	key, _ := h.KeyGen(opts)

	message := []byte("benchmark message")
	digest := sha256.Sum256(message)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = h.Sign(key, digest[:], nil)
	}
}

func BenchmarkVerify(b *testing.B) {
	h, _ := New()
	opts := &bccsp.ECDSAP256KeyGenOpts{Temporary: true}
	key, _ := h.KeyGen(opts)

	message := []byte("benchmark message")
	digest := sha256.Sum256(message)
	signature, _ := h.Sign(key, digest[:], nil)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = h.Verify(key, signature, digest[:], nil)
	}
}

func TestPQCSigner(t *testing.T) {
	signer, err := NewPQCSigner()
	if err != nil {
		t.Fatalf("failed to create signer: %v", err)
	}

	msg := []byte("hello pqc")
	sig := signer.Sign(msg)

	if !signer.Verify(msg, sig) {
		t.Fatal("signature verification failed")
	}
}

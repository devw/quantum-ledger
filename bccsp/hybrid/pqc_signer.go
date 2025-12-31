package hybrid

import (
	"fmt"

	"github.com/open-quantum-safe/liboqs-go/oqs"
)

// PQCAlgorithm da usare
const PQCAlgorithm = "Dilithium2"

// PQCSigner wrap del signer PQC
type PQCSigner struct {
	signer oqs.Signature
}

// NewPQCSigner crea un signer con nuova coppia di chiavi
func NewPQCSigner() (*PQCSigner, error) {
	signer := oqs.Signature{}
	if err := signer.Init(PQCAlgorithm, nil); err != nil {
		return nil, fmt.Errorf("failed to init PQC signer: %w", err)
	}
	return &PQCSigner{signer: signer}, nil
}

// NewPQCSignerFromPrivate crea un signer da chiave privata esistente
func NewPQCSignerFromPrivate(privKey []byte) (*PQCSigner, error) {
	signer := oqs.Signature{}
	if err := signer.Init(PQCAlgorithm, privKey); err != nil {
		return nil, fmt.Errorf("failed to init PQC signer with private key: %w", err)
	}
	return &PQCSigner{signer: signer}, nil
}

// Sign firma il messaggio
func (p *PQCSigner) Sign(msg []byte) ([]byte, error) {
	sig, err := p.signer.Sign(msg)
	if err != nil {
		return nil, fmt.Errorf("PQC signature failed: %w", err)
	}
	return sig, nil
}

// Verify verifica la firma
func (p *PQCSigner) Verify(msg, sig []byte) (bool, error) {
	valid, err := p.signer.Verify(msg, sig)
	if err != nil {
		return false, fmt.Errorf("PQC verification failed: %w", err)
	}
	return valid, nil
}

// PublicKey restituisce la chiave pubblica
func (p *PQCSigner) PublicKey() []byte {
	return p.signer.ExportPublicKey()
}

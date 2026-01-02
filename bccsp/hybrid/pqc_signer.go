// ./bccsp/hybrid/pqc_signer.go
package hybrid

import (
	"fmt"
	"github.com/open-quantum-safe/liboqs-go/oqs"
)

// PQCAlgorithm da usare - ML-DSA-65 è il nome standard NIST per Dilithium3
const PQCAlgorithm = "ML-DSA-65"

// PQCSigner wrap del signer PQC
type PQCSigner struct {
	signer    oqs.Signature
	publicKey []byte
}

// NewPQCSigner crea un signer con nuova coppia di chiavi
func NewPQCSigner() (*PQCSigner, error) {
	signer := oqs.Signature{}
	if err := signer.Init(PQCAlgorithm, nil); err != nil {
		return nil, fmt.Errorf("failed to init PQC signer: %w", err)
	}
	
	// Genera la coppia di chiavi
	pubKey, err := signer.GenerateKeyPair()
	if err != nil {
		signer.Clean()
		return nil, fmt.Errorf("failed to generate key pair: %w", err)
	}
	
	return &PQCSigner{
		signer:    signer,
		publicKey: pubKey,
	}, nil
}

// NewPQCSignerFromPrivate crea un signer da chiave privata esistente
func NewPQCSignerFromPrivate(privKey []byte) (*PQCSigner, error) {
	signer := oqs.Signature{}
	if err := signer.Init(PQCAlgorithm, privKey); err != nil {
		return nil, fmt.Errorf("failed to init PQC signer with private key: %w", err)
	}
	
	// Ricostruisci la chiave pubblica dalla privata (se possibile)
	// Potrebbe servire passarla come parametro separato
	return &PQCSigner{
		signer:    signer,
		publicKey: nil, // TODO: passare come parametro
	}, nil
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
	return p.signer.Verify(msg, sig, p.publicKey)
}

// PublicKey restituisce la chiave pubblica
func (p *PQCSigner) PublicKey() []byte {
	return p.publicKey
}

// Clean libera le risorse
func (p *PQCSigner) Clean() {
	p.signer.Clean()
}
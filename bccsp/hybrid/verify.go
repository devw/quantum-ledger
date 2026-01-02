// ./bccsp/hybrid/verify.go
package hybrid

import (
	"fmt"
	"github.com/hyperledger/fabric-lib-go/bccsp"
	"github.com/open-quantum-safe/liboqs-go/oqs"
)

// Verify verifica la firma ibrida
func (h *HybridBCCSP) Verify(k bccsp.Key, signature, digest []byte, opts bccsp.SignerOpts) (bool, error) {
	key, ok := k.(*hybridKey)
	if !ok {
		return false, fmt.Errorf("invalid key type, expected *hybridKey")
	}
	
	// Verifica che abbiamo la chiave pubblica PQC
	if len(key.pqcPub) == 0 {
		return false, fmt.Errorf("PQC public key is empty")
	}
	
	// Crea un verifier PQC temporaneo per la verifica
	// (la verifica richiede solo la chiave pubblica)
	signer := oqs.Signature{}
	if err := signer.Init(PQCAlgorithm, nil); err != nil {
		return false, fmt.Errorf("failed to init PQC verifier: %w", err)
	}
	defer signer.Clean()
	
	// PQC verification usando la chiave pubblica
	valid, err := signer.Verify(digest, signature, key.pqcPub)
	if err != nil {
		return false, fmt.Errorf("PQC verification failed: %w", err)
	}
	
	return valid, nil
}
package hybrid

import (
	"fmt"
	"github.com/hyperledger/fabric-lib-go/bccsp"
)

// Verify verifica la firma ibrida
func (h *HybridBCCSP) Verify(k bccsp.Key, signature, digest []byte, opts bccsp.SignerOpts) (bool, error) {
	key, ok := k.(*hybridKey)
	if !ok {
		return false, fmt.Errorf("invalid key type, expected *hybridKey")
	}
	
	// PQC verification con gestione errore
	valid, err := key.pqcPriv.Verify(digest, signature)
	if err != nil {
		return false, fmt.Errorf("PQC verification failed: %w", err)
	}
	
	return valid, nil
}
// ./bccsp/hybrid/sign.go
package hybrid

import (
	"fmt"
	"github.com/hyperledger/fabric-lib-go/bccsp"
)

// Sign firma un messaggio con la chiave ibrida
func (h *HybridBCCSP) Sign(k bccsp.Key, digest []byte, opts bccsp.SignerOpts) ([]byte, error) {
	key, ok := k.(*hybridKey)
	if !ok {
		return nil, fmt.Errorf("invalid key type, expected *hybridKey")
	}

	// PQC signature con gestione errore
	pqcSig, err := key.pqcPriv.Sign(digest)
	if err != nil {
		return nil, fmt.Errorf("PQC signature failed: %w", err)
	}
	
	return pqcSig, nil
}
package hybrid

import (
	"fmt"

	"github.com/hyperledger/fabric-lib-go/bccsp"
)

// KeyGen genera una chiave ibrida (ECDSA + PQC)
func (h *HybridBCCSP) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
	// 1️⃣ ECDSA
	ecdsaKey, err := h.sw.KeyGen(opts)
	if err != nil {
		return nil, fmt.Errorf("ECDSA KeyGen failed: %w", err)
	}

	// 2️⃣ PQC
	pqcSigner, err := NewPQCSigner()
	if err != nil {
		return nil, fmt.Errorf("PQC KeyGen failed: %w", err)
	}

	// 3️⃣ hybridKey
	return &hybridKey{
		ecdsaKey: ecdsaKey,
		pqcPub:   pqcSigner.PublicKey(),
		pqcPriv:  pqcSigner, // memorizziamo il signer completo
	}, nil
}

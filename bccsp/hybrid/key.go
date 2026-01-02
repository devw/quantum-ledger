// key.go
package hybrid

import (
	"github.com/hyperledger/fabric-lib-go/bccsp"
)

// hybridKey wraps both ECDSA and PQC keys
type hybridKey struct {
	ecdsaKey bccsp.Key
	pqcPriv  *PQCSigner
	pqcPub   []byte
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

// HasPrivateKey checks if this key contains private key material
func (k *hybridKey) HasPrivateKey() bool {
	return k.pqcPriv != nil
}
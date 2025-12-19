package hybrid

import (
    "github.com/hyperledger/fabric/bccsp"
    "github.com/hyperledger/fabric/bccsp/factory"
)

// HybridBCCSP è uno stub che per ora usa solo il provider SW (ECDSA)
type HybridBCCSP struct {
    sw bccsp.BCCSP
}

// Sign chiama solo il provider SW (ECDSA) per ora
func (h *HybridBCCSP) Sign(k bccsp.Key, digest []byte, opts bccsp.SignerOpts) ([]byte, error) {
    return h.sw.Sign(k, digest, opts)
}

// Verify chiama solo SW (ECDSA) per ora
func (h *HybridBCCSP) Verify(k bccsp.Key, signature, digest []byte, opts bccsp.SignerOpts) (bool, error) {
    return h.sw.Verify(k, signature, digest, opts)
}

// Hash chiama solo SW per ora
func (h *HybridBCCSP) Hash(msg []byte, opts bccsp.HashOpts) ([]byte, error) {
    return h.sw.Hash(msg, opts)
}

// KeyGen chiama solo SW per ora
func (h *HybridBCCSP) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
    return h.sw.KeyGen(opts)
}

// Derive chiama solo SW per ora
func (h *HybridBCCSP) Derive(k bccsp.Key, opts bccsp.KeyDerivOpts) (bccsp.Key, error) {
    return h.sw.Derive(k, opts)
}

// Import chiama solo SW per ora
func (h *HybridBCCSP) Import(raw interface{}, opts bccsp.ImportOpts) (bccsp.Key, error) {
    return h.sw.Import(raw, opts)
}

// Inizializza il provider HYBRID nel factory BCCSP
func init() {
    factory.Register("HYBRID", func(conf *factory.FactoryOpts) (bccsp.BCCSP, error) {
        sw, err := factory.GetBCCSPFromOpts(&conf.SwOpts)
        if err != nil {
            return nil, err
        }
        return &HybridBCCSP{sw: sw}, nil
    })
}

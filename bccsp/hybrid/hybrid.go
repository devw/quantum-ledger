package hybrid

import (
	"hash"

	"github.com/hyperledger/fabric/bccsp"
)

// HybridBCCSP è uno stub che per ora delega tutto al provider SW (ECDSA)
type HybridBCCSP struct {
	sw bccsp.BCCSP
}

// NewHybridBCCSP crea una nuova istanza del provider HYBRID
func NewHybridBCCSP(sw bccsp.BCCSP) *HybridBCCSP {
	return &HybridBCCSP{sw: sw}
}

// KeyGen genera una chiave usando il provider SW
func (h *HybridBCCSP) KeyGen(opts bccsp.KeyGenOpts) (bccsp.Key, error) {
	return h.sw.KeyGen(opts)
}

// KeyDeriv deriva una chiave da un'altra
func (h *HybridBCCSP) KeyDeriv(k bccsp.Key, opts bccsp.KeyDerivOpts) (bccsp.Key, error) {
	return h.sw.KeyDeriv(k, opts)
}

// KeyImport importa una chiave raw
func (h *HybridBCCSP) KeyImport(raw interface{}, opts bccsp.KeyImportOpts) (bccsp.Key, error) {
	return h.sw.KeyImport(raw, opts)
}

// GetKey ritorna una chiave usando il suo SKI
func (h *HybridBCCSP) GetKey(ski []byte) (bccsp.Key, error) {
	return h.sw.GetKey(ski)
}

// Hash calcola l'hash di un messaggio
func (h *HybridBCCSP) Hash(msg []byte, opts bccsp.HashOpts) ([]byte, error) {
	return h.sw.Hash(msg, opts)
}

// GetHash ritorna una nuova istanza di hash
func (h *HybridBCCSP) GetHash(opts bccsp.HashOpts) (hash.Hash, error) {
	return h.sw.GetHash(opts)
}

// Sign firma un digest usando il provider SW
func (h *HybridBCCSP) Sign(k bccsp.Key, digest []byte, opts bccsp.SignerOpts) ([]byte, error) {
	return h.sw.Sign(k, digest, opts)
}

// Verify verifica una firma usando il provider SW
func (h *HybridBCCSP) Verify(k bccsp.Key, signature, digest []byte, opts bccsp.SignerOpts) (bool, error) {
	return h.sw.Verify(k, signature, digest, opts)
}

// Encrypt cifra un plaintext
func (h *HybridBCCSP) Encrypt(k bccsp.Key, plaintext []byte, opts bccsp.EncrypterOpts) ([]byte, error) {
	return h.sw.Encrypt(k, plaintext, opts)
}

// Decrypt decifra un ciphertext
func (h *HybridBCCSP) Decrypt(k bccsp.Key, ciphertext []byte, opts bccsp.DecrypterOpts) ([]byte, error) {
	return h.sw.Decrypt(k, ciphertext, opts)
}

// Inizializzazione del provider nel factory BCCSP
func init() {
	// Register viene chiamato automaticamente all'avvio
	// Nota: in Fabric 2.5, la registrazione avviene tramite il meccanismo dei plugin
	// Per ora, il provider verrà caricato manualmente nel main del peer
}

// GetBCCSP ritorna un'istanza di HYBRID BCCSP configurata
func GetBCCSP(swBCCSP bccsp.BCCSP) bccsp.BCCSP {
	return NewHybridBCCSP(swBCCSP)
}

// Verifica che HybridBCCSP implementi l'interfaccia BCCSP
var _ bccsp.BCCSP = (*HybridBCCSP)(nil)
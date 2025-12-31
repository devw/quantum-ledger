package hybrid

import (
	"encoding/binary"
	"errors"
)

// combineSignatures creates: [4 bytes ECDSA len][ECDSA sig][PQC sig]
func combineSignatures(ecdsaSig, pqcSig []byte) []byte {
	lenBuf := make([]byte, 4)
	binary.BigEndian.PutUint32(lenBuf, uint32(len(ecdsaSig)))

	combined := make([]byte, 0, 4+len(ecdsaSig)+len(pqcSig))
	combined = append(combined, lenBuf...)
	combined = append(combined, ecdsaSig...)
	combined = append(combined, pqcSig...)

	return combined
}

// parseHybridSignature splits combined signature
func parseHybridSignature(signature []byte) (ecdsaSig, pqcSig []byte, err error) {
	if len(signature) < 4 {
		return nil, nil, errors.New("signature too short")
	}

	ecdsaLen := binary.BigEndian.Uint32(signature[:4])
	if ecdsaLen > uint32(len(signature)-4) {
		return nil, nil, errors.New("invalid signature format: ECDSA length exceeds signature size")
	}

	if len(signature) < int(4+ecdsaLen) {
		return nil, nil, errors.New("invalid signature format")
	}

	ecdsaSig = signature[4 : 4+ecdsaLen]
	pqcSig = signature[4+ecdsaLen:]

	return ecdsaSig, pqcSig, nil
}
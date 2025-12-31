#!/bin/bash

echo "======================================"
echo "VERIFICA STATO IMPLEMENTAZIONE PQC"
echo "======================================"

# ===========================
# 1. VERIFICA INFRASTRUTTURA COMPLETATA
# ===========================

echo -e "\n[1] Verifica HYBRID BCCSP Provider..."
test -f bccsp/hybrid/hybrid.go && echo "✅ hybrid.go esiste" || echo "❌ hybrid.go NON trovato"
grep -q "func (h \*HybridBCCSP) KeyGen" bccsp/hybrid/hybrid.go && echo "✅ KeyGen implementato" || echo "⚠️  KeyGen non trovato"
grep -q "func (h \*HybridBCCSP) Sign" bccsp/hybrid/hybrid.go && echo "✅ Sign implementato" || echo "⚠️  Sign non trovato"
grep -q "func (h \*HybridBCCSP) Verify" bccsp/hybrid/hybrid.go && echo "✅ Verify implementato" || echo "⚠️  Verify non trovato"

echo -e "\n[2] Verifica HYBRID Factory..."
test -f docker/compose/hybridfactory.go && echo "✅ hybridfactory.go esiste" || echo "❌ hybridfactory.go NON trovato"
grep -q "type HYBRIDFactory struct" docker/compose/hybridfactory.go && echo "✅ HYBRIDFactory definito" || echo "⚠️  HYBRIDFactory non trovato"

echo -e "\n[3] Verifica Docker Image Custom..."
docker images | grep "custom-fabric-peer" | grep "2.5" && echo "✅ Immagine Docker custom-fabric-peer:2.5 presente" || echo "⚠️  Immagine Docker non trovata"

echo -e "\n[4] Verifica Configurazione Docker Compose..."
test -f docker/compose/fabric-baseline-hybrid.yaml && echo "✅ fabric-baseline-hybrid.yaml esiste" || echo "❌ Configurazione HYBRID non trovata"
grep -q "CORE_PEER_BCCSP_DEFAULT=HYBRID" docker/compose/fabric-baseline-hybrid.yaml && echo "✅ BCCSP configurato su HYBRID" || echo "⚠️  Configurazione BCCSP non trovata"

# ===========================
# 2. VERIFICA INTEGRAZIONE PQC (TODO)
# ===========================

echo -e "\n======================================"
echo "VERIFICA INTEGRAZIONE POST-QUANTUM"
echo "======================================"

echo -e "\n[5] Verifica dipendenza liboqs-go..."
grep -q "github.com/open-quantum-safe/liboqs-go" go.mod 2>/dev/null && echo "✅ liboqs-go presente in go.mod" || echo "❌ TODO: Aggiungere liboqs-go a go.mod"

echo -e "\n[6] Verifica import liboqs in hybrid.go..."
grep -q "github.com/open-quantum-safe/liboqs-go/oqs" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ liboqs importato" || echo "❌ TODO: Importare liboqs in hybrid.go"

echo -e "\n[7] Verifica struttura HybridKey..."
grep -q "type HybridKey struct" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ HybridKey definito" || echo "❌ TODO: Definire struttura HybridKey"
grep -q "pqc.*oqs.Signature" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ Campo PQC in HybridKey" || echo "❌ TODO: Aggiungere campo PQC"

echo -e "\n[8] Verifica implementazione PQC KeyGen..."
grep -q "Dilithium3" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ Dilithium3 configurato in KeyGen" || echo "❌ TODO: Implementare generazione chiavi Dilithium"
grep -q "GenerateKeypair" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ GenerateKeypair presente" || echo "❌ TODO: Chiamare GenerateKeypair()"

echo -e "\n[9] Verifica firma ibrida..."
grep -q "CombineSignatures\|combineSignatures" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ Funzione CombineSignatures presente" || echo "❌ TODO: Implementare CombineSignatures()"

echo -e "\n[10] Verifica verifica ibrida..."
grep -q "ParseHybridSignature\|parseHybridSignature" bccsp/hybrid/hybrid.go 2>/dev/null && echo "✅ ParseHybridSignature presente" || echo "❌ TODO: Implementare ParseHybridSignature()"

# ===========================
# 3. ANALISI DETTAGLIATA CODICE
# ===========================

echo -e "\n======================================"
echo "ANALISI DETTAGLIATA CODICE"
echo "======================================"

echo -e "\n[11] Numero di metodi implementati in HybridBCCSP..."
grep -c "^func (h \*HybridBCCSP)" bccsp/hybrid/hybrid.go 2>/dev/null || echo "0"

echo -e "\n[12] Metodi che attualmente delegano a SW provider..."
grep -A 2 "^func (h \*HybridBCCSP)" bccsp/hybrid/hybrid.go 2>/dev/null | grep -c "h.sw\." || echo "Impossibile verificare"

echo -e "\n[13] Linee di codice in hybrid.go..."
wc -l bccsp/hybrid/hybrid.go 2>/dev/null || echo "File non trovato"

# ===========================
# 4. TEST E VALIDAZIONE
# ===========================

echo -e "\n======================================"
echo "TEST E VALIDAZIONE"
echo "======================================"

echo -e "\n[14] Verifica test unitari per HYBRID..."
find tests/unit -name "*hybrid*" -o -name "*pqc*" 2>/dev/null | wc -l | xargs echo "File di test trovati:"

echo -e "\n[15] Verifica configurazione pytest..."
test -f pytest.ini && echo "✅ pytest.ini presente" || echo "⚠️  pytest.ini non trovato"

echo -e "\n[16] Controlla se il peer HYBRID è in esecuzione..."
docker ps | grep "custom-fabric-peer" && echo "✅ Peer HYBRID in esecuzione" || echo "⚠️  Peer non in esecuzione"

# ===========================
# 5. CHECKLIST RIMANENTE
# ===========================

echo -e "\n======================================"
echo "CHECKLIST TASK RIMANENTI"
echo "======================================"

echo -e "\n📋 FASE 1 - Integrazione Algoritmi PQC:"
echo "  [ ] 1. Aggiungere liboqs-go a go.mod"
echo "  [ ] 2. Importare oqs in hybrid.go"
echo "  [ ] 3. Definire struct HybridKey"
echo "  [ ] 4. Implementare KeyGen con Dilithium3"
echo "  [ ] 5. Implementare Sign ibrido"
echo "  [ ] 6. Implementare Verify ibrido"
echo "  [ ] 7. Implementare CombineSignatures()"
echo "  [ ] 8. Implementare ParseHybridSignature()"
echo "  [ ] 9. Gestire serializzazione chiavi"
echo "  [ ] 10. Aggiungere gestione errori PQC"

echo -e "\n📋 FASE 2 - Test e Validazione:"
echo "  [ ] 1. Scrivere unit test per KeyGen"
echo "  [ ] 2. Scrivere unit test per Sign/Verify"
echo "  [ ] 3. Test integrazione con Fabric"
echo "  [ ] 4. Benchmark prestazioni"

echo -e "\n======================================"
echo "COMANDI RAPIDI UTILI"
echo "======================================"

cat << 'EOF'

# Aggiungere liboqs-go:
cd /path/to/project && go get github.com/open-quantum-safe/liboqs-go/oqs

# Rebuild Docker image dopo modifiche:
cd docker/compose && docker build -f Dockerfile.peer -t custom-fabric-peer:2.5 .

# Avviare rete HYBRID:
docker-compose -f docker/compose/fabric-baseline-hybrid.yaml up -d

# Vedere log del peer:
docker logs -f peer0.org1.example.com

# Verificare BCCSP attivo:
docker exec peer0.org1.example.com peer version

# Fermare rete:
docker-compose -f docker/compose/fabric-baseline-hybrid.yaml down

EOF

echo -e "\n======================================"
echo "FINE VERIFICA"
echo "======================================"
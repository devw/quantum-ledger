#!/bin/bash

set -e

COMPOSE_DIR="docker/compose"
CONFIGS_DIR="${COMPOSE_DIR}/configs"

# Pulizia
echo "Pulizia vecchi certificati..."
rm -rf ${CONFIGS_DIR}/peer0-org1/msp/{cacerts,keystore,signcerts}/*
rm -rf ${CONFIGS_DIR}/orderer/msp/{cacerts,keystore,signcerts}/*

# Crea directory se non esistono
mkdir -p ${CONFIGS_DIR}/peer0-org1/msp/{cacerts,keystore,signcerts,admincerts}
mkdir -p ${CONFIGS_DIR}/orderer/msp/{cacerts,keystore,signcerts,admincerts}

echo "=== Generazione CA Certificate (ECDSA P-256) ==="

# Genera chiave privata CA
openssl ecparam -name prime256v1 -genkey -noout -out ${CONFIGS_DIR}/ca-key.pem

# Genera certificato CA self-signed
openssl req -new -x509 -key ${CONFIGS_DIR}/ca-key.pem \
    -out ${CONFIGS_DIR}/ca-cert.pem \
    -days 365 \
    -subj "/C=US/ST=California/L=San Francisco/O=example.com/OU=COP/CN=ca.example.com"

echo "=== Generazione Peer0 Org1 Certificate ==="

# Genera chiave privata peer
openssl ecparam -name prime256v1 -genkey -noout -out ${CONFIGS_DIR}/peer0-org1/msp/keystore/priv_sk

# Genera CSR per peer con OU=peer
openssl req -new -key ${CONFIGS_DIR}/peer0-org1/msp/keystore/priv_sk \
    -out ${CONFIGS_DIR}/peer0-org1-csr.pem \
    -subj "/C=US/ST=California/L=San Francisco/O=org1.example.com/OU=peer/CN=peer0.org1.example.com"

# Crea file di configurazione per estensioni v3
cat > ${CONFIGS_DIR}/peer0-ext.cnf << 'EXTEOF'
[v3_peer]
subjectAltName=DNS:peer0.org1.example.com
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectKeyIdentifier=hash
EXTEOF

# Firma il certificato peer con la CA
openssl x509 -req -in ${CONFIGS_DIR}/peer0-org1-csr.pem \
    -CA ${CONFIGS_DIR}/ca-cert.pem \
    -CAkey ${CONFIGS_DIR}/ca-key.pem \
    -CAcreateserial \
    -out ${CONFIGS_DIR}/peer0-org1/msp/signcerts/peer0.org1.example.com-cert.pem \
    -days 365 \
    -sha256 \
    -extensions v3_peer \
    -extfile ${CONFIGS_DIR}/peer0-ext.cnf

# Copia CA cert
cp ${CONFIGS_DIR}/ca-cert.pem ${CONFIGS_DIR}/peer0-org1/msp/cacerts/

echo "=== Generazione Orderer Certificate ==="

# Genera chiave privata orderer
openssl ecparam -name prime256v1 -genkey -noout -out ${CONFIGS_DIR}/orderer/msp/keystore/priv_sk

# Genera CSR per orderer con OU=orderer
openssl req -new -key ${CONFIGS_DIR}/orderer/msp/keystore/priv_sk \
    -out ${CONFIGS_DIR}/orderer-csr.pem \
    -subj "/C=US/ST=California/L=San Francisco/O=example.com/OU=orderer/CN=orderer.example.com"

# Crea file di configurazione per estensioni v3
cat > ${CONFIGS_DIR}/orderer-ext.cnf << 'EXTEOF'
[v3_orderer]
subjectAltName=DNS:orderer.example.com
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectKeyIdentifier=hash
EXTEOF

# Firma il certificato orderer con la CA
openssl x509 -req -in ${CONFIGS_DIR}/orderer-csr.pem \
    -CA ${CONFIGS_DIR}/ca-cert.pem \
    -CAkey ${CONFIGS_DIR}/ca-key.pem \
    -CAcreateserial \
    -out ${CONFIGS_DIR}/orderer/msp/signcerts/orderer.example.com-cert.pem \
    -days 365 \
    -sha256 \
    -extensions v3_orderer \
    -extfile ${CONFIGS_DIR}/orderer-ext.cnf

# Copia CA cert
cp ${CONFIGS_DIR}/ca-cert.pem ${CONFIGS_DIR}/orderer/msp/cacerts/

echo "=== Rinomina chiavi con SKI ==="

# Calcola SKI per peer e rinomina
SKI_PEER=$(openssl x509 -in ${CONFIGS_DIR}/peer0-org1/msp/signcerts/peer0.org1.example.com-cert.pem -noout -text | grep -A1 "Subject Key Identifier" | tail -1 | tr -d ' :' | tr '[:upper:]' '[:lower:]')
if [ ! -z "$SKI_PEER" ]; then
    cp ${CONFIGS_DIR}/peer0-org1/msp/keystore/priv_sk ${CONFIGS_DIR}/peer0-org1/msp/keystore/${SKI_PEER}_sk
    echo "Peer SKI: ${SKI_PEER}"
fi

# Calcola SKI per orderer e rinomina
SKI_ORDERER=$(openssl x509 -in ${CONFIGS_DIR}/orderer/msp/signcerts/orderer.example.com-cert.pem -noout -text | grep -A1 "Subject Key Identifier" | tail -1 | tr -d ' :' | tr '[:upper:]' '[:lower:]')
if [ ! -z "$SKI_ORDERER" ]; then
    cp ${CONFIGS_DIR}/orderer/msp/keystore/priv_sk ${CONFIGS_DIR}/orderer/msp/keystore/${SKI_ORDERER}_sk
    echo "Orderer SKI: ${SKI_ORDERER}"
fi

echo "=== Verifica certificati ECDSA con OUs ==="
echo "Peer cert:"
openssl x509 -in ${CONFIGS_DIR}/peer0-org1/msp/signcerts/peer0.org1.example.com-cert.pem -text -noout | grep -E "(Subject:|Public Key Algorithm:)" -A3

echo ""
echo "Orderer cert:"
openssl x509 -in ${CONFIGS_DIR}/orderer/msp/signcerts/orderer.example.com-cert.pem -text -noout | grep -E "(Subject:|Public Key Algorithm:)" -A3

# Pulizia file temporanei
rm -f ${CONFIGS_DIR}/*.pem ${CONFIGS_DIR}/*.srl ${CONFIGS_DIR}/*.cnf

echo ""
echo "✅ Certificati ECDSA con OUs generati con successo!"
echo "✅ Struttura MSP pronta per Hyperledger Fabric"

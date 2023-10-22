#!/bin/bash
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}/config

. ./utils.sh
printSeparator "Generate crypto-material for Org1"
cryptogen generate --config=./cryptogen-input/crypto-config-org1.yaml --output="crypto-material"
printSeparator "Generate crypto-material for Org2"
cryptogen generate --config=./cryptogen-input/crypto-config-org2.yaml --output="crypto-material"
printSeparator "Generate crypto-material for Org3"
cryptogen generate --config=./cryptogen-input/crypto-config-org3.yaml --output="crypto-material"
printSeparator "Generate crypto-material for Orderer"
cryptogen generate --config=./cryptogen-input/crypto-config-orderer.yaml --output="crypto-material"
printSeparator "Create Genesis-Block"
configtxgen -profile modbus2chainNetworkProfile -configPath ${PWD}/config -channelID system-channel -outputBlock ./system-genesis-block/genesis.block
printSeparator "Start modbus2chainNetworkProfile within Docker Containers"
docker-compose -f ./docker/docker-compose-orderer.yaml -f ./docker/docker-compose-org1.yaml -f ./docker/docker-compose-org2.yaml -f ./docker/docker-compose-org3.yaml -f ./docker/docker-compose-ca-org1.yaml up -d
printSeparator "Create Channel Transaction"
configtxgen -profile modbus2chainChannelProfile -configPath ${PWD}/config -outputCreateChannelTx ./channel-artifacts/modbus2chainchannel.tx -channelID modbus2chainchannel && sleep 3
printSeparator "Create Anchor Peers Update for Org 1"
configtxgen -profile modbus2chainChannelProfile -configPath ${PWD}/config -outputAnchorPeersUpdate ./channel-artifacts/ORG1MSPanchors.tx -channelID modbus2chainchannel -asOrg Org1
printSeparator "Create Anchor Peers Update for Org 2"
configtxgen -profile modbus2chainChannelProfile -configPath ${PWD}/config -outputAnchorPeersUpdate ./channel-artifacts/ORG2MSPanchors.tx -channelID modbus2chainchannel -asOrg Org2
printSeparator "Create Anchor Peers Update for Org 3"
configtxgen -profile modbus2chainChannelProfile -configPath ${PWD}/config -outputAnchorPeersUpdate ./channel-artifacts/ORG3MSPanchors.tx -channelID modbus2chainchannel -asOrg Org3
printSeparator "Wait 3 seconds for network to come up" && sleep 3
printSeparator "Set Identity to Org1"
switchIdentity "Org1" 7051 && echoCurrentFabricEnvironment
printSeparator "Create channel"
peer channel create -o localhost:7050 -c modbus2chainchannel --ordererTLSHostnameOverride orderer0.modbus2chain.com -f ./channel-artifacts/modbus2chainchannel.tx --outputBlock ./channel-artifacts/modbus2chainchannel.block --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA
printSeparator "Join Org1 to channel"
peer channel join -b ./channel-artifacts/modbus2chainchannel.block && sleep 1
printSeparator "Update Anchor Peers as Org1"
peer channel update -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com -c modbus2chainchannel -f ./channel-artifacts/ORG1MSPanchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA

# Pacchetta il chaincode
printSeparator "Package Chaincode"

peer lifecycle chaincode package cciotdata.tar.gz --path ./atcc/ --lang node --label cciotdata 

# Installa il chaincode e ottieni il package-id
printSeparator "Install Chaincode for Org1"
peer lifecycle chaincode install cciotdata.tar.gz  --tlsRootCertFiles ./crypto-material/peerOrganizations/org1.modbus2chain.com/tlsca/tlsca.org1.modbus2chain.com-cert.pem

# Ottieni l'elenco dei package installati
INSTALLED_PACKAGES=$(peer lifecycle chaincode queryinstalled)
echo "INSTALLED_PACKAGES ID: $INSTALLED_PACKAGES"
# Estrai il package-id dal risultato
PACKAGE_ID=$(echo "$INSTALLED_PACKAGES" | awk '/Package ID:/{print $3}')

# Stampa il risultato dell'installazione
echo "Package ID: $PACKAGE_ID"

echo "ORDERE CA ID: $ORDERER_CA"

# Approva il chaincode per l'organizzazione 1
printSeparator "Approve Chaincode for Org1"
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com --channelID modbus2chainchannel --name cciotdata --version 1.1 --init-required --sequence 1 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA --package-id $PACKAGE_ID localhost:7051 --waitForEvent --signature-policy "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

printSeparator "Set Identity to Org2"
switchIdentity "Org2" 8051 && echoCurrentFabricEnvironment && sleep 1
printSeparator "Join Org2 to channel"
peer channel join -b ./channel-artifacts/modbus2chainchannel.block  && sleep 1
printSeparator "Update Anchor Peers as Org2"
peer channel update -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com -c modbus2chainchannel -f ./channel-artifacts/ORG2MSPanchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA

peer lifecycle chaincode package cciotdata.tar.gz --path ./atcc/ --lang node --label cciotdata 

# Installa il chaincode e ottieni il package-id
printSeparator "Install Chaincode for Org2"
peer lifecycle chaincode install cciotdata.tar.gz --tlsRootCertFiles /usr/local/go/src/Modbus2Chain/crypto-material/peerOrganizations/org2.modbus2chain.com/peers/peer0.org2.modbus2chain.com/tls/ca.crt

# Ottieni l'elenco dei package installati
INSTALLED_PACKAGES=$(peer lifecycle chaincode queryinstalled)
echo "INSTALLED_PACKAGES ID: $INSTALLED_PACKAGES"
# Estrai il package-id dal risultato
PACKAGE_ID=$(echo "$INSTALLED_PACKAGES" | awk '/Package ID:/{print $3}')

# Stampa il risultato dell'installazione
echo "Package ID: $PACKAGE_ID"

echo "ORDERE CA ID: $ORDERER_CA"
# Approva il chaincode per l'organizzazione 2 
printSeparator "Approve Chaincode for Org2"
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com --channelID modbus2chainchannel --name cciotdata --version 1.1 --init-required --sequence 1 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA --package-id $PACKAGE_ID --waitForEvent --signature-policy "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

# Verifica la disponibilità del commit
printSeparator "Check Commit Readiness"
peer lifecycle chaincode checkcommitreadiness --channelID modbus2chainchannel --name cciotdata --version 1.1 --sequence 1 --init-required --tls $CORE_PEER_TLS_ENABLED --signature-policy "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

# Esegui il commit del chaincode
printSeparator "Commit Chaincode"
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com --channelID modbus2chainchannel --name cciotdata --version 1.1 --sequence 1 --init-required --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA --peerAddresses localhost:7051 --peerAddresses localhost:8051 --tlsRootCertFiles /usr/local/go/src/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/peers/peer0.org1.modbus2chain.com/tls/ca.crt --tlsRootCertFiles /usr/local/go/src/Modbus2Chain/crypto-material/peerOrganizations/org2.modbus2chain.com/peers/peer0.org2.modbus2chain.com/tls/ca.crt --signature-policy "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

# Inizializza il chaincode
printSeparator "Initialize Chaincode"
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA --channelID modbus2chainchannel -n cciotdata --isInit -c '{"Args":["initLedger"]}'


printSeparator "VERIFY THE CHANNEL CREATION"
peer channel getinfo -c modbus2chainchannel
printSeparator "LOGS"
printSeparator "LOGS"
printSeparator "LOGS"
peer lifecycle chaincode queryinstalled --peerAddresses localhost:7051 --tlsRootCertFiles /usr/local/go/src/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/peers/peer0.org1.modbus2chain.com/tls/ca.crt --output json 
peer lifecycle chaincode querycommitted --channelID modbus2chainchannel --name cciotdata


printSeparator "Set Identity to Org3"
switchIdentity "Org3" 8052 && echoCurrentFabricEnvironment && sleep 1
printSeparator "Join Org3 to channel"
peer channel join -b ./channel-artifacts/modbus2chainchannel.block  && sleep 1
printSeparator "Update Anchor Peers as Org3"
peer channel update -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com -c modbus2chainchannel -f ./channel-artifacts/ORG3MSPanchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA

# Approva il chaincode per l'organizzazione 3
printSeparator "Approve Chaincode for Org3"
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com --channelID modbus2chainchannel --name cciotdata --version 1.1 --init-required --sequence 1 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA --package-id $PACKAGE_ID --waitForEvent --signature-policy "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer')"

printSeparator "Done!"

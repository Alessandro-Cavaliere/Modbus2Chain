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
docker-compose -f ./docker/docker-compose-orderer.yaml -f ./docker/docker-compose-org1.yaml -f ./docker/docker-compose-org2.yaml -f ./docker/docker-compose-org3.yaml up -d
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
printSeparator "Set Identity to Org2"
switchIdentity "Org2" 8051 && echoCurrentFabricEnvironment && sleep 1
printSeparator "Join Org2 to channel"
peer channel join -b ./channel-artifacts/modbus2chainchannel.block  && sleep 1
printSeparator "Update Anchor Peers as Org2"
peer channel update -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com -c modbus2chainchannel -f ./channel-artifacts/ORG2MSPanchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA
printSeparator "Set Identity to Org3"
switchIdentity "Org3" 8052 && echoCurrentFabricEnvironment && sleep 1
printSeparator "Join Org3 to channel"
peer channel join -b ./channel-artifacts/modbus2chainchannel.block
printSeparator "Update Anchor Peers as Org3"
peer channel update -o localhost:7050 --ordererTLSHostnameOverride orderer0.modbus2chain.com -c modbus2chainchannel -f ./channel-artifacts/ORG3MSPanchors.tx --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA
printSeparator "Done!"
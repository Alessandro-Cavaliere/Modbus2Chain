package main

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

// Asset provides functions for managing an asset
type Asset struct {
	ID    string `json:"ID"`
	Value int    `json:"value"`
	Owner string `json:"owner"`
}

// Verifica l'accesso in base all'MSP ID
func checkOrgAccess(ctx contractapi.TransactionContextInterface, allowedMspID string) error {
	client := ctx.GetClientIdentity()
	if client == nil {
		return fmt.Errorf("Errore nel recupero dell'identità del client: client non trovato")
	}
	mspID, err := client.GetMSPID()
	if err != nil {
		return fmt.Errorf("Errore nel recupero del MSP ID: %v", err)
	}

	if mspID != allowedMspID {
		return fmt.Errorf("Accesso negato. Questa funzione può essere eseguita solo da utenti registrati presso %s", allowedMspID)
	}

	return nil
}

func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1.modbus2chain.com"); err != nil {
		return err
	}

	assets := []Asset{
		{ID: "temperature", Value: 0, Owner: "Tomoko"},
		{ID: "umidity", Value: 0, Owner: "Brad"},
		{ID: "movement", Value: 0, Owner: "Jin Soo"},
	}

	for _, asset := range assets {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.ID, assetJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state: %v", err)
		}
	}

	return nil
}

func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, value int, owner string) error {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1,modbus2chain.com"); err != nil {
		return err
	}

	asset := Asset{
		ID:    id,
		Value: value,
		Owner: owner,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1,modbus2chain.com"); err != nil {
		return nil, err
	}

	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, id string, value int, owner string) error {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1.modbus2chain.com"); err != nil {
		return err
	}

	// Overwriting original asset with new asset
	asset := Asset{
		ID:    id,
		Value: value,
		Owner: owner,
	}

	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

func (s *SmartContract) TransferAsset(ctx contractapi.TransactionContextInterface, id string, newOwner string) error {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1.modbus2chain.com"); err != nil {
		return err
	}

	asset, err := s.ReadAsset(ctx, id)
	if err != nil {
		return err
	}

	asset.Owner = newOwner
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// Controllo accesso
	if err := checkOrgAccess(ctx, "ca-org1.modbus2chain.com"); err != nil {
		return nil, err
	}

	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}

// Main function starts up the chaincode in the container during instantiate
func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Errore nella creazione del chaincode: %s", err)
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Errore nell'avvio del chaincode: %s", err)
	}
}

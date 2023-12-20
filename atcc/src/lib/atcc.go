package main

import (
	"encoding/json"
	"fmt"
)

// Asset rappresenta un asset nella blockchain
type Asset struct {
	ID    string `json:"ID"`
	Value int    `json:"value"`
	Owner string `json:"owner"`
}

// SimpleChaincode esempio di chaincode semplice
type SimpleChaincode struct {
}

// Init inizializza il chaincode
func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	// Qui puoi inserire la logica per inizializzare il tuo ledger
	return shim.Success(nil)
}

// Invoke - La nostra entry point per le invocazioni
func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	function, args := stub.GetFunctionAndParameters()

	if function == "createAsset" {
		return t.createAsset(stub, args)
	} else if function == "readAsset" {
		return t.readAsset(stub, args)
	}

	return shim.Error("Funzione non riconosciuta")
}

func (t *SimpleChaincode) createAsset(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 3 {
		return shim.Error("Numero di argomenti non corretto. Richiesti 3")
	}

	var asset = Asset{ID: args[0], Value: args[1], Owner: args[2]}
	assetAsBytes, _ := json.Marshal(asset)
	stub.PutState(args[0], assetAsBytes)

	return shim.Success(nil)
}

func (t *SimpleChaincode) readAsset(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 1 {
		return shim.Error("Numero di argomenti non corretto. Richiesto 1")
	}

	assetAsBytes, _ := stub.GetState(args[0])
	return shim.Success(assetAsBytes)
}

func main() {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Errore durante l'avvio del chaincode: %s", err)
	}
}

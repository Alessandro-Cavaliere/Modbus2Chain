const { Contract } = require('fabric-contract-api');

class Asset {
    constructor(id, value, owner) {
        this.ID = id;
        this.Value = value;
        this.Owner = owner;
    }
}

class SimpleChaincode extends Contract {
    async Init(stub) {
        // Qui puoi inserire la logica per inizializzare il tuo ledger
        return stub.getResponse();
    }
    async Hello() {
        return "ciaooo"
    }

    async Invoke(stub) {
        const { fcn, params } = stub.getFunctionAndParameters();

        if (fcn === 'createAsset') {
            return this.createAsset(stub, params);
        } else if (fcn === 'readAsset') {
            return this.readAsset(stub, params);
        }

        return stub.newError('Funzione non riconosciuta');
    }

    async createAsset(stub, args) {
        if (args.length !== 3) {
            return stub.newError('Numero di argomenti non corretto. Richiesti 3');
        }

        const asset = new Asset(args[0], parseInt(args[1]), args[2]);
        await stub.putState(args[0], Buffer.from(JSON.stringify(asset)));

        return stub.getResponse();
    }

    async readAsset(stub, args) {
        if (args.length !== 1) {
            return stub.newError('Numero di argomenti non corretto. Richiesto 1');
        }

        const assetAsBytes = await stub.getState(args[0]);
        if (!assetAsBytes || assetAsBytes.length === 0) {
            return stub.newError(`Asset con ID ${args[0]} non trovato`);
        }

        return assetAsBytes;
    }
}

module.exports = SimpleChaincode;

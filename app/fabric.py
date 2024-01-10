import os
import hfc
import asyncio
from hfc.fabric import Client
from hfc.fabric_ca import CAClient
from hfc.util.crypto.crypto import ecies
from hfc.fabric_network.wallet import FileSystenWallet
from hfc.fabric_ca.caservice import ca_service
from hfc.fabric.user import create_user
from hfc.fabric_ca.caservice import ca_service
from hfc.fabric_network import wallet


loop = asyncio.get_event_loop()

ca_certs_path="/home/alexcav/go/src/GitHub/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/ca/ca-cert.pem"

cli = Client(net_profile="network.json")
cli.new_channel('modbus2chainchannel')

org1_admin = cli.get_user(org_name='org1.modbus2chain.com', name='Admin')


policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
        {'role': {'name': 'member', 'mspId': 'Org2MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0},
            {'signed-by': 1},
        ]
    }
}

responses = loop.run_until_complete(cli.chaincode_instantiate(
                requestor=org1_admin,
                channel_name='modbus2chainchannel',
                peers=['peer0.org1.modbus2chain.com'],
                args=["Init"],
                cc_name="cc-iotdata",
                cc_version='v1.1',
                cc_endorsement_policy=policy, 
               ))

print("\n\n\n")
print("INVOKE CC ..")

args=["temperature"]
response = loop.run_until_complete(cli.chaincode_invoke(
    requestor=org1_admin,
    channel_name='modbus2chainchannel',
    peers=['peer0.org1.modbus2chain.com'],
    args=args,
    cc_name="atcc",
    fcn="ReadAsset",
    wait_for_event=True,  # Aspetta che l'evento sia processato
))

print(response)
print("\n\n\n")
print("RESPONSE SOORA")
print(cli._channels)
ca_certs_path="/home/alexcav/go/src/GitHub/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/ca/ca-cert.pem"

print("CASVC LOADING...")
casvc = ca_service(target="https://0.0.0.0:7054",ca_certs_path=ca_certs_path,ca_name="ca-org1.modbus2chain.com")
print(dir(ca_service))
identityService = casvc.newIdentityService()
adminEnrollment = casvc.enroll("admin", "adminpw")
secret = adminEnrollment.register("user2")
user2Enrollment = casvc.enroll("user2", secret) 

ca_url = cli.CAs.get('ca-org1.modbus2chain.com')._url
ca_certs_path="/home/alexcav/go/src/GitHub/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/ca/ca-cert.pem"

    
 #Istanzia l'ogetto ca_client per gli utenti registrati all'organizzazione. In questo caso è l'admin
ca_admin_org1 = cli.get_user(org_name='org1.modbus2chain.com',name="Admin")   
ca_admin_org2 = cli.get_user(org_name='org2.modbus2chain.com',name="Admin")   
ca_admin_org3 = cli.get_user(org_name='org3.modbus2chain.com',name="Admin") 

new_wallet = wallet.FileSystenWallet() # Creates default wallet at ./tmp/hfc-kvs
user_identity = wallet.Identity("user2", user2Enrollment) # Creates a new Identity of the enrolled user
user_identity.CreateIdentity(new_wallet) # Stores this identity in the FileSystemWallet


"""

# Creare un'istanza del wallet
wallet_path = "hfc_wallets"
# Crea o recupera il wallet
wallet = FileSystenWallet(wallet_path)

# ID di iscrizione dell'utente
enrollment_id = "Admin"

user_folder = "/home/alexcav/go/src/GitHub/Modbus2Chain/crypto-material/peerOrganizations/org1.modbus2chain.com/users/Admin@org1.modbus2chain.com/msp"

# Leggi il certificato di iscrizione
with open(os.path.join(user_folder, "signcerts", "Admin@org1.modbus2chain.com-cert.pem"), "rb") as f:
    enrollment_cert = f.read()

# Leggi la chiave privata
with open(os.path.join(user_folder, "keystore", "priv_sk"), "rb") as f:
    private_key = f.read()

print(enrollment_cert)
print(private_key)

admin = wallet.get('Admin')

print("----")
print(admin)
"""
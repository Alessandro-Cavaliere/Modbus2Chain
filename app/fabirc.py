from hfc.fabric import Client
cli = Client(net_profile="network.json")

print(cli.organizations)  # orgs in the network
print(cli.peers)  # peers in the network
print(cli.orderers)  # orderers in the network
print(cli.CAs)  # ca nodes in the network

# Verifica la configurazione del client
if cli.organizations.get('org1.modbus2chain.com') is None:
    print("Organizzazione 'Org1' non trovata nel profilo di rete.")
else:
    print("Organizzazione 'Org1' trovata.")

# Verifica la configurazione della CA
if cli.CAs.get('ca-org1') is None:
    print("CA 'ca-org1' non trovata nel profilo di rete.")
else:
    print("CA 'ca-org1' trovata.")

print(cli)
 #Istanzia l'ogetto ca_client per gli utenti registrati all'organizzazione. In questo caso è l'admin
ca_admin_org1 = cli.get_user(org_name='org1.modbus2chain.com',name="Admin")   

ca_admin_org1
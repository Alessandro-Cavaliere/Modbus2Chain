import socket

beaglebone_ip = "192.168.7.2" # Indirizzo IP del nostro BeagleBone Black
beaglebone_port = 22 # Porta SSH del nostro BeagleBone Black

# creazione socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connettiti al BeagleBone
    s.connect((beaglebone_ip, beaglebone_port))
    print("Connessione riuscita!!!!")
    # chiudi la connessione
    s.close()
except socket.error as e:
    # gestisci il caso in cui la connessione fallisce
    print("Connessione fallita: {e}")
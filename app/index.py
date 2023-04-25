import socket

from pymodbus.client import ModbusSerialClient as ModbusClient
beaglebone_ip = "192.168.7.2" # Indirizzo IP del nostro BeagleBone Black
beaglebone_port = 22 # Porta SSH del nostro BeagleBone Black

# creazione socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Configura il client Modbus RTU
client = ModbusClient(method='rtu', port='/dev/ttyS1', baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Connetti al bus Modbus
connected = client.connect()

try:
    # connettiti al BeagleBone
    s.connect((beaglebone_ip, beaglebone_port))
    print("Connessione riuscita!!!!")
    # chiudi la connessione

    if connected:
    # Leggi i registri dall'unità slave (ad es. Arduino)
    # Supponendo che l'Arduino memorizzi la temperatura nel registro 0 e l'umidità nel registro 1
        response = client.read_input_registers(address=0, count=2, unit=1)
    
    if response.isError():
        print("Errore nella lettura dei registri")
    else:
            # Estrai la temperatura e l'umidità dai registri
            temperature = response.registers[0] / 10
            humidity = response.registers[1] / 10
            print(f"Temperatura: {temperature} °C")
            print(f"Umidità: {humidity} %")
        
            # Chiudi la connessione
            client.close()
            

    s.close()
except socket.error as e:
    # gestisci il caso in cui la connessione fallisce
    print("Connessione fallita: {e}")
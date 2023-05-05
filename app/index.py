import time
import os
from dotenv import load_dotenv, find_dotenv
import paramiko
import board
import adafruit_dht
from pymodbus.client import ModbusSerialClient as ModbusSerialClient

load_dotenv(find_dotenv())

# Imposta i parametri per la connessione SSH - bbb = BeagleBone Black
bbb_ip = os.getenv('BBB_IP')
bbb_username = os.getenv('BBB_SSH_USERNAME')
bbb_password = os.getenv('BBB_SSH_PASSWORD')

# Configura il client Modbus RTU 
client = ModbusClient(method='rtu', port='/dev/ttyS1', baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')


try:
    # Crea una connessione SSH
    bbb = paramiko.SSHClient()
    bbb.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bbb.connect(beaglebone_ip, username=bbb_username, password=bbb_password)

    # Esegui il comando per impostare la direzione della porta GPIO 45 come output
    stdin, stdout, stderr = bbb.exec_command('echo out > /sys/class/gpio/gpio45/direction')
    print("Connessione riuscita!!!!")
    # Sensor should be set to Adafruit_DHT.DHT11,
    # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
    dht_device = adafruit_dht.DHT11(board.D18)

    temperature = dht_device.temperature
    humidity = dht_device.humidity
    print(
    "Temp: {:.1f} , C Humidity: {}% ".format(
    temperature, humidity
    )
    )
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
    # Fai suonare il buzzer per 10 secondi
    for i in range(30):
        bbb.exec_command(b"echo 1 > /sys/class/gpio/gpio45/value\n")
        time.sleep(0.1)
        bbb.exec_command(b"echo 0 > /sys/class/gpio/gpio45/value\n")
        time.sleep(0.1)
        print("SONO QUI")

    # Chiudi la connessione
    bbb.close()
except Exception as e:
    print(f"Errore: {e}")
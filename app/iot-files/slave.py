#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Main script of the Slave. 

This file is similar to the loop() function on Arduino

Create a Modbus TCP client (slave) which can be requested for data or set with
specific values by a host device (master).

In our case , the Slave device is a Raspberry Pi Pico W
"""

# system packages
import time
import urequests

# import modbus client classes
from package.umodbus import tcp

IS_DOCKER_MICROPYTHON = False
try:
    import network
except ImportError:
    IS_DOCKER_MICROPYTHON = True
    import json


# ===============================================
if IS_DOCKER_MICROPYTHON is False:
    # connect to a network
    station = network.WLAN(network.STA_IF)
    if station.active() and station.isconnected():
        station.disconnect()
        time.sleep(1)
    station.active(False)
    time.sleep(1)
    station.active(True)

    # station.connect('SSID', 'PASSWORD')
    station.connect('POCO X3 NFC', 'miciona97')
    time.sleep(1)

    while True:
        print('Waiting for WiFi connection...')
        if station.isconnected():
            print('Connected to WiFi.')
            print(station.ifconfig())
            break
        time.sleep(2)

# ===============================================
# TCP Slave setup
tcp_port = 502              # port to listen to

if IS_DOCKER_MICROPYTHON:
    local_ip = '172.24.0.2'     # static Docker IP address
else:
    # set IP address of the MicroPython device explicitly
    # local_ip = '192.168.4.1'    # IP address
    # or get it from the system after a connection to the network has been made
    local_ip = station.ifconfig()[0]

# ModbusTCP can get TCP requests from a host device to provide/set data
client = tcp.ModbusTCP()
is_bound = False

# check whether client has been bound to an IP and port
is_bound = client.get_bound_status()

if not is_bound:
    client.bind(local_ip=local_ip, local_port=tcp_port)


def my_coil_set_cb(reg_type, address, val):
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val))
    if val:
        print("dati prelevati : TEMP :10, UMID:20")  #lacio della funzione di prelevamento dati
        client.set_hreg(address= 93,value= 12)
        client.set_hreg(address= 94,value= 562)
        print('TEMP HREG {} SETTATO: {}'.format(93, "perfetto"))
        url = "http://192.168.10.174:8000/" #ip del mio pc

        #qui si lancerà l'API di prelevamento dati oppure le funzioni da dentro qui.
        try:
            print("ecco")
            # Effettua una richiesta GET all'URL
            response = urequests.get(url)
            print("risp")
            # Verifica se la richiesta ha avuto successo (codice di stato 200)
            if response.status_code == 200:
                print("Richiesta API riuscita.")
                print("Risposta:")
                print(response.text)
            else:
                print("La richiesta API ha restituito un codice di stato:", response.status_code)

        except Exception as e:
            print("Si è verificato un errore durante la richiesta API:", e)
            print(e)


def my_coil_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


def my_holding_register_set_cb(reg_type, address, val):
    print('Custom callback, called on setting {} at {} to: {}'.
          format(reg_type, address, val))


def my_holding_register_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


def my_discrete_inputs_register_get_cb(reg_type, address, val):
    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))


def my_inputs_register_get_cb(reg_type, address, val):
    # usage of global isn't great, but okay for an example
    global client

    print('Custom callback, called on getting {} at {}, currently: {}'.
          format(reg_type, address, val))

    # any operation should be as short as possible to avoid response timeouts
    new_val = val[0] + 1

    # It would be also possible to read the latest ADC value at this time
    # adc = machine.ADC(12)     # check MicroPython port specific syntax
    # new_val = adc.read()

    client.set_ireg(address=address, value=new_val)
    print('Incremented current value by +1 before sending response')


def reset_data_registers_cb(reg_type, address, val):
    # usage of global isn't great, but okay for an example
    global client
    global register_definitions

    print('Resetting register data to default values ...')
    client.setup_registers(registers=register_definitions)
    print('Default values restored')


# commond slave register setup, to be used with the Master example above
register_definitions = {
    "COILS": {
        "MOVEMENT_HANDLE": {
            "register": 42,
            "len": 1,
            "val": 0
        },
        "RESPONSE_TEST": {
            "register": 123,
            "len": 1,
            "val": 1
        }
    },
    "HREGS": {
        "TEXT_REGISTER_HREG": {
            "register": 100,
            "len": 3,
            "val": 11  # Valore iniziale della stringa
        },
        "TEMPERATURE_HREG": {
            "register": 93,
            "len": 3,
            "val": 1
        },
        "HUMIDITY_HREG": {
            "register": 94,
            "len": 1,
            "val": 0  # Valore iniziale dell'umidità
        },
        "PRESSURE_HREG": {
            "register": 95,
            "len": 1,
            "val": 0  # Valore iniziale della pressione
        }
    },
    "IREGS": {
        "DATE_CREATION_OF_THE_PROJECT_IREG": {
            "register": 10,
            "len": 1,
            "val": 1679804937 # timestamp corrente in formato int (da convertire in interfaccia)
        }
    }
}

# add callbacks for different Modbus functions
# each register can have a different callback
# coils and holding register support callbacks for set and get
register_definitions['COILS']['MOVEMENT_HANDLE']['on_set_cb'] = my_coil_set_cb
register_definitions['COILS']['MOVEMENT_HANDLE']['on_get_cb'] = my_coil_get_cb

print('Setting up registers ...')
# use the defined values of each register type provided by register_definitions
client.setup_registers(registers=register_definitions)
# alternatively use dummy default values (True for bool regs, 999 otherwise)
# client.setup_registers(registers=register_definitions, use_default_vals=True)
print('Register setup done')

print('Serving as TCP client on {}:{}'.format(local_ip, tcp_port))

while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))

print("Finished providing/accepting data as client")

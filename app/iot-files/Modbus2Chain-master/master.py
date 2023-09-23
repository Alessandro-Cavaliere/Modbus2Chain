#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Main script of the Master. 

This file is similar to the loop() function on Arduino

Create a Modbus TCP host (master) which requests or sets data on a client
device.

In our case , the Master device is a BeagleBone Black
"""

# system packages
import time

# import modbus host classes
from package.umodbus import tcp

IS_DOCKER_MICROPYTHON = False
try:
    import network
except ImportError:
    IS_DOCKER_MICROPYTHON = True
    import sys


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
slave_tcp_port = 502            # port to listen to
slave_addr = 10                 # bus address of client

# set IP address of the MicroPython device acting as client (slave)
if IS_DOCKER_MICROPYTHON:
    slave_ip = '192.168.10.119'     # static Docker IP address
else:
    slave_ip = '192.168.10.119'     # IP address

# TCP Master setup
# act as host, get Modbus data via TCP from a client device
# ModbusTCPMaster can make TCP requests to a client device to get/set data
# host = ModbusTCP(
host = tcp.TCP(
    slave_ip=slave_ip,
    slave_port=slave_tcp_port,
    timeout=5)              # optional, default 5

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

print('Requesting and updating data on TCP client at {}:{}'.
      format(slave_ip, slave_tcp_port))
print()

# READ COILS
coil_address = register_definitions['COILS']['MOVEMENT_HANDLE']['register']
coil_qty = register_definitions['COILS']['MOVEMENT_HANDLE']['len']
coil_status = host.read_coils(
    slave_addr=slave_addr,
    starting_addr=coil_address,
    coil_qty=coil_qty)
print('Status of COIL {}: {}'.format(coil_address, coil_status))
time.sleep(1)

# WRITE COILS
new_coil_val = 1
operation_status = host.write_single_coil(
    slave_addr=slave_addr,
    output_address=coil_address,
    output_value=new_coil_val)
print('Result of setting COIL {}: {}'.format(coil_address, operation_status))
time.sleep(1)

# READ COILS again
coil_status = host.read_coils(
    slave_addr=slave_addr,
    starting_addr=coil_address,
    coil_qty=coil_qty)
print('Status of COIL {}: {}'.format(coil_address, coil_status))
time.sleep(1)

print()

# READ HREGS
hreg_address = register_definitions['HREGS']['TEMPERATURE_HREG']['register']
register_qty = register_definitions['HREGS']['TEMPERATURE_HREG']['len']
register_value = host.read_holding_registers(
    slave_addr=slave_addr,
    starting_addr=hreg_address,
    register_qty=register_qty,
    signed=False)

print('Status of HREG {}: {}'.format(hreg_address, register_value))
time.sleep(1)


# READ HREGS
hreg_address1 = register_definitions['HREGS']['HUMIDITY_HREG']['register']
register_qty1 = register_definitions['HREGS']['HUMIDITY_HREG']['len']
register_value1 = host.read_holding_registers(
    slave_addr=slave_addr,
    starting_addr=hreg_address1,
    register_qty=register_qty1,
    signed=False)

print('Status of HREG {}: {}'.format(hreg_address1, register_value1))
time.sleep(1)

"""
# WRITE HREGS 
new_hreg_val = 44
operation_status = host.write_single_register(
    slave_addr=slave_addr,
    register_address=hreg_address,
    register_value=new_hreg_val,
    signed=False)
print('Result of setting HREG {}: {}'.format(hreg_address, operation_status))
time.sleep(1)


# READ HREGS again
register_value = host.read_holding_registers(
    slave_addr=slave_addr,
    starting_addr=hreg_address,
    register_qty=register_qty,
    signed=False)
print('Status of HREG {}: {}'.format(hreg_address, register_value))
time.sleep(1)
"""
print()

# READ IREGS
ireg_address = register_definitions['IREGS']['DATE_CREATION_OF_THE_PROJECT_IREG']['register']
register_qty = register_definitions['IREGS']['DATE_CREATION_OF_THE_PROJECT_IREG']['len']
register_value = host.read_input_registers(
    slave_addr=slave_addr,
    starting_addr=ireg_address,
    register_qty=register_qty,
    signed=False)
print('Status of IREG {}: {}'.format(ireg_address, register_value))
time.sleep(1)

print()

# reset all registers back to their default values on the client
# WRITE COILS
print('Resetting register data to default values...')
coil_address = \
    register_definitions['COILS']['RESPONSE_TEST']['register']
new_coil_val = True
operation_status = host.write_single_coil(
    slave_addr=slave_addr,
    output_address=coil_address,
    output_value=new_coil_val)
print('Result of setting COIL {}: {}'.format(coil_address, operation_status))
time.sleep(1)

print()

print("Finished requesting/setting data on client")

if IS_DOCKER_MICROPYTHON:
    sys.exit(0)
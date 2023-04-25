from flask import Flask, request
from hfc.fabric import Client
app = Flask("Modbus2Chain")

try:
    cli = Client(net_profile="./network.json")
    print("Client object created successfully!")
    print ( cli.organizations )
except FileNotFoundError:
    print("Error: could not find the network profile file.")
except Exception as e:
    print(f"Error: {e}")

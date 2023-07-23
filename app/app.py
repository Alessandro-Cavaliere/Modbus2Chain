from flask import Flask, request, jsonify
import sys
sys.path.insert(0, 'app\routes\auth.py')
import auth
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
app = Flask("Modbus2Chain")


connection = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE'),
    connect_timeout=60
)

@app.route('/')
def home():
    return "Welcome to Modbus2Chain Server"

@app.route('/login', methods=['POST'])
def login():
    # Esempio di autenticazione con username e password
    data = request.form
    print(data)
    username = data.get('username')
    print(username)
    password = data.get('password')

    # Esempio di verifica delle credenziali
    if username == "utente" and password == "password":
        token = auth.generate_token(username)
        return jsonify({"token": token}), 200

    return jsonify({"message": "Credenziali non valide"}), 401

@app.route('/protected', methods=['GET'])
def protected_route():
    if not auth.authenticate_token():
        return jsonify({"message": "Token non valido"}), 401

    return jsonify({"message": "Questa è una rotta protetta"}), 200

app.run(port=8000)

from flask import Flask, request, jsonify
import sys
import subprocess
import paramiko
sys.path.insert(0, 'app\routes\auth.py')
import auth
import os
import datetime
import mysql.connector
from dotenv import load_dotenv
import jwt

load_dotenv()
app = Flask("Modbus2Chain")


connection = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE'),
    connect_timeout=60
)

# Chiave segreta per la firma del token JWT (dovrebbe essere segreta)
jwt_secret_key = "Modbus"


bbb = paramiko.SSHClient()
bbb_ip = os.getenv('BBB_IP')
bbb_username = os.getenv('BBB_SSH_USERNAME')
bbb_password = os.getenv('BBB_SSH_PASSWORD')

@app.route('/')
def home():
    return "Welcome to Modbus2Chain Server"


# Funzione per generare un token JWT
def generate_jwt_token():
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Scadenza di 30 minuti
    payload = {
        "exp": expiration_time,
        "user" : "alex"
    }
    token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")
    return token


# Route per il login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Connessione SSH alla BBB
        bbb.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        bbb.connect(bbb_ip, username=bbb_username, password=bbb_password)

        # Esegui l'autenticazione con successo e genera il token JWT
        token = generate_jwt_token()

        # Restituisci il token JWT in risposta
        return jsonify({"token": token}), 200

    except paramiko.AuthenticationException:
        # Gestisci errori di autenticazione SSH
        return jsonify({"message": "Errore di autenticazione SSH"}), 401

    except paramiko.SSHException as e:
        # Gestisci altri errori SSH
        return jsonify({"message": f"Errore SSH: {str(e)}"}), 500

    except Exception as e:
        # Gestisci altre eccezioni generali
        return jsonify({"message": f"Errore generico: {str(e)}"}), 500


@app.route('/sendData', methods=['POST'])
def sendData():
    python_command = 'python3 /var/lib/cloud9/Modbus2Chain/app/index.py'

    # Esegui il comando Python
    stdin, stdout, stderr = bbb.exec_command(python_command)
    print("Comando lanciato!!!!")
    print(stdout.read().decode('utf-8'))

@app.route('/protected', methods=['GET'])
def protected_route():
    if not auth.authenticate_token():
        return jsonify({"message": "Token non valido"}), 401

    return jsonify({"message": "Questa è una rotta protetta"}), 200

app.run(host='192.168.178.21',port=8000)  #ip del pc locale

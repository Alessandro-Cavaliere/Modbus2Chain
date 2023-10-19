from flask import Flask, jsonify, request
import sys
import paramiko
sys.path.insert(0, 'app\routes\auth.py')
import auth
import os
import datetime
from dotenv import load_dotenv
import jwt
import utils

load_dotenv()
app = Flask("Modbus2Chain")



# Chiave segreta per la firma del token JWT (dovrebbe essere segreta)
jwt_secret_key = os.getenv('SECRET_APP')


bbb = paramiko.SSHClient()
bbb_ip = os.getenv('BBB_IP')
bbb_username = os.getenv('BBB_SSH_USERNAME')
bbb_password = os.getenv('BBB_SSH_PASSWORD')

# SSH connection to the BBB
bbb.set_missing_host_key_policy(paramiko.AutoAddPolicy())
bbb.connect(bbb_ip, username=bbb_username, password=bbb_password)
utils.load_files_on_bbb(bbb)

@app.route('/')
def home():
    return "Welcome to Modbus2Chain Server"


# Route per il login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Apply the authenticate_token_app middleware function here
        if not auth.authenticate_token_app(request.headers.get('Authorization')):
            return jsonify({"message": "Unauthorized"}), 401
        
        #restituzione utente: dao.login_user()
        user={
            "name":"alex",
            "pass":"root"
        }

        # Esegui l'autenticazione con successo e genera il token JWT
        token = auth.generate_jwt_token(user)

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
    try:
        # Apply the authenticate_token_app middleware function here
        if not auth.authenticate_token(request.headers.get('Authorization')):
            return jsonify({"message": "Unauthorized"}), 401
        
        python_command = 'python3 /var/lib/cloud9/Modbus2Chain-master/master.py'

        # Esegui il comando Python
        stdin, stdout, stderr = bbb.exec_command(python_command)
        print("Comando lanciato!!!!")
        print(stdout.read().decode('utf-8'))   

    except Exception as e:
        # Gestisci eccezioni
        print("Si è verificato un errore durante l'esecuzione del comando:", str(e))
    
    return "Comando completato con successo"  # Aggiungi una risposta HTTP appropriata


@app.route('/protected', methods=['GET'])
def protected_route():
    if not auth.authenticate_token():
        return jsonify({"message": "Token non valido"}), 401

    return jsonify({"message": "Questa è una rotta protetta"}), 200

app.run(host='0.0.0.0',port=8000)  #ip del pc locale

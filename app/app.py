from flask import Flask, jsonify, request
import sys
import paramiko
sys.path.insert(0, 'app\routes\auth.py')
import auth
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import dao
import utils

load_dotenv()
app = Flask("Modbus2Chain")

# Connessione al database MongoDB
client = MongoClient(os.getenv("HOST"))
db = client[os.getenv("DATABASE")]
print(client)
users = db["utenti"]

# Chiave segreta per la firma del token JWT (dovrebbe essere segreta)
jwt_secret_key = os.getenv('SECRET_APP')

"""
bbb = paramiko.SSHClient()
bbb_ip = os.getenv('BBB_IP')
bbb_username = os.getenv('BBB_SSH_USERNAME')
bbb_password = os.getenv('BBB_SSH_PASSWORD')

# SSH connection to the BBB
bbb.set_missing_host_key_policy(paramiko.AutoAddPolicy())
bbb.connect(bbb_ip, username=bbb_username, password=bbb_password)
utils.load_files_on_bbb(bbb)
"""
@app.route('/')
def home():
    return "Welcome to Modbus2Chain Server"


@app.route('/register', methods=['POST'])
def register():
    try:
        # Estrai i dati dal corpo della richiesta JSON
        data = request.form
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Verifica se email e password sono forniti
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        existing_user = dao.find_user_by_email(db, email)
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        # Crea un nuovo utente nel database (puoi implementare questa funzione in base alle tue esigenze)
        dao.register_user(db, email, password,first_name,last_name)

        return jsonify({"message": "Registration successful"}), 201  # 201 Created

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 500 Internal Server Error


# Route per il login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Apply the authenticate_token_app middleware function here
        if not auth.authenticate_token_app(request.headers.get('Authorization')):
            return jsonify({"message": "Unauthorized"}), 401
        
        email = request.form.get('email')
        password = request.form.get('password')
        # Verifica se email e password sono forniti
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        user =dao.login_user(db, email,password)
        if user == False:
            return jsonify({"error": "Invalid email or password"}), 401
        # Esegui l'autenticazione con successo e genera il token JWT
        token = auth.generate_jwt_token(user)
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

app.run(host='0.0.0.0',port=5000)  #ip del pc locale
from flask import  request
import jwt
import datetime
import os

# Funzione middleware per l'autenticazione dell'app
def authenticate_token_app(auth_header):
    if auth_header:
        token = auth_header.split(' ')[1]  # Estrae il token dal formato "Bearer <token>"
        print(token)
        # Verifica il token (implementa la tua logica di verifica qui)
        if token == os.getenv('SECRET_APP'):
            return True
    return False

# Funzione middleware per l'autenticazione
def authenticate_token(auth_header):
    token = auth_header and auth_header.split(' ')[1]

    # Verifica se il token è presente
    if not token:
        return False

    try:
        # Verifica e decodifica il token
        jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

# Funzione per generare un token JWT
def generate_jwt_token(user):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Scadenza di 30 minuti
    payload = {
        "exp": expiration_time,
        "user" : user
    }
    token = jwt.encode(payload,os.getenv('JWT_SECRET'), algorithm="HS256")
    return token


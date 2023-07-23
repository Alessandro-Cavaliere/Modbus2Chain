from flask import  request
import jwt
import datetime
import os

# Funzione middleware per l'autenticazione dell'app
def authenticate_token_app():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(' ')[1]  # Estrae il token dal formato "Bearer <token>"

        # Verifica il token (implementa la tua logica di verifica qui)
        if token == os.getenv('SECRET_APP'):
            return True
    return False

# Funzione middleware per l'autenticazione
def authenticate_token():
    # Ottieni il token Bearer dall'header della richiesta
    auth_header = request.headers.get('Authorization')
    token = auth_header and auth_header.split(' ')[1]

    # Verifica se il token è presente
    if not token:
        return False

    try:
        # Verifica e decodifica il token
        user = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])

        # Se il token è valido, salva l'utente nella variabile globale
        # oppure puoi anche passare l'utente nel contesto della richiesta (g)
        # per utilizzarlo nelle rotte successive
        request.user = user
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

# Funzione per generare un token JWT
def generate_token(user):
    print(datetime.date)
    token = jwt.encode({"user": user, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       os.getenv('JWT_SECRET'), algorithm="HS256")
    return token


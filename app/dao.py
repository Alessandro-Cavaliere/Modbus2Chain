from werkzeug.security import generate_password_hash, check_password_hash

def register_user(db , email, password, first_name, last_name):
    users = db['utenti']
    hashed_password = generate_password_hash(password, method='sha256')
    print(hashed_password)
    user_data = {
        'email': email,
        'password': hashed_password,
        'first_name': first_name,
        'last_name': last_name
    }
 
    if users.find_one({"email": email}):
        return False

    users.insert_one(user_data)
    print("eccoci")
    return True

def login_user(db , email, password):
    users = db['utenti']
    user = users.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return False

    return user

def find_user_by_email(db, email):
    users_collection = db["utenti"]
    
    user = users_collection.find_one({"email": email})
    
    return user

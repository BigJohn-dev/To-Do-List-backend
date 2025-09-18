from src.extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, email, password):
    user = mongo.db.users.find_one({"email": email})
    if user:
        return None

    hashed = generate_password_hash(password)
    new_user = {
        "username": username,
        "email": email,
        "password": hashed
    }
    mongo.db.users.insert_one(new_user)
    return new_user

def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def check_user_password(user, password):
    return check_password_hash(user["password"], password)

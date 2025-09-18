from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import mongo

class User:
    collection = mongo.db.users  # Mongo collection

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }
        result = User.collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return User.collection.find_one({"email": email})

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_password=False):
        data = {
            "username": self.username,
            "email": self.email,
        }
        if include_password:
            data["password_hash"] = self.password_hash
        return data

import datetime
import re
from functools import wraps
from bson import ObjectId
import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import mongo

auth_bp = Blueprint("auth", __name__)


def validate_email(email):
    pattern = r"^[\w\.-]+@gmail\.com$"
    return re.match(pattern, email) is not None


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if not validate_email(email):
        return jsonify({"error": "Invalid email. Must be a Gmail address"}), 400

    # Check if user exists
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "Email has already been used"}), 400

    hashed_password = generate_password_hash(password)

    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow()
    }

    result = mongo.db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)

    return jsonify({
        "id": user["_id"],
        "username": user["username"],
        "email": user["email"]
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect password"}), 401

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        str(current_app.config["SECRET_KEY"]),
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "user": {"id": str(user["_id"]), "username": user["username"], "email": user["email"]},
        "token": token
    }), 200


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid token format"}), 401

        token = parts[1]

        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            user_id = data["user_id"]

            # Convert back to ObjectId for MongoDB lookup
            current_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

            if not current_user:
                return jsonify({"error": "User not found"}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            print(f"JWT decode error: {e}")
            return jsonify({"error": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated



import datetime
import re
import jwt
from flask import Blueprint, request, jsonify, current_app
from src.dtos.login_dto import LoginRequest, LoginResponse
from src.models.user import User
from src.extensions import db

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

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email has already been used"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    req = LoginRequest(**data)


    user = User.query.filter_by(email=req.email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404


    if not user.check_password(req.password):
        return jsonify({"error": "Incorrect password"}), 401


    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    res = LoginResponse(
        message="Login successful",
        user={"id": user.id, "username": user.username, "email": user.email},
        token=token
    )
    return jsonify(res.__dict__), 200

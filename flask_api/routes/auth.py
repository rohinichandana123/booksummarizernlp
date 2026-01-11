from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        gender=data["gender"],
        age=data["age"],
        qualification=data["qualification"],
        occupation=data["occupation"],
        country=data["country"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"})


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    })

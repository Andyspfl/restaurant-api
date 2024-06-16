from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user_model import User
from app.utils.decorators import jwt_required, roles_required

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role")

    if not name or not email or not password or not phone or not role:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 400

    new_user = User(name, email, password, phone, role)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.find_by_email(email)
    if user and user.check_password(password):
        # Si las credenciales son válidas, genera un token JWT
        access_token = create_access_token(
            identity={"email": user.email, "role": user.role}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


@user_bp.route("/me", methods=["GET"])
@jwt_required
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200


@user_bp.route("/users", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_users():
    users = User.query.all()
    return jsonify([{"name": user.name, "email": user.email, "role": user.role} for user in users]), 200

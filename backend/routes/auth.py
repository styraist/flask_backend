import jwt

from flask import Blueprint, request, jsonify
from sqlalchemy import select
from werkzeug.security import check_password_hash

from backend.dto.credentials import CredentialsSchema
from backend import db
from backend.models.user import User
from backend.routes import secret_token



auth_bp = Blueprint("auth", __name__)
credentials_schema = CredentialsSchema()

@auth_bp.route("/login", methods=['POST'])
def login():
    d = request.json
    credentials = credentials_schema.load(d)
    
    user = db.session.scalars(select(User).where(User.username == credentials.username)).one()

    if not check_password_hash(user.password, credentials.password):
        raise Exception("Invalid password")
    
    encoded_jwt = jwt.encode(
        {"sub": user.id, "username": user.username},
        secret_token,
        algorithm="HS256")
    
    return jsonify({"token": encoded_jwt})
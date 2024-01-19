from sqlalchemy import select, insert
from werkzeug.security import generate_password_hash

from flask import Blueprint, jsonify, request, Response
from backend.dto.user import UserCreationSchema
from backend.routes import token_auth
from backend.models.user import User, UserSchema
from backend import db


users_bp = Blueprint("users", __name__, url_prefix='/users')
user_schema = UserSchema()
user_creation_schema = UserCreationSchema()


@users_bp.route("", methods=['GET'])
@token_auth.login_required
def get_all_users():
    users = db.session.scalars(select(User)).all()
    return jsonify(user_schema.dump(users, many=True))


@users_bp.route("", methods=['POST'])
def create_user():
    d = request.json
    new_user = user_creation_schema.load(d)

    db.session.execute(insert(User).values(
        username=new_user.username,
        email=new_user.email,
        password=generate_password_hash(new_user.password)
    ))
    db.session.commit()

    return Response(status=204)


@users_bp.route("/<user_id>")
@token_auth.login_required
def get_user(user_id):
    user = db.session.scalars(select(User).where(User.id == user_id)).one()
    return jsonify(user_schema.dump(user))
from flask import url_for
from sqlalchemy import select, func

from backend import db, User

def test_create_user(app_with_db):

    response = app_with_db.post(url_for("users.create_user"),
                                json={
                                    "username": "Joe",
                                    "password": "Abcdefgh",
                                    "email": "joe@mail.com"
                                })
    
    assert response.status_code == 204
    count = db.session.execute(select(func.count(User.id)).where(User.username == "Joe")).scalar_one()
    assert count == 1

def test_get_user_by_username(app_with_data):

    response = app_with_data.post(
        url_for("auth.login"),
        json={
            "username": "salih",
            "password": "pass"
        }
    )
    auth_data = response.json
    token = auth_data["token"]

    response = app_with_data.get(url_for("users.get_user",
                                         username = "salih"),
                                         headers={
                                             "Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json
    assert data["username"] == "salih"


def test_get_all_users(app_with_data):
    
    response = app_with_data.post(
        url_for("auth.login"),
        json={
            "username": "salih",
            "password": "pass"
        }
    )
    auth_data = response.json
    token = auth_data["token"]

    response = app_with_data.get(url_for("users.get_all_users"),
                                 headers={
                                     "Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
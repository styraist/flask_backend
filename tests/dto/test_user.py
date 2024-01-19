import pytest
from marshmallow import ValidationError

from backend.dto.user import UserCreationSchema


@pytest.mark.parametrize(
        "password, valid",
        [
            ("Abcde12345", True),
            ("12345Abcde", True),
            ("Abcdefghij", True),
            ("abcde12345", False),
            ("ABCDE12345", False),
            ("12345678", False),
            ("Abc123", False),
        ]
)

def test_validate_password(password, valid):
    schema = UserCreationSchema()
    data = {
        "username": "salih",
        "password": password,
        "email": "salih@salih.com"
    }

    try:
        user = schema.load(data)
        assert valid

        assert user is not None
        assert user.username == data["username"]
        assert user.password == password
        assert user.email == data["email"]
    except ValidationError:
        assert not valid

def test_missing_fields():
    schema = UserCreationSchema()
    data = {
        "username": "salih",
        "password": "Abdce12345"
    }

    with pytest.raises(ValidationError):
        schema.load(data)
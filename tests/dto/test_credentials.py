import pytest
from marshmallow import ValidationError

from backend.dto.credentials import CredentialsSchema


def test_missing_fields():

    schema = CredentialsSchema()
    data = {
        "username": "salih",
    }

    with pytest.raises(ValidationError):
        schema.load(data)
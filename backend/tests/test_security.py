import uuid

import jwt
import pytest

from app.security import (
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("correct-horse-battery-staple")
    assert verify_password("correct-horse-battery-staple", hashed)
    assert not verify_password("wrong-password", hashed)


def test_access_token_roundtrip() -> None:
    user_id = uuid.uuid4()
    token = create_access_token(user_id=user_id, role="admin")
    payload = decode_access_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["role"] == "admin"


def test_access_token_rejects_tampering() -> None:
    token = create_access_token(user_id=uuid.uuid4(), role="admin")
    with pytest.raises(jwt.PyJWTError):
        decode_access_token(token + "tampered")


def test_generate_refresh_token_is_hashed_consistently() -> None:
    raw, token_hash = generate_refresh_token()
    assert token_hash == hash_refresh_token(raw)
    assert raw != token_hash

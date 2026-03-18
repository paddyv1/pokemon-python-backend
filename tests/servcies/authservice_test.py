from datetime import timedelta

import jwt
import pytest
from fastapi import HTTPException

from app.models.user import User
from app.services.authservice import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_user,
    does_user_exist,
    does_username_password_match,
    get_current_user_normal,
    get_password_hash,
    retrieve_user,
    verify_password,
)


def test_get_password_hash_and_verify_password():
    plain = "pikachu123"
    hashed = get_password_hash(plain)

    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrongpass", hashed) is False


def test_create_user_inserts_hashed_user(db_session):
    created = create_user("ash", "pikachu123", db_session)
    saved = db_session.query(User).filter(User.username == "ash").first()

    assert created is True
    assert saved is not None
    assert saved.username == "ash"
    assert saved.hashed_password != "pikachu123"
    assert verify_password("pikachu123", saved.hashed_password) is True


def test_create_user_returns_false_for_duplicate_username(db_session):
    first = create_user("misty", "staryu123", db_session)
    second = create_user("misty", "anotherpass123", db_session)
    count = db_session.query(User).filter(User.username == "misty").count()

    assert first is True
    assert second is False
    assert count == 1


def test_does_user_exist_true_and_false(db_session):
    create_user("brock", "onix12345", db_session)

    assert does_user_exist("brock", db_session) is True
    assert does_user_exist("gary", db_session) is False


def test_does_username_password_match(db_session):
    create_user("jessie", "meowth123", db_session)

    assert does_username_password_match("jessie", "meowth123", db_session) is True
    assert does_username_password_match("jessie", "wrongpass", db_session) is False
    assert does_username_password_match("unknown", "whatever123", db_session) is False


def test_retrieve_user_returns_user_schema_or_none(db_session):
    create_user("tracey", "scyther123", db_session)

    found = retrieve_user("tracey", db_session)
    missing = retrieve_user("nobody", db_session)

    assert found is not None
    assert found.username == "tracey"
    assert missing is None


def test_create_access_token_contains_subject_and_exp():
    token = create_access_token({"sub": "ash"}, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["sub"] == "ash"
    assert "exp" in decoded


@pytest.mark.anyio
async def test_get_current_user_normal_returns_user_for_valid_token(db_session):
    create_user("may", "torchic123", db_session)
    token = create_access_token({"sub": "may"}, expires_delta=timedelta(minutes=5))

    user = await get_current_user_normal(token=token, db=db_session)

    assert user.username == "may"


@pytest.mark.anyio
async def test_get_current_user_normal_raises_401_for_invalid_token(db_session):
    with pytest.raises(HTTPException) as exc:
        await get_current_user_normal(token="not-a-real-token", db=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


@pytest.mark.anyio
async def test_get_current_user_normal_raises_401_when_user_not_found(db_session):
    token = create_access_token({"sub": "missing-user"}, expires_delta=timedelta(minutes=5))

    with pytest.raises(HTTPException) as exc:
        await get_current_user_normal(token=token, db=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
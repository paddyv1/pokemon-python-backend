from app.models.user import User


def test_register_success(client, db_session):
    payload = {
        "username": "ashketchum",
        "password": "pikachu123",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

    user = db_session.query(User).filter(User.username == "ashketchum").first()
    assert user is not None
    assert user.username == "ashketchum"
    assert user.hashed_password != "pikachu123"
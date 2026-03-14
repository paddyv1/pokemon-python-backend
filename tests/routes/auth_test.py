from app.models.user import User

def test_register_success(client, db_session):
    payload = {"username": "ashketchum", "password": "pikachu123"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

    user = db_session.query(User).filter(User.username == "ashketchum").first()
    assert user is not None
    assert user.hashed_password != "pikachu123"

def test_register_duplicate_username_returns_error(client):
    payload = {"username": "misty", "password": "staryu123"}

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json() == {"error": "User already exists"}

def test_register_short_password_fails_validation(client):
    response = client.post(
        "/auth/register",
        json={"username": "brock", "password": "short"},
    )

    assert response.status_code == 422

def test_login_success_returns_token(client):
    client.post(
        "/auth/register",
        json={"username": "gary", "password": "eevee123"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "gary", "password": "eevee123"},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["token_type"] == "bearer"
    assert body["access_token"]

def test_login_wrong_password_returns_400(client):
    client.post(
        "/auth/register",
        json={"username": "jessie", "password": "meowth123"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "jessie", "password": "wrongpass123"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_unknown_user_returns_400(client):
    response = client.post(
        "/auth/login",
        data={"username": "unknown", "password": "whatever123"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}

def test_me_requires_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_me_returns_current_user(client):
    client.post(
        "/auth/register",
        json={"username": "tracey", "password": "scyther123"},
    )
    login = client.post(
        "/auth/login",
        data={"username": "tracey", "password": "scyther123"},
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"username": "tracey"}
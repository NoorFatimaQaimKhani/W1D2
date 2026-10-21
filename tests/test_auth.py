from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def login(username="teacher01", password="Password123"):
    return client.post("/auth/login", json={"username": username, "password": password})


def test_login_then_me_returns_the_same_user():
    response = login()
    assert response.status_code == 200
    token = response.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json() == {"username": "teacher01"}


def test_wrong_password_and_unknown_user_give_the_same_error():
    wrong_password = login(password="WrongPass123")
    unknown_user = login(username="nobody99")
    assert wrong_password.status_code == 401
    assert unknown_user.status_code == 401
    assert wrong_password.json() == unknown_user.json()


def test_me_without_token_returns_401():
    assert client.get("/auth/me").status_code == 401


def test_short_password_is_rejected_with_422():
    assert login(password="short").status_code == 422
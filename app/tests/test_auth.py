from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post("/api/v1/auth/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    response = client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

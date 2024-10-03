import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_login(use_test_client: TestClient):
    # criando um usuário
    payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    response = use_test_client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    # logando com o usuário criado
    payload = {"username": "devMaster", "password": "jujuba"}
    response = use_test_client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    # response_json = response.json()
    # assert response_json["access_token"]
    # assert response_json["refresh_token"]
    # assert response_json["access_token_expires"]
    # assert response_json["nickname"] == "dev"
    # assert response_json["email"] == "dev@test.com.br"
    # assert response_json["phone"] == "9999999999"





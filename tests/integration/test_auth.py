from unittest.mock import patch
import pytest


@pytest.mark.asyncio
async def test_signup(use_test_client):
    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201


@pytest.mark.asyncio
async def test_login(use_test_client):
    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Logando com o usuário criado
    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    response_json = login_response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json


@pytest.mark.asyncio
async def test_logout(use_test_client):
    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Logando com o usuário criado
    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Realizando o logout
    headers = {"Authorization": f"Bearer {access_token}"}
    logout_response = use_test_client.post("/api/v1/auth/logout", headers=headers)
    assert logout_response.status_code == 200

    response_json = logout_response.json()
    assert response_json["message"] == "Successfully logged out"

@pytest.mark.asyncio
@patch("app.core.mailer.send_pin_email")
async def test_forgot_password(mock_send_pin_email, use_test_client):
    mock_send_pin_email.return_value = None

    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Solicitando recuperação de senha
    forgot_password_payload = {"email": "master@dev.com"}
    forgot_password_response = use_test_client.post("/api/v1/auth/forgot-password", json=forgot_password_payload)
    assert forgot_password_response.status_code == 200

    response_json = forgot_password_response.json()
    assert response_json["message"] == "PIN sent to email"

@pytest.mark.asyncio
@patch("app.core.mailer.send_pin_email")
@patch("app.api.v1.auth.auth_repository.AuthRepository.generate_pin")
async def test_reset_password(mock_generate_pin, mock_send_pin_email, use_test_client):
    mock_send_pin_email.return_value = None
    mock_generate_pin.return_value = "123456"

    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Solicitando recuperação de senha
    forgot_password_payload = {"email": "master@dev.com"}
    forgot_password_response = use_test_client.post("/api/v1/auth/forgot-password", json=forgot_password_payload)
    assert forgot_password_response.status_code == 200

    response_json = forgot_password_response.json()
    assert response_json["message"] == "PIN sent to email"

    # Resetando a senha
    reset_password_payload = {
        "email": "master@dev.com",
        "pin": "123456",
        "new_password": "nova_senha"
    }
    reset_password_response = use_test_client.post("/api/v1/auth/reset-password", json=reset_password_payload)
    assert reset_password_response.status_code == 200

    response_json = reset_password_response.json()
    assert response_json["message"] == "Password reset successfully."

@pytest.mark.asyncio
async def test_change_password(use_test_client):
    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Logando com o usuário criado
    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Alterando a senha
    change_password_payload = {
        "old_password": "jujuba",
        "new_password": "nova_senha"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    change_password_response = use_test_client.put("/api/v1/auth/change-password", json=change_password_payload, headers=headers)
    assert change_password_response.status_code == 200

    response_json = change_password_response.json()
    assert response_json["message"] == "Password changed successfully"

@pytest.mark.asyncio
async def test_get_me(use_test_client):
    # Criando um usuário
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Logando com o usuário criado
    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Verificando dados do usuário autenticado
    headers = {"Authorization": f"Bearer {access_token}"}
    get_me_response = use_test_client.get("/api/v1/auth/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    assert response_json["username"] == "devMaster"
    assert response_json["email"] == "master@dev.com"
    assert response_json["name"] == "dev"
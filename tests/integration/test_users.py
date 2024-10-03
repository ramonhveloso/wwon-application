import pytest


@pytest.mark.asyncio
async def test_get_users_me(use_test_client):
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

    # Obtendo perfil do usuário autenticado
    headers = {"Authorization": f"Bearer {access_token}"}
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    assert response_json["email"] == "master@dev.com"
    assert response_json["name"] == "dev"


@pytest.mark.asyncio
async def test_put_users_me(use_test_client):
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

    # Atualizando perfil do usuário autenticado
    update_profile_payload = {
        "username": "devMasterUpdated",
        "email": "master_updated@dev.com",
        "name": "devUpdated",
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    put_me_response = use_test_client.put(
        "/api/v1/users/me", json=update_profile_payload, headers=headers
    )
    assert put_me_response.status_code == 200

    response_json = put_me_response.json()
    assert response_json["email"] == "master_updated@dev.com"
    assert response_json["name"] == "devUpdated"


@pytest.mark.asyncio
async def test_get_users(use_test_client):
    # Criando um usuário admin
    signup_payload = {
        "username": "adminUser",
        "password": "adminPass",
        "email": "admin@dev.com",
        "name": "admin",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Logando com o usuário admin
    login_payload = {"username": "admin@dev.com", "password": "adminPass"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Listando usuários (admin)
    headers = {"Authorization": f"Bearer {access_token}"}
    get_users_response = use_test_client.get("/api/v1/users", headers=headers)
    assert get_users_response.status_code == 200

    response_json = get_users_response.json()
    assert "users" in response_json


@pytest.mark.asyncio
async def test_get_user(use_test_client):
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

    # Atualizando dados de um usuário específico
    headers = {"Authorization": f"Bearer {access_token}"}
    # Obtendo perfil do usuário autenticado
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    user_id = response_json["id"]

    headers = {"Authorization": f"Bearer {access_token}"}
    get_user_response = use_test_client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_user_response.status_code == 200

    response_json = get_user_response.json()
    assert response_json["email"] == "master@dev.com"
    assert response_json["name"] == "dev"


@pytest.mark.asyncio
async def test_put_user(use_test_client):
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

    # Atualizando dados de um usuário específico
    headers = {"Authorization": f"Bearer {access_token}"}
    # Obtendo perfil do usuário autenticado
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    user_id = response_json["id"]

    update_user_payload = {
        "username": "devMasterUpdated",
        "email": "master_updated@dev.com",
        "name": "devUpdated",
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    put_user_response = use_test_client.put(
        f"/api/v1/users/{user_id}", json=update_user_payload, headers=headers
    )
    assert put_user_response.status_code == 200

    response_json = put_user_response.json()
    assert response_json["email"] == "master_updated@dev.com"
    assert response_json["name"] == "devUpdated"


@pytest.mark.asyncio
async def test_delete_user(use_test_client):
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

    # Atualizando dados de um usuário específico
    headers = {"Authorization": f"Bearer {access_token}"}
    # Obtendo perfil do usuário autenticado
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    user_id = response_json["id"]

    headers = {"Authorization": f"Bearer {access_token}"}
    delete_user_response = use_test_client.delete(
        f"/api/v1/users/{user_id}", headers=headers
    )
    assert delete_user_response.status_code == 200

    # Verificando se o usuário foi deletado
    get_user_response = use_test_client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_user_response.status_code == 404

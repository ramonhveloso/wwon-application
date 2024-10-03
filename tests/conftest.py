from dotenv import load_dotenv
import pytest
import os

# Carrega o arquivo .env
load_dotenv()

# Pega a URL do banco de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

os.environ.update(
    {
        "DATABASE_URL":f"{DATABASE_URL}",
        "SECRET_KEY":f"{SECRET_KEY}",
        "SMTP_SERVER":f"{SMTP_SERVER}",
        "SMTP_PORT":f"{SMTP_PORT}",
        "SMTP_USERNAME":f"{SMTP_USERNAME}",
        "SMTP_PASSWORD":f"{SMTP_PASSWORD}",
    }
)

@pytest.fixture
def use_test_client():
    from starlette.testclient import TestClient
    from app.api.v1.router import router
    return TestClient(router)
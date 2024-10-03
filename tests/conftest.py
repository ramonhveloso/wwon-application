import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.main import app
from app.middleware.dependencies import get_db

# Configurar o banco de dados PostgreSQL para testes
DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("TEST_DATABASE_URL não está configurado")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)


# Fixture para o banco de dados de teste
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# Fixture para o cliente de teste
@pytest.fixture(scope="function")
def use_test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

from fastapi import Depends
from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_service import AuthService
from app.db.session import SessionLocal
from app.core.security import decode_access_token, oauth2_scheme

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_verifier(token = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload.get("sub")


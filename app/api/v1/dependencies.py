from fastapi import Depends

from app.core.security import decode_access_token, oauth2_scheme
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_verifier(token=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload.get("sub")

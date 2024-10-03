from fastapi import Depends
from pydantic import BaseModel

from app.core.security import decode_access_token, oauth2_scheme
from app.database.session import SessionLocal


class AuthUser(BaseModel):
    id: int
    email: str
    token: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def jwt_middleware(token=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return AuthUser(id=payload.get("id"), email=payload.get("email"), token=token)

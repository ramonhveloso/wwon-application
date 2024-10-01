from typing import Optional

from pydantic import BaseModel, EmailStr

from app.api.v1.users.user_schemas import UserCreate


class AuthCreateUser(UserCreate):
    pass


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ResponseGetUsersMe(BaseModel):
    username: str
    email: EmailStr
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    chave_pix: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str

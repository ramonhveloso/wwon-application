from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Obter perfil do usuário autenticado
class GetUsersMeResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


# Atualizar perfil do usuário autenticado
class PutUsersMeRequest(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


class PutUsersMeResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


# (Admin) Listar usuários
class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


class GetUsersResponse(BaseModel):
    users: List[User]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


# Ver perfil de um usuário específico
class GetUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


# Atualizar dados de um usuário específico
class PutUserRequest(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


class PutUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


# Excluir um usuário específico
class DeleteUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, data):
        return cls(**data)

from typing import Optional

from pydantic import BaseModel, EmailStr


class Response(BaseModel):
    message: str

    class Config:
        from_attributes = True


class PostSignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    chave_pix: Optional[str] = None


class PostSignUpResponse(BaseModel):
    username: str
    email: EmailStr
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    chave_pix: Optional[str] = None


class PostLoginRequest(BaseModel):
    email: EmailStr
    password: str


class PostLoginResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class PostLogoutRequest(BaseModel):
    token: str


class PostLogoutResponse(Response):
    pass


class PostForgotPasswordRequest(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class PostForgotPasswordResponse(Response):
    pass


class PostResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    class Config:
        from_attributes = True


class PostResetPasswordResponse(Response):
    pass


class PutChangePasswordRequest(BaseModel):
    token: str
    old_password: str
    new_password: str

    class Config:
        from_attributes = True


class PutChangePasswordResponse(Response):
    pass


class GetMeRequest(BaseModel):
    token: str

    class Config:
        from_attributes = True


class GetMeResponse(BaseModel):
    username: str
    email: EmailStr
    name: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    chave_pix: Optional[str] = None

    class Config:
        from_attributes = True

from datetime import timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import (
    GetMeRequest,
    GetMeResponse,
    PostForgotPasswordRequest,
    PostForgotPasswordResponse,
    PostLoginRequest,
    PostLoginResponse,
    PostLogoutRequest,
    PostLogoutResponse,
    PostResetPasswordRequest,
    PostSignUpRequest,
    PostSignUpResponse,
    PutChangePasswordRequest,
    PutChangePasswordResponse,
)
from app.core.mailer import send_password_reset_email
from app.core.security import create_access_token, get_password_hash, verify_password


class AuthService:
    def __init__(self, auth_repository: AuthRepository = Depends()):
        self.auth_repository = auth_repository

    async def create_user(
        self, db: Session, data: PostSignUpRequest
    ) -> PostSignUpResponse:
        hashed_password = get_password_hash(password=data.password)
        data.password = hashed_password
        response_repository = await self.auth_repository.create_user(db, data)
        return PostSignUpResponse(
            username=response_repository.username,
            email=response_repository.email,
            name=response_repository.name,
            cpf=response_repository.cpf,
            cnpj=response_repository.cnpj,
            chave_pix=response_repository.chave_pix,
        )

    async def authenticate_user(self, db: Session, data: PostLoginRequest):
        # Autenticar o usuário com e-mail e senha
        db_user = await self.auth_repository.get_user_by_email(db, data.email)
        if db_user and verify_password(data.password, db_user.password):
            return db_user
        return None

    def create_access_token(self, user) -> PostLoginResponse:
        # Criar token de acesso para o usuário
        token_data = {"sub": user.email}
        response = {
            "access_token": create_access_token(token_data),
            "token_type": "bearer",
        }
        return PostLoginResponse(**response)

    async def logout(self, db: Session, data: PostLogoutRequest) -> PostLogoutResponse:
        # Logout do usuário, adicionando o token à blacklist
        token_id = await self.auth_repository.verify_token(data.token)
        if token_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        await self.auth_repository.add_token(db, data.token)
        return PostLogoutResponse(message="Successfully logged out")

    def is_token_blacklisted(self, db: Session, token: str) -> bool:
        """Verifica se um token está na blacklist."""
        token_id = self.auth_repository.verify_token(token)
        return self.auth_repository.is_token_blacklisted(db, token_id)

    async def forgot_password(
        self, db: Session, data: PostForgotPasswordRequest
    ) -> PostForgotPasswordResponse:
        # Enviar email com link para reset de senha
        user = await self.auth_repository.get_user_by_email(db, data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        reset_token = create_access_token(
            {"sub": data.email}, expires_delta=timedelta(minutes=30)
        )
        send_password_reset_email(user.email, reset_token)
        PostForgotPasswordResponse(message="Password reset link sent to email")

    async def reset_password(self, data: PostResetPasswordRequest, db: Session):
        # Resetar a senha com base no token
        email = await self.auth_repository.verify_token(data.token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        hashed_password = get_password_hash(data.new_password)
        self.auth_repository.update_password(db, email, hashed_password)

    async def change_password(
        self, data: PutChangePasswordRequest, db: Session
    ) -> PutChangePasswordResponse:
        # Alterar a senha do usuário autenticado
        email = await self.auth_repository.verify_token(data.token)
        user = self.auth_repository.get_user_by_email(db, email)
        if not user or not verify_password(data.old_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        hashed_password = get_password_hash(data.new_password)
        self.auth_repository.update_password(db, email, hashed_password)
        return PutChangePasswordResponse(message="Password changed successfully")

    async def get_authenticated_user(
        self, data: GetMeRequest, db: Session
    ) -> GetMeResponse:
        # Obter informações do usuário autenticado com base no token
        email = self.auth_repository.verify_token(data.token)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await self.auth_repository.get_user_by_email(db, email)
        return GetMeResponse(
            username=user.username,
            email=user.email,
            name=user.name,
            cpf=user.cpf,
            cnpj=user.cnpj,
            chave_pix=user.chave_pix,
        )

    def verify_token(self, token: str):
        # Verificar token
        return self.auth_repository.verify_token(token)

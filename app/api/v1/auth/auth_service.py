from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import (
    GetAuthMeResponse,
    PostForgotPasswordRequest,
    PostForgotPasswordResponse,
    PostLoginResponse,
    PostLogoutResponse,
    PostResetPasswordRequest,
    PostResetPasswordResponse,
    PostSignUpRequest,
    PostSignUpResponse,
    PutChangePasswordRequest,
    PutChangePasswordResponse,
)
from app.core.mailer import send_pin_email
from app.core.security import create_access_token, get_password_hash, verify_password
from app.middleware.dependencies import AuthUser


class AuthService:
    def __init__(self, auth_repository: AuthRepository = Depends()):
        self.auth_repository = auth_repository

    async def create_user(
        self, db: Session, data: PostSignUpRequest
    ) -> PostSignUpResponse:
        hashed_password = get_password_hash(password=data.password)
        data.password = hashed_password
        try:
            response_repository = await self.auth_repository.create_user(db, data)
        except:
            # Lança uma exceção HTTP com status 409 se ocorrer um erro específico
            raise HTTPException(status_code=409, detail=f"Conflict")

        return PostSignUpResponse(
            username=response_repository.username,
            email=response_repository.email,
            name=response_repository.name,
            cpf=response_repository.cpf,
            cnpj=response_repository.cnpj,
            chave_pix=response_repository.chave_pix,
        )

    async def authenticate_user(self, db: Session, data: OAuth2PasswordRequestForm):
        # Autenticar o usuário com e-mail e senha
        db_user = await self.auth_repository.get_user_by_email(db, data.username)
        if db_user and verify_password(data.password, db_user.password):
            return db_user
        if not db_user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    def create_access_token(self, user) -> PostLoginResponse:
        # Criar token de acesso para o usuário
        token_data = {"id": user.id, "email": user.email}
        response = {
            "access_token": create_access_token(token_data),
            "token_type": "bearer",
        }
        return PostLoginResponse(**response)

    async def logout(self, db: Session, authuser: AuthUser) -> PostLogoutResponse:
        # Logout do usuário, adicionando o token à blacklist
        if authuser.token is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        await self.auth_repository.add_token(db, authuser.token)
        return PostLogoutResponse(message="Successfully logged out")

    async def is_token_blacklisted(self, db: Session, token: str) -> bool:
        """Verifica se um token está na blacklist."""
        token_id = self.auth_repository.verify_token(token)
        if token_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return await self.auth_repository.is_token_blacklisted(db, str(token_id))

    async def forgot_password(
        self, db: Session, data: PostForgotPasswordRequest
    ) -> PostForgotPasswordResponse:
        # Envia email com o pin para reset de senha
        user = await self.auth_repository.get_user_by_email(db, data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Gerar PIN de 6 dígitos
        pin = self.auth_repository.generate_pin()
        
        # Define o tempo de expiração do PIN
        pin_expiration = datetime.now() + timedelta(minutes=5)

        # Armazena o PIN e sua expiração no banco de dados
        await self.auth_repository.save_pin(db, user.id, pin, pin_expiration)

        # Enviar o PIN por e-mail
        await send_pin_email(user.email, pin)

        return PostForgotPasswordResponse(message="PIN sent to email")

    async def reset_password(
        self, data: PostResetPasswordRequest, db: Session
    ) -> PostResetPasswordResponse:
        # Verificar se o PIN é válido
        pin_validation_result = await self.auth_repository.verify_pin(
            db=db, email=data.email, pin=data.pin
        )

        # Verifica o resultado da validação do PIN
        if "error" in pin_validation_result:
            # Lança a exceção apropriada com base na mensagem de erro
            error_detail = pin_validation_result["error"]

            if error_detail == "Invalid PIN":
                raise HTTPException(
                    status_code=400, detail="The provided PIN is invalid."
                )
            elif error_detail == "PIN has expired":
                raise HTTPException(
                    status_code=400, detail="The provided PIN has expired."
                )
            elif error_detail == "User not found":
                raise HTTPException(status_code=404, detail="User not found.")

        # Se o PIN for válido, hash a nova senha
        hashed_password = get_password_hash(data.new_password)

        # Atualizar a senha no repositório
        await self.auth_repository.update_password(db, data.email, hashed_password)

        return PostResetPasswordResponse(message="Password reset successfully.")

    async def change_password(
        self, authuser: AuthUser, data: PutChangePasswordRequest, db: Session
    ) -> PutChangePasswordResponse:
        # Alterar a senha do usuário autenticado
        user = await self.auth_repository.get_user_by_id(db, authuser.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user or not verify_password(data.old_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        hashed_password = get_password_hash(data.new_password)
        await self.auth_repository.update_password(db, authuser.email, hashed_password)
        return PutChangePasswordResponse(message="Password changed successfully")

    async def get_authenticated_user(self, id: int, db: Session) -> GetAuthMeResponse:
        # Obter informações do usuário autenticado com base no token
        if not id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await self.auth_repository.get_user_by_id(db, id)
        return GetAuthMeResponse(
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

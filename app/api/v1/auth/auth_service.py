from datetime import timedelta

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import AuthRequest
from app.api.v1.users.user_schemas import UserCreate
from app.core.mailer import send_password_reset_email
from app.core.security import create_access_token, get_password_hash, verify_password


class AuthService:
    def __init__(self, auth_repository: AuthRepository = Depends()):
        self.auth_repository = auth_repository

    def create_user(self, db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        return self.auth_repository.create_user(db, user)

    def authenticate_user(self, db: Session, user: AuthRequest):
        # Autenticar o usuário com e-mail e senha
        db_user = self.auth_repository.get_user_by_email(db, user.email)
        if db_user and verify_password(user.password, db_user.password):
            return db_user
        return None

    def create_access_token(self, user):
        # Criar token de acesso para o usuário
        token_data = {"sub": user.email}
        return {"access_token": create_access_token(token_data), "token_type": "bearer"}

    def logout(self, db: Session, token: str):
        # Logout do usuário, adicionando o token à blacklist
        token_id = self.auth_repository.verify_token(token)
        if token_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        self.auth_repository.add_token(db, token_id)

    def is_token_blacklisted(self, db: Session, token: str) -> bool:
        """Verifica se um token está na blacklist."""
        token_id = self.auth_repository.verify_token(token)
        return self.auth_repository.is_token_blacklisted(db, token_id)

    def forgot_password(self, db: Session, email: str):
        # Enviar email com link para reset de senha
        user = self.auth_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        reset_token = create_access_token(
            {"sub": email}, expires_delta=timedelta(minutes=30)
        )
        send_password_reset_email(user.email, reset_token)

    def reset_password(self, token: str, new_password: str, db: Session):
        # Resetar a senha com base no token
        email = self.auth_repository.verify_token(token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        hashed_password = get_password_hash(new_password)
        self.auth_repository.update_password(db, email, hashed_password)

    def change_password(
        self, email: str, old_password: str, new_password: str, db: Session
    ):
        # Alterar a senha do usuário autenticado
        user = self.auth_repository.get_user_by_email(db, email)
        if not user or not verify_password(old_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        hashed_password = get_password_hash(new_password)
        self.auth_repository.update_password(db, email, hashed_password)

    def get_authenticated_user(self, db: Session, token: str):
        # Obter informações do usuário autenticado com base no token
        email = self.auth_repository.verify_token(token)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return self.auth_repository.get_user_by_email(db, email)

    def verify_token(self, token: str):
        # Verificar token
        return self.auth_repository.verify_token(token)

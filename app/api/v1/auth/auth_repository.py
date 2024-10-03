from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.api.v1.auth.auth_schemas import PostSignUpRequest
from app.core.security import decode_access_token
from app.database.models.blacklist import TokenBlacklist
from app.database.models.user import User


class AuthRepository:
    async def create_user(self, db: Session, data: PostSignUpRequest):
        """Criação do usuário no banco de dados."""
        db_user = User(
            username=data.username,
            password=data.password,
            name=data.name,
            email=data.email,
            cpf=data.cpf,
            cnpj=data.cnpj,
            chave_pix=data.chave_pix,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, db: Session, id: int):
        """Obter o usuário pelo id."""
        return db.query(User).filter(User.id == id).first()

    async def get_user_by_email(self, db: Session, email: str):
        """Obter o usuário pelo e-mail."""
        return db.query(User).filter(User.email == email).first()

    async def update_password(self, db: Session, email: str, new_password: str):
        """Atualizar a senha do usuário."""
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.password = new_password  # type: ignore
            db.commit()

    async def verify_token(self, token: str):
        """Decodificar o token JWT para verificar se é válido."""
        payload = decode_access_token(token)
        return payload if payload else None

    async def add_token(self, db: Session, token_id: str):
        """Adicionar um token à blacklist."""
        token = TokenBlacklist(id=token_id)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    async def is_token_blacklisted(self, db: Session, token_id: str) -> bool:
        """Verificar se um token está na blacklist."""
        return (
            db.query(TokenBlacklist).filter(TokenBlacklist.id == token_id).first()
            is not None
        )

    async def save_pin(self, db: Session, user_id: int, pin: str, expiration: datetime):
        user = db.query(User).filter(User.id == user_id).first()
        user.reset_pin = pin  # type: ignore
        user.reset_pin_expiration = expiration  # type: ignore
        db.add(user)
        db.commit()

    async def verify_pin(self, db: Session, email: str, pin: str):
        """Lógica para verificar o PIN no banco de dados"""
        user = db.query(User).filter(User.email == email).first()

        if user:
            if user.reset_pin == pin:
                if user.reset_pin_expiration >= datetime.now(timezone.utc):
                    return {
                        "email": user.email,
                        "expiration": user.reset_pin_expiration,
                    }
                return {"error": "PIN has expired"}
            return {"error": "Invalid PIN"}

        return {"error": "User not found"}

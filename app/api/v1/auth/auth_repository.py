# app/repositories/auth_repository.py

from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.blacklist import TokenBlacklist
from app.core.security import decode_access_token
from app.api.v1.users.user_schemas import UserCreate

class AuthRepository:
    def create_user(self, db: Session, user: UserCreate):
        """Criação do usuário no banco de dados."""
        db_user = User(email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, db: Session, email: str):
        """Obter o usuário pelo e-mail."""
        return db.query(User).filter(User.email == email).first()

    def update_password(self, db: Session, email: str, new_password: str):
        """Atualizar a senha do usuário."""
        user = self.get_user_by_email(db, email)
        if user:
            user.password = new_password
            db.commit()

    def verify_token(self, token: str):
        """Decodificar o token JWT para verificar se é válido."""
        payload = decode_access_token(token)
        return payload.get("sub") if payload else None

    def add_token(self, db: Session, token_id: str):
        """Adicionar um token à blacklist."""
        token = TokenBlacklist(id=token_id)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def is_token_blacklisted(self, db: Session, token_id: str) -> bool:
        """Verificar se um token está na blacklist."""
        return db.query(TokenBlacklist).filter(TokenBlacklist.id == token_id).first() is not None

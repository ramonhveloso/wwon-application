from sqlalchemy.orm import Session

from app.api.v1.users.user_schemas import PutUserRequest, PutUsersMeRequest
from app.db.models.user import User


class UserRepository:
    async def get_user_by_email(self, db: Session, email: str):
        """Obtém o usuário pelo email."""
        return db.query(User).filter(User.email == email).first()

    async def get_user_by_id(self, db: Session, user_id: int):
        """Obtém o usuário pelo ID."""
        return db.query(User).filter(User.id == user_id).first()

    async def update_user_profile(
        self, db: Session, user: User, data: PutUsersMeRequest
    ):
        """Atualiza o perfil do usuário autenticado."""
        user.name = data.name if data.name else user.name  # type: ignore
        user.email = data.email if data.email else user.email  # type: ignore
        db.commit()
        db.refresh(user)
        return user

    async def update_user(self, db: Session, user: User, data: PutUserRequest):
        """Atualiza os dados de um usuário específico."""
        user.name = data.name if data.name else user.name  # type: ignore
        user.email = data.email if data.email else user.email  # type: ignore
        db.commit()
        db.refresh(user)
        return user

    async def delete_user(self, db: Session, user: User):
        """Exclui um usuário do banco de dados."""
        db.delete(user)
        db.commit()
        return user

    async def get_all_users(self, db: Session):
        """Retorna todos os usuários no banco de dados."""
        return db.query(User).all()

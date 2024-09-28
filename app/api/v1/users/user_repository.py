from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: User) -> None:
        db.add(user)
        db.commit()
        db.refresh(user)

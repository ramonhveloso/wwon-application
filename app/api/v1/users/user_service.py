from sqlalchemy.orm import Session
from app.api.v1.users.user_schemas import UserRequest
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.v1.users.user_repository import get_user_by_username

class UserService:
    def create_user(db: Session, user: UserRequest):
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(db: Session, user: UserRequest):
        db_user = get_user_by_username(db, username=user.username)
        if db_user and verify_password(user.password, db_user.hashed_password):
            return db_user
        return False

    def create_access_token(user: User):
        return create_access_token(data={"sub": user.username})

    def get_all_users(db: Session):
        return db.query(User).all()

    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

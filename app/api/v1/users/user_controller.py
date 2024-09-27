from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.api.v1.users.user_schemas import User
from app.api.v1.users.user_service import UserService


router = APIRouter()

@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

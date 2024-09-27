from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.users.user_schemas import user as user_schema
from app.api.v1.users.user_service import user_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[user_schema.User])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=user_schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

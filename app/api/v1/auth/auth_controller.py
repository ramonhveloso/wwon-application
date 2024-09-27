from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.users.user_schemas import user as user_schema
from app.api.v1.users.user_service import user_service
from app.db.session import get_db

router = APIRouter()

@router.post("/signup", response_model=user_schema.User)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.post("/login", response_model=user_schema.Token)
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user_service.create_access_token(user)

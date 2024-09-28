from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_db
from app.api.v1.users.user_schemas import Token, User, UserCreate, UserRequest
from app.api.v1.users.user_service import UserService

router = APIRouter()


@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


@router.post("/login", response_model=Token)
def login(user: UserRequest, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return UserService.create_access_token(user)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.api.v1.items.item_controller import create_item
from app.api.v1.users.user_schemas import Token, User, UserRequest
from app.api.v1.users.user_service import UserService


router = APIRouter()

@router.post("/signup", response_model=User)
def signup(user: UserRequest, db: Session = Depends(get_db)):
    return create_item(db, user)

@router.post("/login", response_model=Token)
def login(user: UserRequest, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return UserService.create_access_token(user)

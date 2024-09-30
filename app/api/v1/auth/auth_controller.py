from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_db
from app.api.v1.users.user_schemas import Token, User, UserCreate, UserRequest
from app.api.v1.users.user_service import UserService

router = APIRouter()


# Registro de novo usuário
@router.post("/auth/signup", response_model=User)
def post_signup(user: UserCreate, db: Session = Depends(get_db)):
    print(user)
    return UserService.create_user(db, user)


# Login do usuário
@router.post("/auth/login", response_model=Token)
def post_login(user: UserRequest, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return UserService.create_access_token(user)


# Logout do usuário
@router.post("/auth/logout", response_model=Token)
def post_logout(user: UserRequest, db: Session = Depends(get_db)):
    pass


# Solicitar recuperação de senha
@router.post("/auth/forgot-password", response_model=Token)
def post_forgot_password(user: UserRequest, db: Session = Depends(get_db)):
    pass


# Solicitar recuperação de senha
@router.post("/auth/reset-password", response_model=Token)
def post_reset_password(user: UserRequest, db: Session = Depends(get_db)):
    pass


# Alterar senha
@router.put("/auth/change-password", response_model=Token)
def put_reset_password(user: UserRequest, db: Session = Depends(get_db)):
    pass


# Verificar token e dados do usuário autenticado
@router.get("/auth/me", response_model=Token)
def get_reset_password(user: UserRequest, db: Session = Depends(get_db)):
    pass

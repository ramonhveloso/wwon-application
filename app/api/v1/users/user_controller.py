from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_db
from app.api.v1.users.user_schemas import User
from app.api.v1.users.user_service import UserService

router = APIRouter()


# Obter perfil do usuário autenticado
@router.get("/users/me", response_model=list[User])
def get_users_me(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# Atualizar perfil do usuário autenticado
@router.put("/users/me", response_model=list[User])
def put_users_me(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# (Admin) Listar usuários
@router.get("/users/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


# Ver perfil de um usuário específico
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Atualizar dados de um usuário específico
@router.put("/users/{user_id}", response_model=User)
def put_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Excluir um usuário específico
@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

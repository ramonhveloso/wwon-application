from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_db, token_verifier
from app.api.v1.users.user_repository import UserRepository
from app.api.v1.users.user_schemas import (
    DeleteUserResponse,
    GetUserResponse,
    GetUsersMeResponse,
    GetUsersResponse,
    PutUserRequest,
    PutUserResponse,
    PutUsersMeRequest,
    PutUsersMeResponse,
    User,
)
from app.api.v1.users.user_service import UserService

router = APIRouter()
user_service = UserService(UserRepository())


# Obter perfil do usuário autenticado
@router.get("/me")
async def get_users_me(
    email: str = Depends(token_verifier), db: Session = Depends(get_db)
) -> GetUsersMeResponse:
    response_service = await user_service.get_authenticated_user(db=db, email=email)
    return GetUsersMeResponse.model_validate(response_service)


# Atualizar perfil do usuário autenticado
@router.put("/me")
async def put_users_me(
    data: PutUsersMeRequest,
    email: str = Depends(token_verifier),
    db: Session = Depends(get_db),
) -> PutUsersMeResponse:
    response_service = await user_service.update_user_profile(
        db=db, email=email, data=data
    )
    return PutUsersMeResponse.model_validate(response_service)


# (Admin) Listar usuários
@router.get("/")
async def get_users(
    db: Session = Depends(get_db), email: str = Depends(token_verifier)
) -> GetUsersResponse:
    response_service = await user_service.get_all_users(db)
    return GetUsersResponse(
        users=[User.model_validate(user) for user in response_service]
    )


# Ver perfil de um usuário específico
@router.get("/{user_id}")
async def get_user(
    user_id: int, db: Session = Depends(get_db), email: str = Depends(token_verifier)
) -> GetUserResponse:
    response_service = await user_service.get_user_by_id(db, user_id)
    if not response_service:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserResponse.model_validate(response_service)


# Atualizar dados de um usuário específico
@router.put("/{user_id}")
async def put_user(
    data: PutUserRequest,
    user_id: int,
    db: Session = Depends(get_db),
    email: str = Depends(token_verifier),
) -> PutUserResponse:
    response_service = await user_service.update_user(db=db, user_id=user_id, data=data)
    return PutUserResponse.model_validate(response_service)


# Excluir um usuário específico
@router.delete("/{user_id}")
async def delete_user(
    user_id: int, db: Session = Depends(get_db), mail: str = Depends(token_verifier)
) -> DeleteUserResponse:
    response_service = await user_service.delete_user(db=db, user_id=user_id)
    if not response_service:
        raise HTTPException(status_code=404, detail="User not found")
    return DeleteUserResponse.model_validate(response_service)

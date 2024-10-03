from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.users.user_repository import UserRepository
from app.api.v1.users.user_schemas import (
    DeleteUserResponse,
    GetUserResponse,
    GetUsersMeResponse,
    PutUserRequest,
    PutUserResponse,
    PutUsersMeRequest,
    PutUsersMeResponse,
)
from app.db.models.user import User


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def get_authenticated_user(
        self, db: Session, email: str
    ) -> GetUsersMeResponse:
        user = await self.user_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return GetUsersMeResponse(
            id=int(user.id),
            email=str(user.email),
            name=str(user.name),
        )

    async def update_user_profile(
        self, db: Session, email: str, data: PutUsersMeRequest
    ) -> PutUsersMeResponse:
        user = await self.user_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Atualizar o perfil do usuário
        updated_user = await self.user_repository.update_user_profile(db, user, data)
        return PutUsersMeResponse(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
        )

    async def get_all_users(self, db: Session) -> List[User]:
        users = await self.user_repository.get_all_users(db)
        return [
            User(id=user.id, email=user.email, name=user.name, is_active=user.is_active)
            for user in users
        ]

    async def get_user_by_id(self, db: Session, user_id: int) -> GetUserResponse:
        user = await self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return GetUserResponse(id=user.id, email=user.email, name=user.name)

    async def update_user(
        self, db: Session, user_id: int, data: PutUserRequest
    ) -> PutUserResponse:
        user = await self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Atualizar dados do usuário
        updated_user = await self.user_repository.update_user(db, user, data)
        return PutUserResponse(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
        )

    async def delete_user(self, db: Session, user_id: int) -> DeleteUserResponse:
        user = await self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Excluir usuário
        deleted_user = await self.user_repository.delete_user(db, user)
        return DeleteUserResponse(
            id=deleted_user.id,
            email=deleted_user.email,
            name=deleted_user.name,
        )

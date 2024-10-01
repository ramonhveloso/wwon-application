from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import (
    GetMeRequest,
    GetMeResponse,
    PostForgotPasswordRequest,
    PostForgotPasswordResponse,
    PostLoginRequest,
    PostLoginResponse,
    PostLogoutRequest,
    PostLogoutResponse,
    PostResetPasswordRequest,
    PostResetPasswordResponse,
    PostSignUpRequest,
    PostSignUpResponse,
    PutChangePasswordRequest,
    PutChangePasswordResponse,
)
from app.api.v1.auth.auth_service import AuthService
from app.api.v1.dependencies import get_db

router = APIRouter()
auth_service = AuthService(AuthRepository())


# Registro de novo usuário
@router.post("/signup")
async def post_signup(
    data: PostSignUpRequest, db: Session = Depends(get_db)
) -> PostSignUpResponse:
    response_service = await auth_service.create_user(db=db, data=data)
    return PostSignUpResponse.model_validate(response_service)


# Login do usuário
@router.post("/login")
async def post_login(
    data: PostLoginRequest, db: Session = Depends(get_db)
) -> PostLoginResponse:
    authenticated_user = await auth_service.authenticate_user(db=db, data=data)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    response_service = auth_service.create_access_token(authenticated_user)
    return PostLoginResponse.model_validate(response_service)


# Logout do usuário
@router.post("/logout")
async def post_logout(
    data: PostLogoutRequest, db: Session = Depends(get_db)
) -> PostLogoutResponse:
    response_service = await auth_service.logout(db=db, data=data)
    return PostLogoutResponse.model_validate(response_service)


# Solicitar recuperação de senha
@router.post("/forgot-password")
async def post_forgot_password(
    data: PostForgotPasswordRequest, db: Session = Depends(get_db)
) -> PostForgotPasswordResponse:
    response_service = await auth_service.forgot_password(db=db, data=data)
    return PostForgotPasswordResponse.model_validate(response_service)


# Resetar senha
@router.post("/reset-password")
async def post_reset_password(
    data: PostResetPasswordRequest, db: Session = Depends(get_db)
) -> PostResetPasswordResponse:
    response_service = await auth_service.reset_password(db=db, data=data)
    return PostResetPasswordResponse.model_validate(response_service)


# # Alterar senha
@router.put("/change-password")
async def put_change_password(
    data: PutChangePasswordRequest,
    db: Session = Depends(get_db),
) -> PutChangePasswordResponse:
    response_service = await auth_service.change_password(db=db, data=data)
    return PutChangePasswordResponse.model_validate(response_service)


# Verificar dados do usuário autenticado
@router.get("/me")
async def get_me(data: GetMeRequest, db: Session = Depends(get_db)) -> GetMeResponse:
    response_service = await AuthService.get_authenticated_user(db=db, data=data)
    return None

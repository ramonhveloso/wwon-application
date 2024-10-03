from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_repository import AuthRepository
from app.api.v1.auth.auth_schemas import (
    GetAuthMeResponse,
    PostForgotPasswordRequest,
    PostForgotPasswordResponse,
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
from app.api.v1.dependencies import get_db, token_verifier

router = APIRouter()
auth_service = AuthService(AuthRepository())


# Registro de novo usuário
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def post_signup(
    data: PostSignUpRequest, db: Session = Depends(get_db)
) -> PostSignUpResponse:
    response_service = await auth_service.create_user(db=db, data=data)
    return PostSignUpResponse.model_validate(response_service)


# Login do usuário
@router.post("/login")
async def post_login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> PostLoginResponse:
    authenticated_user = await auth_service.authenticate_user(db=db, data=data)
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


# Alterar senha
@router.put("/change-password")
async def put_change_password(
    data: PutChangePasswordRequest,
    db: Session = Depends(get_db),
) -> PutChangePasswordResponse:
    response_service = await auth_service.change_password(db=db, data=data)
    return PutChangePasswordResponse.model_validate(response_service)


# Verificar dados do usuário autenticado
@router.get("/me")
async def get_me(
    email: str = Depends(token_verifier), db: Session = Depends(get_db)
) -> GetAuthMeResponse:
    response_service = await auth_service.get_authenticated_user(db=db, email=email)
    return GetAuthMeResponse.model_validate(response_service)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.auth_schemas import AuthCreateUser, AuthRequest, Token, User
from app.api.v1.auth.auth_service import AuthService
from app.api.v1.dependencies import get_db

router = APIRouter()


class AuthController:
    def __init__(self, auth_service: AuthService = Depends()):
        self.auth_service = auth_service

    # Registro de novo usuário
    @router.post("/auth/signup", response_model=User)
    def post_signup(self, user: AuthCreateUser, db: Session = Depends(get_db)):
        return self.auth_service.create_user(db, user)

    # Login do usuário
    @router.post("/auth/login", response_model=Token)
    def post_login(self, user: AuthRequest, db: Session = Depends(get_db)):
        authenticated_user = self.auth_service.authenticate_user(db, user)
        if not authenticated_user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        return self.auth_service.create_access_token(authenticated_user)

    # Logout do usuário
    @router.post("/auth/logout", response_model=str)
    def post_logout(self, db: Session = Depends(get_db), token: str = Depends()):
        self.auth_service.logout(db, token)
        return {"detail": "Successfully logged out"}

    # Solicitar recuperação de senha
    @router.post("/auth/forgot-password", response_model=str)
    def post_forgot_password(self, user: AuthRequest, db: Session = Depends(get_db)):
        self.auth_service.forgot_password(db, user.email)
        return {"detail": "Password reset link sent to email"}

    # Resetar senha
    @router.post("/auth/reset-password", response_model=str)
    def post_reset_password(
        self, token: str, new_password: str, db: Session = Depends(get_db)
    ):
        self.auth_service.reset_password(token, new_password, db)
        return {"detail": "Password reset successfully"}

    # Alterar senha
    @router.put("/auth/change-password", response_model=str)
    def put_change_password(
        self,
        user: AuthRequest,
        old_password: str,
        new_password: str,
        db: Session = Depends(get_db),
    ):
        self.auth_service.change_password(user.email, old_password, new_password, db)
        return {"detail": "Password changed successfully"}

    # Verificar dados do usuário autenticado
    @router.get("/auth/me", response_model=User)
    def get_me(self, db: Session = Depends(get_db), token: str = Depends()):
        return self.auth_service.get_authenticated_user(db, token)

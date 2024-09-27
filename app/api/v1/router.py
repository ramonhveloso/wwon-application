from fastapi import APIRouter
from app.api.v1.auth.auth_controller import router as auth_router
from app.api.v1.users.user_controller import router as users_router
from app.api.v1.items.item_controller import router as items_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(items_router, prefix="/items", tags=["Items"])

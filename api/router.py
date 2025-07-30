from fastapi import APIRouter
from users.routes import router as user_router
from engine.routes import router as engine_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/api/users", tags=["Users"])
api_router.include_router(engine_router, prefix='/api', tags=['Core Features'])

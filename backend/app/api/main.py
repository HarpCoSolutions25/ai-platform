from backend.app.api.routes import oganization
from fastapi import APIRouter


from app.api.routes import items, login, private, users, utils,project,organization

from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(oganization.router)
api_router.include_router(project.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

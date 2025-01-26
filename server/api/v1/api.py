from fastapi import APIRouter

from server.api.v1.endpoints.users import router as users_router
from server.api.v1.endpoints.items import router as items_router


router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(items_router, prefix="/items", tags=["Items"])

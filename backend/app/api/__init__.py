"""API routes module"""

from fastapi import APIRouter
from app.api import tasks, notifications

router = APIRouter()
router.include_router(tasks.router)
router.include_router(notifications.router)

__all__ = ["router"]

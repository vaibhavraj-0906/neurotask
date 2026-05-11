"""
Notifications API routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import NotificationResponse, MessageResponse
from app.services import NotificationService


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/due", response_model=list[NotificationResponse])
def get_due_reminders(db: Session = Depends(get_db)):
    """
    Get all due reminders
    """
    service = NotificationService(db)
    reminders = service.get_due_reminders()
    return reminders


@router.get("/upcoming", response_model=list[NotificationResponse])
def get_upcoming_reminders(hours: int = 24, db: Session = Depends(get_db)):
    """
    Get reminders for the next N hours
    """
    service = NotificationService(db)
    reminders = service.get_upcoming_reminders(hours)
    return reminders


@router.post("/check", response_model=MessageResponse)
def check_notifications(db: Session = Depends(get_db)):
    """
    Manually trigger notification check
    """
    service = NotificationService(db)
    service._check_due_reminders()
    return MessageResponse(message="Notifications checked", success=True)

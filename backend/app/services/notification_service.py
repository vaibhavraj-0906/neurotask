"""
Notification Service - Handles task reminders and notifications
"""

import time
from datetime import datetime, timedelta
from typing import List, Callable
from threading import Thread
import logging

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for managing notifications"""
    
    def __init__(self, db: Session, notification_callback: Callable = None):
        """
        Initialize notification service
        
        Args:
            db: Database session
            notification_callback: Callback function for notifications
        """
        self.db = db
        self.notification_callback = notification_callback
        self._running = False
        self._scheduler_thread = None
    
    def start_scheduler(self, check_interval: int = 60):
        """
        Start background notification scheduler
        
        Args:
            check_interval: Check for reminders every N seconds
        """
        if self._running:
            return
        
        self._running = True
        self._scheduler_thread = Thread(
            target=self._scheduler_loop,
            args=(check_interval,),
            daemon=True
        )
        self._scheduler_thread.start()
        logger.info("Notification scheduler started")
    
    def stop_scheduler(self):
        """Stop background scheduler"""
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        logger.info("Notification scheduler stopped")
    
    def _scheduler_loop(self, check_interval: int):
        """Background scheduler loop"""
        while self._running:
            try:
                self._check_due_reminders()
                time.sleep(check_interval)
            except Exception as e:
                logger.error(f"Error in notification scheduler: {e}")
    
    def _check_due_reminders(self):
        """Check for due reminders and send notifications"""
        from app.models import Task
        
        now = datetime.utcnow()
        
        # Find tasks with due reminders
        due_tasks = self.db.query(Task).filter(
            Task.reminder_time <= now,
            Task.completed == False,
            Task.reminder_time.isnot(None)
        ).all()
        
        for task in due_tasks:
            self._send_notification(task)
    
    def _send_notification(self, task):
        """Send notification for task"""
        if self.notification_callback:
            notification = {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "deadline": task.deadline.isoformat() if task.deadline else None,
            }
            self.notification_callback(notification)
        
        logger.info(f"Notification sent for task: {task.title}")
    
    def get_due_reminders(self) -> List[dict]:
        """Get list of due reminders"""
        from app.models import Task
        
        now = datetime.utcnow()
        
        due_tasks = self.db.query(Task).filter(
            Task.reminder_time <= now,
            Task.completed == False,
            Task.reminder_time.isnot(None)
        ).all()
        
        return [
            {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
            }
            for task in due_tasks
        ]
    
    def schedule_reminder(self, task_id: str, reminder_time: datetime) -> bool:
        """Schedule a reminder for a task"""
        from app.models import Task
        
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.reminder_time = reminder_time
        self.db.commit()
        return True
    
    def get_upcoming_reminders(self, hours: int = 24) -> List[dict]:
        """Get reminders for next N hours"""
        from app.models import Task
        
        now = datetime.utcnow()
        future = now + timedelta(hours=hours)
        
        upcoming = self.db.query(Task).filter(
            Task.reminder_time.between(now, future),
            Task.completed == False,
            Task.reminder_time.isnot(None)
        ).all()
        
        return [
            {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "reminder_time": task.reminder_time.isoformat(),
            }
            for task in upcoming
        ]

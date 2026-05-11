"""
Task Service - Business logic for task management
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Task, PriorityEnum
from app.nlp import NLPEngine


class TaskService:
    """Service for task operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.nlp_engine = NLPEngine()
    
    def create_task_from_natural_language(self, text: str) -> Task:
        """
        Create a task from natural language input
        
        Args:
            text: User input in natural language
            
        Returns:
            Created Task object
        """
        # Parse input
        parsed = self.nlp_engine.parse(text)
        
        # Create task
        task = Task(
            title=parsed["task_title"],
            description=text,
            original_text=text,
            priority=PriorityEnum(parsed["priority"]),
            category=parsed["category"],
            deadline=self._parse_datetime(parsed["deadline"]) if parsed["deadline"] else None,
            reminder_time=self._parse_datetime(parsed["reminder_time"]) if parsed["reminder_time"] else None,
            recurrence=parsed["recurrence"],
            confidence_score=parsed["confidence_score"],
            parsed_data=parsed,
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.db.query(Task).all()
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority"""
        return self.db.query(Task).filter(Task.priority == PriorityEnum(priority)).all()
    
    def get_active_tasks(self) -> List[Task]:
        """Get active (not completed) tasks"""
        return self.db.query(Task).filter(Task.completed == False).all()
    
    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due in next N days"""
        from datetime import datetime, timedelta
        today = datetime.utcnow()
        future = today + timedelta(days=days)
        
        return self.db.query(Task).filter(
            Task.deadline.between(today, future),
            Task.completed == False
        ).all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update task"""
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task, key) and key not in ["id", "created_at"]:
                setattr(task, key, value)
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def complete_task(self, task_id: str) -> Optional[Task]:
        """Mark task as complete"""
        return self.update_task(task_id, completed=True, completed_at=datetime.utcnow())
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        return self.db.query(Task).filter(
            (Task.title.ilike(f"%{query}%")) | 
            (Task.description.ilike(f"%{query}%"))
        ).all()
    
    @staticmethod
    def _parse_datetime(iso_string: Optional[str]) -> Optional[datetime]:
        """Parse ISO format datetime string"""
        if not iso_string:
            return None
        try:
            return datetime.fromisoformat(iso_string)
        except:
            return None

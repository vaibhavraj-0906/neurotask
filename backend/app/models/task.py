"""
Task model for database
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Enum
from sqlalchemy.dialects.sqlite import JSON
import enum
import uuid

from app.database import Base


class PriorityEnum(str, enum.Enum):
    """Priority levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core fields
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Priority and category
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    
    # Dates and times
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    deadline = Column(DateTime, nullable=True, index=True)
    reminder_time = Column(DateTime, nullable=True, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Recurrence
    recurrence = Column(String(200), nullable=True)  # e.g., "FREQ=WEEKLY;BYDAY=MO,WE,FR"
    
    # Status
    completed = Column(Boolean, default=False, nullable=False, index=True)
    
    # NLP-related
    original_text = Column(Text, nullable=True)  # Original user input
    confidence_score = Column(Integer, nullable=True)  # 0-100 confidence in parsing
    
    # Metadata
    parsed_data = Column(JSON, nullable=True)  # Store full parsed JSON
    tags = Column(JSON, nullable=True)  # List of tags
    
    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value if isinstance(self.priority, PriorityEnum) else self.priority,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "reminder_time": self.reminder_time.isoformat() if self.reminder_time else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "recurrence": self.recurrence,
            "completed": self.completed,
            "original_text": self.original_text,
            "confidence_score": self.confidence_score,
            "tags": self.tags,
        }

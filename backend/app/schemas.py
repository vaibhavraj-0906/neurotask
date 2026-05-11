"""
Pydantic schemas for request/response validation
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TaskCreateRequest(BaseModel):
    """Request schema for task creation"""

    text: str = Field(
        ...,
        description="Natural language task description"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Finish OS lab report tonight"
            }
        }
    )


class TaskUpdateRequest(BaseModel):
    """Request schema for task update"""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None

    deadline: Optional[datetime] = None
    reminder_time: Optional[datetime] = None

    recurrence: Optional[str] = None
    completed: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "priority": "high",
                "deadline": "2026-12-31T23:59:59"
            }
        }
    )


class TaskResponse(BaseModel):
    """Response schema for task"""

    id: str
    title: str

    description: Optional[str] = None

    priority: str
    category: Optional[str] = None

    created_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    recurrence: Optional[str] = None

    completed: bool

    original_text: Optional[str] = None
    confidence_score: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ParseResponse(BaseModel):
    """Response schema for NLP parsing"""

    raw_input: str
    intent: str
    intent_confidence: float

    task_title: str

    deadline: Optional[str] = None

    priority: str
    category: Optional[str] = None
    recurrence: Optional[str] = None

    confidence_score: int

    parsed_at: str


class NotificationResponse(BaseModel):
    """Response schema for notification"""

    task_id: str
    title: str

    priority: str

    deadline: Optional[datetime] = None
    reminder_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
    success: bool


class ErrorResponse(BaseModel):
    """Error response"""

    error: str
    details: Optional[str] = None
    success: bool = False
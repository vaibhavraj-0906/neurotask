"""
Pydantic schemas for request/response validation
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreateRequest(BaseModel):
    """Request schema for task creation"""
    text: str = Field(..., description="Natural language task description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Finish OS lab report tonight"
            }
        }


class TaskUpdateRequest(BaseModel):
    """Request schema for task update"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    deadline: Optional[str] = None
    reminder_time: Optional[str] = None
    recurrence: Optional[str] = None
    completed: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "priority": "high",
                "deadline": "2024-12-31T23:59:59"
            }
        }


class TaskResponse(BaseModel):
    """Response schema for task"""
    id: str
    title: str
    description: Optional[str]
    priority: str
    category: Optional[str]
    created_at: Optional[str]
    deadline: Optional[str]
    reminder_time: Optional[str]
    completed_at: Optional[str]
    recurrence: Optional[str]
    completed: bool
    original_text: Optional[str]
    confidence_score: Optional[int]
    
    class Config:
        from_attributes = True


class ParseResponse(BaseModel):
    """Response schema for NLP parsing"""
    raw_input: str
    intent: str
    intent_confidence: float
    task_title: str
    deadline: Optional[str]
    priority: str
    category: Optional[str]
    recurrence: Optional[str]
    confidence_score: int
    parsed_at: str


class NotificationResponse(BaseModel):
    """Response schema for notification"""
    task_id: str
    title: str
    priority: str
    deadline: Optional[str]
    reminder_time: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    details: Optional[str] = None
    success: bool = False

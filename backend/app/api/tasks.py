"""
Task API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    ParseResponse,
    MessageResponse
)

from app.services import TaskService
from app.nlp import NLPEngine
from app.models import PriorityEnum


router = APIRouter(prefix="/api/tasks", tags=["tasks"])
nlp_engine = NLPEngine()


@router.post("/parse", response_model=ParseResponse)
def parse_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    """
    Parse natural language input without creating a task
    Useful for previewing what the AI understood
    """
    try:
        parsed = nlp_engine.parse(request.text)
        return ParseResponse(**parsed)

    except Exception as e:
        print("PARSE ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=TaskResponse)
def create_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    """
    Create a task from natural language input
    """
    try:
        service = TaskService(db)

        task = service.create_task_from_natural_language(
            request.text
        )

        return TaskResponse.from_orm(task)

    except Exception as e:
        print("CREATE TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    completed: bool = Query(
        None,
        description="Filter by completion status"
    ),

    priority: str = Query(
        None,
        description="Filter by priority"
    ),

    category: str = Query(
        None,
        description="Filter by category"
    ),

    db: Session = Depends(get_db)
):
    """
    List all tasks with optional filters
    """

    try:
        service = TaskService(db)

        # Get all tasks
        tasks = service.get_all_tasks()

        # Filter by completed
        if completed is not None:
            tasks = [
                t for t in tasks
                if t.completed == completed
            ]

        # Filter by priority
        if priority:
            tasks = [
                t for t in tasks
                if str(
                    t.priority.value
                    if hasattr(t.priority, "value")
                    else t.priority
                ) == priority
            ]

        # Filter by category
        if category:
            tasks = [
                t for t in tasks
                if t.category == category
            ]

        return [
            TaskResponse.from_orm(t)
            for t in tasks
        ]

    except Exception as e:
        print("LIST TASKS ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/upcoming", response_model=list[TaskResponse])
def get_upcoming_tasks(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get tasks due in the next N days
    """

    try:
        service = TaskService(db)

        tasks = service.get_upcoming_tasks(days)

        return [
            TaskResponse.from_orm(t)
            for t in tasks
        ]

    except Exception as e:
        print("UPCOMING TASKS ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Get a specific task by ID
    """

    try:
        service = TaskService(db)

        task = service.get_task_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return TaskResponse.from_orm(task)

    except HTTPException:
        raise

    except Exception as e:
        print("GET TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    request: TaskUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update a task
    """

    try:
        service = TaskService(db)

        task = service.get_task_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        # Remove None values
        update_data = {
            k: v
            for k, v in request.dict().items()
            if v is not None
        }

        # Convert priority string to enum
        if "priority" in update_data:
            update_data["priority"] = PriorityEnum(
                update_data["priority"]
            )

        updated_task = service.update_task(
            task_id,
            **update_data
        )

        return TaskResponse.from_orm(updated_task)

    except HTTPException:
        raise

    except Exception as e:
        print("UPDATE TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Mark task as complete
    """

    try:
        service = TaskService(db)

        task = service.complete_task(task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return TaskResponse.from_orm(task)

    except HTTPException:
        raise

    except Exception as e:
        print("COMPLETE TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete task
    """

    try:
        service = TaskService(db)

        success = service.delete_task(task_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return MessageResponse(
            message="Task deleted successfully",
            success=True
        )

    except HTTPException:
        raise

    except Exception as e:
        print("DELETE TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/query", response_model=list[TaskResponse])
def search_tasks(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Search tasks
    """

    try:
        service = TaskService(db)

        tasks = service.search_tasks(q)

        return [
            TaskResponse.from_orm(t)
            for t in tasks
        ]

    except Exception as e:
        print("SEARCH TASK ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))
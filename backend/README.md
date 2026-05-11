# NeuroTask Backend

This is the FastAPI backend for the NeuroTask NLP-powered to-do list application.

## Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the server**:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Project Structure

- `app/` - Main application code
  - `main.py` - FastAPI application entry point
  - `config.py` - Configuration settings
  - `schemas.py` - Pydantic models for request/response
  - `models/` - Database models
  - `database/` - Database configuration
  - `nlp/` - NLP engine (intent parsing, entity extraction)
  - `services/` - Business logic (TaskService, NotificationService)
  - `api/` - API routes

## API Endpoints

### Tasks
- `POST /api/tasks/parse` - Parse natural language without creating task
- `POST /api/tasks/create` - Create task from natural language
- `GET /api/tasks/` - List all tasks (with filters)
- `GET /api/tasks/upcoming` - Get upcoming tasks
- `GET /api/tasks/{task_id}` - Get task by ID
- `PUT /api/tasks/{task_id}` - Update task
- `POST /api/tasks/{task_id}/complete` - Mark task as complete
- `DELETE /api/tasks/{task_id}` - Delete task
- `GET /api/tasks/search/query` - Search tasks

### Notifications
- `GET /api/notifications/due` - Get due reminders
- `GET /api/notifications/upcoming` - Get upcoming reminders
- `POST /api/notifications/check` - Manually check notifications

## Example Usage

**Create a task from natural language:**
```bash
curl -X POST "http://localhost:8000/api/tasks/create" \
  -H "Content-Type: application/json" \
  -d '{"text": "Finish OS lab report tonight"}'
```

**Parse input without creating:**
```bash
curl -X POST "http://localhost:8000/api/tasks/parse" \
  -H "Content-Type: application/json" \
  -d '{"text": "Gym every Monday Wednesday Friday at 6 am"}'
```

**List all tasks:**
```bash
curl "http://localhost:8000/api/tasks/"
```

**Mark task as complete:**
```bash
curl -X POST "http://localhost:8000/api/tasks/{task_id}/complete"
```

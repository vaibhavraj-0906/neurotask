# NeuroTask API Documentation

Complete API reference for NeuroTask backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API is open (no authentication required). In production, consider adding:
- JWT tokens
- API keys
- OAuth2

## Common Response Format

### Success Response
```json
{
  "id": "uuid",
  "title": "Task title",
  "priority": "high|medium|low",
  // ... other fields
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": "Additional details (optional)",
  "success": false
}
```

---

## Endpoints

### Health & Info

#### Get API Status
```
GET /
```

**Response:**
```json
{
  "message": "NeuroTask API",
  "version": "1.0.0",
  "status": "running"
}
```

#### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Tasks

#### Parse Natural Language (Preview)
```
POST /api/tasks/parse
```

Parse input without creating a task. Useful for showing preview before creation.

**Request:**
```json
{
  "text": "Finish OS lab report tonight"
}
```

**Response:**
```json
{
  "raw_input": "Finish OS lab report tonight",
  "intent": "create_task",
  "intent_confidence": 0.9,
  "task_title": "Finish OS lab report",
  "deadline": "2024-01-15T21:00:00",
  "priority": "medium",
  "category": "study",
  "recurrence": null,
  "confidence_score": 85,
  "parsed_at": "2024-01-15T12:00:00"
}
```

---

#### Create Task from Natural Language
```
POST /api/tasks/create
```

Create a new task from natural language input.

**Request:**
```json
{
  "text": "Gym every Monday Wednesday Friday at 6 am"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Gym",
  "description": "Gym every Monday Wednesday Friday at 6 am",
  "priority": "low",
  "category": "fitness",
  "created_at": "2024-01-15T12:00:00",
  "deadline": null,
  "reminder_time": "2024-01-15T06:00:00",
  "completed_at": null,
  "recurrence": "FREQ=WEEKLY;BYDAY=MO,WE,FR",
  "completed": false,
  "original_text": "Gym every Monday Wednesday Friday at 6 am",
  "confidence_score": 92
}
```

---

#### List All Tasks
```
GET /api/tasks/
```

Get all tasks with optional filters.

**Query Parameters:**
- `completed` (boolean) - Filter by completion status
- `priority` (string) - Filter by priority: `high`, `medium`, `low`
- `category` (string) - Filter by category name

**Example:**
```
GET /api/tasks/?priority=high&completed=false
```

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish OS lab report",
    "priority": "high",
    // ...
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Team meeting",
    "priority": "high",
    // ...
  }
]
```

---

#### Get Upcoming Tasks
```
GET /api/tasks/upcoming
```

Get tasks due in the next N days.

**Query Parameters:**
- `days` (integer, 1-90) - Number of days ahead. Default: 7

**Example:**
```
GET /api/tasks/upcoming?days=30
```

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Submit DSA assignment",
    "deadline": "2024-01-20T23:59:59",
    "priority": "high",
    // ...
  }
]
```

---

#### Get Task by ID
```
GET /api/tasks/{task_id}
```

Get a specific task.

**Path Parameters:**
- `task_id` (string) - Task UUID

**Example:**
```
GET /api/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Finish OS lab report",
  "priority": "medium",
  // ... all task fields
}
```

**Status Codes:**
- `200` - Success
- `404` - Task not found

---

#### Update Task
```
PUT /api/tasks/{task_id}
```

Update task fields.

**Path Parameters:**
- `task_id` (string) - Task UUID

**Request:**
```json
{
  "title": "Updated title",
  "priority": "high",
  "deadline": "2024-01-20T18:00:00",
  "category": "work"
}
```

Only include fields you want to update. Null fields are ignored.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "priority": "high",
  // ... updated task
}
```

---

#### Complete Task
```
POST /api/tasks/{task_id}/complete
```

Mark a task as complete.

**Path Parameters:**
- `task_id` (string) - Task UUID

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Finish OS lab report",
  "completed": true,
  "completed_at": "2024-01-15T14:30:00",
  // ...
}
```

---

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

Delete a task permanently.

**Path Parameters:**
- `task_id` (string) - Task UUID

**Response:**
```json
{
  "message": "Task deleted successfully",
  "success": true
}
```

**Status Codes:**
- `200` - Deleted successfully
- `404` - Task not found

---

#### Search Tasks
```
GET /api/tasks/search/query
```

Search tasks by title or description.

**Query Parameters:**
- `q` (string, required) - Search query (minimum 1 character)

**Example:**
```
GET /api/tasks/search/query?q=assignment
```

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish OS assignment",
    "description": "Complete chapter 3-5 of OS textbook",
    // ...
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "DSA assignment submission",
    // ...
  }
]
```

---

### Notifications

#### Get Due Reminders
```
GET /api/notifications/due
```

Get all reminders that are due right now.

**Response:**
```json
[
  {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Team meeting",
    "priority": "high",
    "deadline": "2024-01-15T14:00:00"
  }
]
```

---

#### Get Upcoming Reminders
```
GET /api/notifications/upcoming
```

Get reminders for the next N hours.

**Query Parameters:**
- `hours` (integer) - Hours ahead. Default: 24

**Example:**
```
GET /api/notifications/upcoming?hours=48
```

**Response:**
```json
[
  {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Submit assignment",
    "priority": "high",
    "reminder_time": "2024-01-15T20:00:00"
  }
]
```

---

#### Check Notifications
```
POST /api/notifications/check
```

Manually trigger notification check (useful for testing).

**Response:**
```json
{
  "message": "Notifications checked",
  "success": true
}
```

---

## Data Models

### Task

```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string or null",
  "priority": "high | medium | low",
  "category": "string or null",
  "created_at": "ISO 8601 datetime",
  "deadline": "ISO 8601 datetime or null",
  "reminder_time": "ISO 8601 datetime or null",
  "completed_at": "ISO 8601 datetime or null",
  "recurrence": "RRULE string or null",
  "completed": "boolean",
  "original_text": "string (raw user input)",
  "confidence_score": "integer (0-100)"
}
```

### ParseResult

```json
{
  "raw_input": "string",
  "intent": "create_task | edit_task | delete_task | complete_task | list_tasks | search_tasks",
  "intent_confidence": "float (0.0-1.0)",
  "task_title": "string",
  "deadline": "ISO 8601 datetime or null",
  "priority": "high | medium | low",
  "category": "string or null",
  "recurrence": "RRULE string or null",
  "confidence_score": "integer (0-100)",
  "parsed_at": "ISO 8601 datetime"
}
```

### Notification

```json
{
  "task_id": "string (UUID)",
  "title": "string",
  "priority": "high | medium | low",
  "deadline": "ISO 8601 datetime or null",
  "reminder_time": "ISO 8601 datetime or null"
}
```

---

## Error Codes

| Code | Error | Meaning |
|------|-------|---------|
| 200 | - | Success |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## Rate Limiting

Currently no rate limiting. In production, consider implementing:
- 100 requests per minute per IP
- 10,000 requests per day per user

---

## CORS

The API allows requests from all origins. In production, restrict to your frontend domain:

```python
allow_origins=["https://neurotask.app"]
```

---

## Pagination

Currently not implemented. For large datasets, consider adding:
- `?page=1&limit=20`
- `?offset=0&limit=50`

---

## Examples

### Create Multiple Tasks

```bash
# Create tasks from natural language
curl -X POST "http://localhost:8000/api/tasks/create" \
  -H "Content-Type: application/json" \
  -d '{"text": "Gym tomorrow at 6am"}'

curl -X POST "http://localhost:8000/api/tasks/create" \
  -H "Content-Type: application/json" \
  -d '{"text": "Study for exam this weekend"}'

curl -X POST "http://localhost:8000/api/tasks/create" \
  -H "Content-Type: application/json" \
  -d '{"text": "Pay electricity bill by Friday"}'
```

### Get High-Priority Active Tasks

```bash
curl "http://localhost:8000/api/tasks/?priority=high&completed=false"
```

### Complete a Task

```bash
curl -X POST "http://localhost:8000/api/tasks/550e8400-e29b-41d4-a716-446655440000/complete"
```

### Search Tasks

```bash
curl "http://localhost:8000/api/tasks/search/query?q=meeting"
```

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Task CRUD operations
- NLP parsing
- Notifications system

---

## Support

- Documentation: See docs/
- Issues: GitHub Issues
- Email: support@neurotask.dev

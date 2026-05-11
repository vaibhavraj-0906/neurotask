# NeuroTask - AI-Powered NLP To-Do List Application

> **"Type naturally. The AI understands everything."**

NeuroTask is a modern, intelligent desktop productivity application that lets users create, edit, and manage tasks using **natural language** instead of traditional forms. Powered by advanced NLP and an AI-first design philosophy.

## 🎯 Core Vision

The application is built on a simple premise: **typing naturally should be the primary interaction model**. No forms, no dropdowns, no complexity—just conversational task management.

**Example inputs the AI understands:**

```
"Remind me to submit the DSA assignment tomorrow at 8"
"Gym every Monday Wednesday Friday"
"Call mom in 2 hours"
"Finish OS lab report tonight"
"Pay electricity bill before Friday"
"Team meeting next Monday at 10 AM"
```

The system intelligently extracts:
- **Task title** - What needs to be done?
- **Date/Time** - When is it due?
- **Priority** - How urgent is it?
- **Recurrence** - Does it repeat?
- **Category** - What type of task?
- **Confidence score** - How confident is the AI?

---

## 🚀 Features

### 1. **Natural Language Task Input**
Users create tasks by typing conversationally. No structured forms required.

**Input:** `"Finish OS lab report tonight"`
**Parsed Output:**
```json
{
  "task": "Finish OS lab report",
  "deadline": "Today 9:00 PM",
  "priority": "Medium",
  "category": "Study"
}
```

### 2. **Smart Date & Time Understanding**
Supports human-like time interpretation:
- `"tomorrow"`, `"tonight"`, `"today"`
- `"next Friday"`, `"this evening"`
- `"in 2 hours"`, `"in 15 minutes"`
- `"end of month"`, `"ASAP"`
- `"every alternate day"`, `"weekdays"`

### 3. **Automatic Priority Detection**
AI infers urgency from language patterns:
- **High**: "URGENT", "ASAP", "immediately", "critical"
- **Medium**: "need to", "should", "tonight", "soon"
- **Low**: "maybe", "someday", "later", "whenever"

Tasks are color-coded: 🔴 High | 🟡 Medium | 🔵 Low

### 4. **Conversational Task Editing**
Modify tasks naturally without touching forms:
- `"Move gym to 7 PM"`
- `"Delete the assignment task"`
- `"Mark all study tasks complete"`
- `"Reschedule meeting to tomorrow"`
- `"Make this high priority"`

### 5. **Desktop Notifications**
- Native system notifications for reminders
- Sound alerts
- Snooze options
- Works even when app is minimized
- Offline-first behavior

### 6. **Intelligent Task Categorization**
AI auto-detects categories:
- **Study** - assignments, projects, exams
- **Fitness** - gym, exercise, workouts
- **Work** - meetings, reports, deadlines
- **Personal** - calls, visits, family
- **Finance** - bills, payments, invoices
- **Shopping** - groceries, purchases
- **Entertainment** - movies, games, reading

### 7. **Minimal Modern UI**
- Clean, distraction-free interface
- Fast and responsive
- Keyboard-friendly
- Inspired by ChatGPT, Notion AI, Things 3
- Instant visual feedback

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Electron/Tauri - Lightweight desktop app
- React 18 - UI library
- Tailwind CSS - Styling
- Axios - HTTP client

**Backend:**
- Python FastAPI - High-performance API
- SQLite - Local database
- SQLAlchemy - ORM

**NLP Engine:**
- spaCy - NLP processing
- dateparser - Date/time parsing
- Duckling/Chrono - Entity extraction
- Custom intent parser

**Notifications:**
- Native OS notifications
- APScheduler - Scheduled reminders

### Project Structure

```
NeuroTask/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── schemas.py           # Pydantic models
│   │   ├── models/              # Database models
│   │   ├── database/            # DB setup
│   │   ├── nlp/                 # NLP engine
│   │   │   ├── intent_parser.py
│   │   │   ├── entity_extractor.py
│   │   │   └── nlp_engine.py
│   │   ├── services/            # Business logic
│   │   │   ├── task_service.py
│   │   │   └── notification_service.py
│   │   └── api/                 # API routes
│   │       ├── tasks.py
│   │       └── notifications.py
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── utils/               # Utilities
│   │   ├── styles/              # Global styles
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── tauri.conf.json
│   ├── package.json
│   └── README.md
│
└── docs/
    ├── ARCHITECTURE.md          # This file
    ├── API.md                   # API documentation
    ├── DEVELOPMENT.md           # Setup guide
    └── NLP.md                   # NLP system details
```

### Data Flow

```
User Input
    ↓
Frontend (TaskInput Component)
    ↓
API Call (POST /api/tasks/create)
    ↓
Backend (FastAPI)
    ↓
NLP Engine
    ├─ Intent Parser → determine action (create, edit, delete, etc.)
    ├─ Entity Extractor → extract dates, priority, category
    └─ Task Structuring → normalize to JSON schema
    ↓
Task Service
    ├─ Create task in database
    ├─ Calculate confidence score
    └─ Schedule reminder if needed
    ↓
Notification Service
    ├─ Store reminder timestamp
    └─ Schedule background job
    ↓
Response sent to Frontend
    ↓
Frontend Updates UI
```

---

## 📊 Database Schema

### Task Model

```python
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "priority": "high|medium|low",
  "category": "string",
  "created_at": "datetime",
  "deadline": "datetime",
  "reminder_time": "datetime",
  "recurrence": "RRULE string",
  "completed": "boolean",
  "completed_at": "datetime",
  "original_text": "string",  # Raw user input
  "confidence_score": "0-100",
  "parsed_data": "json"  # Full parsing result
}
```

### Database
- **Type:** SQLite (local, fast, zero setup)
- **Location:** `backend/neurotask.db`
- **Migrations:** Handled by SQLAlchemy

---

## 🧠 NLP System

### Pipeline

**Step 1: Intent Detection**

Classifies the user's intent:
- `create_task` - Create new task
- `edit_task` - Modify existing task
- `delete_task` - Remove task
- `complete_task` - Mark as done
- `list_tasks` - Show tasks
- `search_tasks` - Find tasks

**Step 2: Entity Extraction**

Extracts structured data:
- **DateTime** - When is it due? (dateparser)
- **Priority** - How urgent? (keyword matching)
- **Category** - What type? (category keywords)
- **Recurrence** - Does it repeat? (pattern matching)
- **Task Name** - What to do? (text cleaning)

**Step 3: Task Structuring**

Normalizes extracted entities into task schema:
- Resolve ambiguous dates
- Set defaults for missing fields
- Calculate confidence score
- Store raw parsing data

**Step 4: Confidence Scoring**

Score ranges 0-100:
- **90-100:** High confidence (clear intent, all fields extracted)
- **70-89:** Good confidence (clear intent, some fields missing)
- **50-69:** Medium confidence (ambiguous but parseable)
- **0-49:** Low confidence (needs clarification)

### Examples

**Example 1:**
```
Input: "Gym every Monday Wednesday Friday at 6 am"
Confidence: 95%

Output:
{
  "task": "Gym",
  "time": "6:00 AM",
  "recurrence": "FREQ=WEEKLY;BYDAY=MO,WE,FR",
  "priority": "low",
  "category": "fitness"
}
```

**Example 2:**
```
Input: "URGENT: submit assignment ASAP"
Confidence: 88%

Output:
{
  "task": "Submit assignment",
  "priority": "high",
  "deadline": null,  # No specific date
  "category": "study"
}
```

**Example 3:**
```
Input: "maybe watch Batman sometime"
Confidence: 72%

Output:
{
  "task": "Watch Batman",
  "priority": "low",
  "category": "entertainment",
  "deadline": null
}
```

---

## 🔔 Notification System

### How It Works

1. **Reminder Creation** - When task is created with deadline/reminder time
2. **Background Scheduler** - Runs every 60 seconds (configurable)
3. **Check Due** - Queries tasks with reminder_time <= now
4. **Send Notification** - Triggers OS notification
5. **Mark Sent** - Update task status (optional)

### Features

- ✅ Native OS notifications (Windows, Mac, Linux)
- ✅ Sound alerts
- ✅ Snooze for 5/15/60 minutes
- ✅ Mark complete directly from notification
- ✅ Persistent reminders for high-priority tasks
- ✅ Works offline
- ✅ Works when app is minimized

---

## 🔮 Future Enhancements

The architecture is designed to scale. Future features planned:

1. **Voice Input** - Say tasks instead of typing
2. **AI Coach** - Personalized productivity suggestions
3. **Smart Scheduling** - AI-suggested optimal task times
4. **Calendar Integration** - Sync with Google Calendar, Outlook
5. **Email Integration** - Create tasks from emails
6. **Semantic Search** - Find tasks by meaning, not keywords
7. **AI-Generated Plans** - Daily schedule recommendations
8. **Habit Tracking** - Build and track habits
9. **Team Collaboration** - Share tasks and lists
10. **Local LLM** - Run Ollama/Llama for offline AI

### Scalability Considerations

- **Modular services** - Each service can scale independently
- **API-first design** - Easy to add new frontends (mobile, web, CLI)
- **Database-agnostic** - Can switch from SQLite to PostgreSQL
- **LLM-ready** - Optional integration with Ollama or cloud APIs
- **Plugin system** - Extend with custom parsers and integrations

---

## 📚 Development

### Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run tauri:dev
```

### Testing

```bash
# Test backend
python -m pytest

# Test frontend
npm test
```

### Building

```bash
# Build backend (package as executable)
pyinstaller backend/run.py

# Build frontend
npm run tauri:build
```

---

## 🎨 Design Philosophy

### Key Principles

1. **Conversational** - Talk to the app naturally
2. **Fast** - Instant feedback and processing
3. **Smart** - AI that actually understands
4. **Minimal** - No unnecessary UI clutter
5. **Offline** - Works without internet
6. **Private** - No data leaves your computer
7. **Extensible** - Easy to add features
8. **Beautiful** - Modern, premium feel

### UI/UX Guidelines

- Dark mode support
- Smooth animations
- Keyboard shortcuts
- Touch-friendly on tablets
- Accessible (WCAG 2.1)
- Responsive design

---

## 📖 API Documentation

See [API.md](./API.md) for detailed endpoint documentation.

### Key Endpoints

```
POST   /api/tasks/parse           # Parse without creating
POST   /api/tasks/create          # Create task
GET    /api/tasks/                # List all
GET    /api/tasks/{id}            # Get specific
PUT    /api/tasks/{id}            # Update
POST   /api/tasks/{id}/complete   # Mark complete
DELETE /api/tasks/{id}            # Delete
GET    /api/tasks/search/query    # Search

GET    /api/notifications/due     # Due reminders
GET    /api/notifications/upcoming # Upcoming reminders
```

---

## 🐛 Debugging

### Backend Logs
```bash
# Run with verbose logging
DEBUG=True python run.py
```

### Frontend Logs
- Open DevTools: `F12` or `Cmd+Option+I`
- Check Network tab for API requests
- Console tab for JavaScript errors

---

## 🚀 Deployment

### Desktop App (Tauri)
```bash
npm run tauri:build
# Creates distributable .exe, .dmg, .deb
```

### Web App
```bash
npm run build
# Creates static files in `dist/`
# Deploy to Vercel, Netlify, etc.
```

### Backend Server
```bash
# Docker
docker build -t neurotask-backend .
docker run -p 8000:8000 neurotask-backend

# Or PyPI package
pip install neurotask
neurotask-server
```

---

## 📝 License

MIT - See LICENSE file

---

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md

---

## 📧 Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@neurotask.dev

---

**Built with ❤️ for productive minds.**

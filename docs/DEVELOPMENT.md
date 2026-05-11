# NeuroTask - Development Setup Guide

Complete guide to set up and develop NeuroTask locally.

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space

### Required Software

#### Node.js & npm
- Download from https://nodejs.org/
- Version 16+ recommended
- Check: `node --version` and `npm --version`

#### Python
- Download from https://python.org/
- Version 3.8+ recommended
- Check: `python --version`

#### Rust (for Tauri/Desktop app)
- Download from https://rustup.rs/
- Installs rustc, cargo, etc.
- Check: `rustc --version`

#### Git
- Download from https://git-scm.com/
- Check: `git --version`

---

## Setup Instructions

### 1. Clone the Repository

```bash
cd "d:\School Work\VIT Chennai\summer projects"
git clone <repository-url> neurotask
cd neurotask
```

Or if you have the files locally, navigate to the project directory.

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (default settings are fine for development)
```

#### Initialize Database

```bash
# The database is automatically created on first run
# Or manually initialize:
python -c "from app.database import init_db; init_db()"
```

#### Start Backend Server

```bash
# Method 1: Run script
python run.py

# Method 2: Run FastAPI directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Keep this terminal running!

---

### 3. Frontend Setup

#### Open New Terminal

```bash
cd frontend
```

#### Install Dependencies

```bash
npm install
```

#### Install Tauri CLI (optional, for desktop app)

```bash
npm install @tauri-apps/cli
```

#### Development Mode - Web Version

```bash
npm run dev
```

Then open http://localhost:5173 in your browser.

#### Development Mode - Desktop App

```bash
npm run tauri:dev
```

This will launch the Tauri desktop application. Changes are auto-reloaded.

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app
│   │   ├── config.py                # Configuration
│   │   ├── schemas.py               # Data models
│   │   ├── models/
│   │   │   └── task.py             # Task model
│   │   ├── database/
│   │   │   └── __init__.py         # Database setup
│   │   ├── nlp/
│   │   │   ├── intent_parser.py    # Intent detection
│   │   │   ├── entity_extractor.py # Entity extraction
│   │   │   └── nlp_engine.py       # Main NLP engine
│   │   ├── services/
│   │   │   ├── task_service.py     # Task operations
│   │   │   └── notification_service.py  # Notifications
│   │   └── api/
│   │       ├── tasks.py            # Task endpoints
│   │       └── notifications.py    # Notification endpoints
│   ├── requirements.txt
│   ├── run.py
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── TaskCard.jsx
│   │   │   ├── TaskInput.jsx
│   │   │   ├── TaskFilters.jsx
│   │   │   ├── TaskList.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── hooks/                  # Custom hooks
│   │   │   ├── useTasks.js
│   │   │   └── useNotifications.js
│   │   ├── utils/                  # Utilities
│   │   │   └── index.js
│   │   ├── styles/                 # Styling
│   │   │   └── global.css
│   │   ├── App.jsx                 # Main component
│   │   └── main.jsx                # Entry point
│   ├── index.html                  # HTML template
│   ├── package.json
│   ├── vite.config.js
│   ├── tauri.conf.json
│   └── README.md
│
├── docs/
│   ├── ARCHITECTURE.md             # System design
│   ├── API.md                      # API documentation
│   ├── DEVELOPMENT.md              # This file
│   └── NLP.md                      # NLP details
│
└── README.md                       # Project overview
```

---

## Common Tasks

### Running Tests

#### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test
pytest tests/test_nlp.py

# With coverage
pytest --cov=app
```

#### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# With coverage
npm test -- --coverage
```

### Building for Production

#### Backend

```bash
cd backend

# Build executable with PyInstaller
pip install pyinstaller
pyinstaller --onefile run.py

# Output: dist/run.exe (or dist/run on macOS/Linux)
```

#### Frontend - Web

```bash
cd frontend

# Build static files
npm run build

# Output: dist/ directory
# Deploy to Vercel, Netlify, etc.
```

#### Frontend - Desktop

```bash
cd frontend

# Build Tauri app
npm run tauri:build

# Output: src-tauri/target/release/
# Creates .exe, .dmg, .deb, etc. depending on OS
```

---

## Debugging

### Backend Debugging

#### Using print statements

```python
# In app/services/task_service.py
print(f"Creating task: {text}")
print(f"Parsed result: {parsed}")
```

#### Using Python debugger

```python
import pdb; pdb.set_trace()
# Then use commands: n, s, c, p <var>, etc.
```

#### Using VS Code debugger

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

Then press F5 to start debugging.

### Frontend Debugging

#### Browser DevTools
- Press F12 or Cmd+Option+I
- Network tab: Check API requests
- Console tab: JavaScript errors
- Sources tab: Set breakpoints

#### VS Code DevTools (for Tauri)
- In development mode, press F12 in the Tauri window
- Same as browser DevTools

---

## Troubleshooting

### Backend Issues

#### Port already in use

```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

#### Database locked

```bash
# Delete the database and restart
rm backend/neurotask.db
python backend/run.py
```

#### Import errors

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall
```

### Frontend Issues

#### Port 5173 already in use

```bash
# Use different port
npm run dev -- --port 5174
```

#### Dependencies not installing

```bash
# Clear npm cache
npm cache clean --force
npm install
```

#### Tauri not found

```bash
# Reinstall Tauri CLI
npm install -g @tauri-apps/cli
```

---

## Environment Variables

### Backend (.env)

```env
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite:///neurotask.db

# NLP
NLP_MODEL=en_core_web_sm
CONFIDENCE_THRESHOLD=0.6

# Timezone
TIMEZONE=UTC

# Notifications
NOTIFICATION_CHECK_INTERVAL=60

# Optional: Local LLM
USE_LOCAL_LLM=False
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### Frontend (.env.local, optional)

```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=NeuroTask
VITE_DEBUG=true
```

---

## Performance Tips

### Backend
- Use SQLite connection pooling for databases
- Cache NLP models in memory
- Implement request rate limiting
- Use async/await for I/O operations

### Frontend
- Lazy load components
- Use React.memo for expensive components
- Implement virtual scrolling for long lists
- Optimize bundle size with code splitting

---

## Code Standards

### Python (Backend)

```python
# Use type hints
def create_task(text: str) -> Task:
    ...

# Use docstrings
def parse(text: str) -> Dict[str, Any]:
    """
    Parse user input.
    
    Args:
        text: User input
        
    Returns:
        Parsed result
    """
    ...

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.info("Task created")
```

### JavaScript (Frontend)

```javascript
// Use modern ES6+ syntax
const useTasks = () => {
  const [tasks, setTasks] = useState([])
  // ...
}

// Use proper component naming
export const TaskCard = ({ task, onComplete }) => {
  // ...
}

// Use comments for complex logic
// Calculate stats from tasks
const stats = calculateStats(tasks)
```

---

## Git Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/task-editing
# Make changes
git add .
git commit -m "Add task editing feature"
git push origin feature/task-editing
```

### Creating a Pull Request

1. Push to feature branch
2. Open GitHub/GitLab
3. Create pull request
4. Request reviews
5. Merge after approval

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tauri Docs**: https://tauri.app/
- **Tailwind CSS**: https://tailwindcss.com/
- **spaCy**: https://spacy.io/

---

## Getting Help

- Check existing issues: https://github.com/your-repo/issues
- Create a new issue with detailed description
- Join community Discord/Slack
- Email: support@neurotask.dev

---

## Next Steps

1. Complete this setup
2. Run backend: `cd backend && python run.py`
3. Run frontend: `cd frontend && npm run dev`
4. Visit http://localhost:5173
5. Create your first task!
6. Check docs/ARCHITECTURE.md for system design

Happy coding! 🚀

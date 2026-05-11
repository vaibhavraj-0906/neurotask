# NeuroTask - Quick Start Guide

Get NeuroTask up and running in **5 minutes**.

## Prerequisites

- Node.js 16+ (https://nodejs.org/)
- Python 3.8+ (https://python.org/)
- 2GB free disk space

## Step 1: Clone/Download Project

```bash
cd "d:\School Work\VIT Chennai\summer projects\to-do list (NLP)"
```

Project files are already here!

## Step 2: Start Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python run.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Backend is ready at http://localhost:8000

## Step 3: Start Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Expected output:**
```
VITE v5.0.0  ready in 123 ms

➜  Local:   http://localhost:5173/
```

✅ Frontend is ready at http://localhost:5173

## Step 4: Open the App

Open your browser and go to: **http://localhost:5173**

You should see the NeuroTask interface!

## Step 5: Create Your First Task

In the text input, type:

```
"Gym tomorrow at 6 am"
```

Then press Enter or click "Add Task"

**Expected result:**
- ✅ Task created: "Gym"
- 📅 Tomorrow at 6:00 AM
- 🏷️ Category: Fitness
- 🎯 Priority: Low

## 🎮 Try More Examples

```
"Finish assignment today"
→ Creates task for today, Study category

"Call mom in 2 hours"
→ Creates task in 2 hours, Personal category

"Pay bill by Friday"
→ Creates task for Friday, Finance category

"Study every weekday"
→ Creates recurring task Mon-Fri, Study category

"URGENT: Complete project ASAP"
→ Creates task with HIGH priority
```

## 📚 Available Features

### View Tasks
- ✅ All tasks listed below
- ✅ Color-coded by priority
- 🔴 Red = High priority
- 🟡 Yellow = Medium priority
- 🔵 Blue = Low priority

### Filter Tasks
- Filter by priority (High/Medium/Low)
- Filter by category (Study, Fitness, Work, etc.)
- Filter by status (Active/Completed)

### Manage Tasks
- ✏️ Edit task (click pencil icon)
- ✅ Mark complete (click checkbox)
- 🗑️ Delete task (click trash icon)

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Kill process on port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Backend not responding

**Error:** `Cannot connect to http://localhost:8000`

**Solution:**
- Make sure backend terminal shows "running on http://127.0.0.1:8000"
- Check you're in the `backend/` directory
- Check Python is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend not loading

**Error:** `Cannot reach http://localhost:5173`

**Solution:**
- Make sure frontend terminal shows "Local: http://localhost:5173"
- Check you're in the `frontend/` directory
- Check Node.js is installed: `node --version`
- Reinstall dependencies: `npm install`

## 📖 Next Steps

1. **Explore the interface** - Create a few tasks
2. **Try different inputs** - See how the AI understands natural language
3. **Read the docs** - Check [docs/](../docs/) for detailed information
4. **Customize** - Edit colors, add categories, extend functionality

## 🔗 Important Links

- **API Docs**: http://localhost:8000/docs (when backend is running)
- **Swagger UI**: http://localhost:8000/swagger
- **Architecture**: See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)
- **API Reference**: See [docs/API.md](../docs/API.md)
- **NLP Guide**: See [docs/NLP.md](../docs/NLP.md)

## 🎯 Common Commands

### Frontend Development
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run tauri:dev    # Run as desktop app (requires Rust)
```

### Backend Development
```bash
python run.py                                    # Run server
python -m pytest                                 # Run tests
DEBUG=True python run.py                         # Run with verbose logging
```

## 💡 Pro Tips

1. **Keyboard shortcut**: Press Enter to submit task
2. **Shift+Enter**: Multiline input
3. **Search**: Use filters at the top
4. **Preview before creating**: Post to `/api/tasks/parse` endpoint

## 🎨 Customization

### Change theme
Edit `frontend/src/styles/global.css`

### Change API URL
Edit `frontend/src/hooks/useTasks.js`:
```javascript
const API_BASE_URL = 'http://your-server:8000/api'
```

### Change database
Edit `backend/app/config.py`:
```python
DATABASE_URL = "sqlite:////path/to/your/db.db"
```

## 📞 Need Help?

1. Check troubleshooting above
2. Read docs in [docs/](../docs/) folder
3. Check GitHub issues
4. Email support@neurotask.dev

## ✨ What's Next?

- Build the desktop app with Tauri
- Add voice input
- Integrate with calendar
- Add team collaboration

---

**Enjoy using NeuroTask! 🚀**

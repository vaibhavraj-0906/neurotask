# NeuroTask - AI-Powered NLP To-Do List Application

> **"Type naturally. The AI understands everything."**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Node.js](https://img.shields.io/badge/node.js-16+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

NeuroTask is a **modern, intelligent desktop productivity application** that lets users create, edit, and manage tasks using **natural language** instead of traditional forms.

## 🎯 The Problem

Traditional task managers are **slow and cumbersome**:
- Click here, fill that field, select a date, add a priority
- 5+ interactions for a simple task
- No understanding of natural language
- Clunky and unintuitive

## ✨ The Solution

**Type naturally. The AI understands everything.**

```
User: "Gym every Monday Wednesday Friday at 6 am"
AI:   ✅ Task created: "Gym"
      📅 Repeats: Mon, Wed, Fri at 6:00 AM
      🎯 Priority: Low
      🏷️  Category: Fitness
```

## 🚀 Features

✅ **Natural Language Input** - Create tasks by typing conversationally
✅ **Smart Date/Time Parsing** - Understands "tomorrow", "in 2 hours", "end of month"
✅ **Auto Priority Detection** - Infers urgency from keywords (URGENT, ASAP, maybe)
✅ **Intelligent Categorization** - Auto-detects: Study, Fitness, Work, Personal, Finance, Shopping, Entertainment
✅ **Conversational Editing** - "Move gym to 7 PM" instead of clicking around
✅ **Desktop Notifications** - Native system notifications with snooze options
✅ **Recurring Tasks** - "Every weekday", "every other Monday", custom patterns
✅ **Minimal Modern UI** - Clean, fast, distraction-free design
✅ **Offline-First** - Works without internet
✅ **Privacy** - All data stays on your machine

## 📸 Screenshots

[Placeholder for screenshots]

## 🏗️ Technology Stack

### Frontend
- **Tauri** - Lightweight desktop app framework
- **React 18** - Modern UI library
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client

### Backend
- **Python FastAPI** - High-performance API
- **SQLite** - Local database
- **SQLAlchemy** - ORM
- **APScheduler** - Task scheduling

### NLP Engine
- **spaCy** - NLP processing
- **dateparser** - Intelligent date parsing
- **Custom Intent Parser** - Action detection
- **Entity Extraction** - Structured data extraction

## 🎮 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- 2GB free disk space

### Installation

1. **Clone repository**
```bash
git clone https://github.com/yourusername/neurotask.git
cd neurotask
```

2. **Set up backend**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend runs at http://localhost:8000

3. **Set up frontend** (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

4. **Open in browser**
Visit http://localhost:5173 and start creating tasks!

### Creating Tasks

Try these examples:

```
"Finish OS lab report tonight"
"Gym every Monday Wednesday Friday at 6 am"
"Call mom in 2 hours"
"Pay electricity bill before Friday"
"Team meeting next Monday at 10 AM"
"URGENT: Submit DSA assignment ASAP"
"Maybe watch Batman later"
```

## 📖 Documentation

- **[Quick Start Guide](./QUICKSTART.md)** - Get started in 5 minutes
- **[Architecture](./docs/ARCHITECTURE.md)** - System design and components
- **[API Reference](./docs/API.md)** - Complete API documentation
- **[Development Setup](./docs/DEVELOPMENT.md)** - Development guide
- **[NLP System](./docs/NLP.md)** - How the AI works

## 🔧 Project Structure

```
NeuroTask/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── nlp/               # NLP engine
│   │   ├── services/          # Business logic
│   │   ├── api/               # API routes
│   │   ├── models/            # Database models
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── run.py
│
├── frontend/                   # Tauri + React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── utils/             # Utilities
│   │   └── App.jsx
│   ├── index.html
│   └── package.json
│
└── docs/                       # Documentation
    ├── ARCHITECTURE.md
    ├── API.md
    ├── DEVELOPMENT.md
    └── NLP.md
```

## 📊 Examples

### Example 1: Study Task
```
Input:  "Finish OS lab report tonight"
Output: 
{
  "title": "Finish OS lab report",
  "deadline": "Today 9:00 PM",
  "priority": "medium",
  "category": "study",
  "confidence": 88%
}
```

### Example 2: Recurring Fitness
```
Input:  "Gym every Monday Wednesday Friday at 6 am"
Output:
{
  "title": "Gym",
  "time": "6:00 AM",
  "recurrence": "FREQ=WEEKLY;BYDAY=MO,WE,FR",
  "priority": "low",
  "category": "fitness",
  "confidence": 95%
}
```

### Example 3: Financial Task
```
Input:  "Pay electricity bill before Friday"
Output:
{
  "title": "Pay electricity bill",
  "deadline": "Friday 11:59 PM",
  "priority": "medium",
  "category": "finance",
  "confidence": 92%
}
```

## 🧠 How the AI Works

The NLP engine processes your input in 4 steps:

1. **Intent Detection** - What do you want? (create, edit, delete, etc.)
2. **Entity Extraction** - Extract dates, priorities, categories
3. **Task Structuring** - Normalize into task schema
4. **Confidence Scoring** - How confident in the parsing? (0-100%)

Learn more in [NLP.md](./docs/NLP.md)

## 🔌 API Endpoints

### Create Task
```bash
POST /api/tasks/create
Body: { "text": "Finish assignment tomorrow" }
```

### List Tasks
```bash
GET /api/tasks/?priority=high&completed=false
```

### Parse Without Creating
```bash
POST /api/tasks/parse
Body: { "text": "Gym on Monday" }
```

See [API.md](./docs/API.md) for complete reference

## 🎨 Design Philosophy

- **Conversational** - Talk to your task manager
- **Fast** - Instant feedback
- **Smart** - AI that understands
- **Minimal** - No unnecessary complexity
- **Beautiful** - Premium design
- **Private** - Your data, your machine

## 🚦 Status

- ✅ Core NLP engine
- ✅ Task management API
- ✅ Notification system
- ✅ React frontend
- ✅ Task filtering & search
- 🔄 Desktop app (Tauri) - In progress
- 🔄 Advanced scheduling - In progress
- ⏳ Voice input - Planned
- ⏳ Team collaboration - Planned
- ⏳ Mobile app - Planned

## 🐛 Known Issues

- Date ambiguity: "Friday" could be this or next week
- No conversation history
- Single timezone support (UTC)
- No multi-user support yet

See [Issues](https://github.com/yourusername/neurotask/issues) for more

## 🗺️ Roadmap

### v1.1 (Q2 2024)
- Fuzzy matching for task names
- Better date ambiguity resolution
- Confidence feedback in UI

### v1.2 (Q3 2024)
- Conversation context
- Email integration
- Calendar sync

### v2.0 (Q4 2024)
- Local LLM support (Ollama)
- Voice input
- Mobile app
- Team collaboration

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md)

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See [LICENSE](./LICENSE) file

## 💬 Support

- **Documentation**: Check [docs/](./docs/) folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/neurotask/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/neurotask/discussions)
- **Email**: support@neurotask.dev

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Designed for [React](https://react.dev/)
- Packaged with [Tauri](https://tauri.app/)
- NLP powered by [spaCy](https://spacy.io/)

## 📜 Citation

If you use NeuroTask in your research or project, please cite:

```bibtex
@software{neurotask2024,
  title={NeuroTask: AI-Powered NLP To-Do List Application},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/neurotask}
}
```

---

**Built with ❤️ for productive minds.**

[⬆ Back to top](#neurotask---ai-powered-nlp-to-do-list-application)

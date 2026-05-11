# NeuroTask Frontend

Modern, AI-powered task management application built with React and Tauri.

## Stack

- **Tauri** - Lightweight desktop app framework
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Zustand** - State management (optional, using hooks for now)

## Setup

### Prerequisites
- Node.js 16+
- Rust (for Tauri)

### Installation

```bash
# Install dependencies
npm install

# Install Tauri CLI
npm install @tauri-apps/cli

# Or use Tauri globally
cargo install tauri-cli
```

### Development

```bash
# Run in development mode
npm run tauri:dev

# Or run Vite dev server separately
npm run dev
```

### Build

```bash
# Build desktop application
npm run tauri:build

# Build web version
npm run build
```

## Project Structure

```
src/
  ├── components/       # React components
  │   ├── TaskCard.jsx
  │   ├── TaskInput.jsx
  │   ├── TaskFilters.jsx
  │   ├── TaskList.jsx
  │   ├── Header.jsx
  │   └── Sidebar.jsx
  ├── hooks/            # Custom React hooks
  │   ├── useTasks.js
  │   └── useNotifications.js
  ├── pages/            # Page components (future)
  ├── utils/            # Utility functions
  ├── styles/           # Global styles
  ├── App.jsx           # Main app component
  └── main.jsx          # Entry point
```

## Features

- **Natural Language Input** - Create tasks by typing naturally
- **Smart Parsing** - AI understands dates, priorities, and categories
- **Real-time Updates** - Instant feedback and updates
- **Filtering** - Filter by priority, category, and status
- **Notifications** - Desktop notifications for reminders
- **Responsive Design** - Works on different screen sizes

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api`

Make sure the backend is running before starting the frontend development server.

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

## Deployment

1. **Development**: Run `npm run tauri:dev`
2. **Build**: Run `npm run tauri:build` to create distributable binary
3. **Distribution**: The built app will be in `src-tauri/target/release/`

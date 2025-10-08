# Learning Center Integration Guide

## Overview

This document explains how to integrate the Learning Center components (Phase 1) into your application. Phase 1 includes:

1. **Backend API Endpoints** for file browsing, help content, and log streaming
2. **ContextPanel** - Right sidebar with step-specific help
3. **LiveLogViewer** - Bottom drawer with real-time log streaming
4. **FileSystemBrowser** - File tree browser for pydantic_library

---

## Backend Components

### 1. Learning Center Router

**File:** `demo-app/backend/app/routers/learning_center.py`

**Endpoints:**
- `GET /api/learning-center/files/browse?path=/` - Browse directory structure
- `GET /api/learning-center/files/read?path=<file>` - Read file contents
- `GET /api/learning-center/help/step/{step_number}` - Get help for step (1-6)
- `GET /api/learning-center/help/all` - Get help for all steps
- `WS /api/learning-center/logs/stream` - WebSocket for real-time logs
- `POST /api/learning-center/logs/clear` - Clear log buffer
- `GET /api/learning-center/logs/count` - Get log count and connections
- `GET /api/learning-center/health` - Health check

**Log Streaming Infrastructure:**
- `LogBroadcaster` class manages WebSocket connections and log buffering
- `WebSocketLogHandler` captures logs from Python's logging system
- Logs are automatically broadcast to all connected WebSocket clients
- Supports buffering up to 1000 log entries (configurable)
- Auto-reconnection on client disconnect

---

## Frontend Components

### 1. ContextPanel Component

**File:** `demo-app/frontend/components/learning-center/ContextPanel.tsx`

**Props:**
```typescript
interface ContextPanelProps {
  currentStep: number      // Current workflow step (1-6)
  onFileClick?: (filePath: string) => void  // Optional callback for file clicks
}
```

**Features:**
- Collapsible right sidebar (fixed position)
- Fetches help content from `/api/learning-center/help/step/{step_number}`
- Displays step name, description, files used, libraries, and tips
- Auto-updates when step changes
- Error handling with user-friendly messages

**Usage Example:**
```tsx
import ContextPanel from '@/components/learning-center/ContextPanel'

export default function WorkflowPage() {
  const { currentStep } = useWorkflowStore()

  return (
    <div className="relative">
      {/* Main content */}
      <div className="pr-96"> {/* Add right padding for panel */}
        <YourWorkflowComponent />
      </div>

      {/* Context Panel */}
      <ContextPanel
        currentStep={currentStep}
        onFileClick={(path) => console.log('File clicked:', path)}
      />
    </div>
  )
}
```

---

### 2. LiveLogViewer Component

**File:** `demo-app/frontend/components/learning-center/LiveLogViewer.tsx`

**Props:**
```typescript
interface LiveLogViewerProps {
  maxHeight?: string          // Max height when expanded (default: '400px')
  initialExpanded?: boolean   // Initial expanded state (default: false)
}
```

**Features:**
- Bottom drawer (fixed position) with real-time WebSocket log streaming
- Connects to `ws://localhost:8000/api/learning-center/logs/stream`
- Filters by level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Filters by step (1-6)
- Search functionality (searches message, module, function)
- Download logs as text file
- Clear logs button
- Auto-reconnection on disconnect
- Color-coded log levels

**Usage Example:**
```tsx
import LiveLogViewer from '@/components/learning-center/LiveLogViewer'

export default function AppLayout({ children }) {
  return (
    <div className="min-h-screen">
      {/* Your app content */}
      {children}

      {/* Live Log Viewer */}
      <LiveLogViewer
        maxHeight="400px"
        initialExpanded={false}
      />
    </div>
  )
}
```

**Log Entry Format:**
```typescript
interface LogEntry {
  timestamp: string          // ISO 8601 timestamp
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'
  logger: string            // Logger name (e.g., 'app.routers.research')
  message: string           // Log message
  module: string            // Module name
  function: string          // Function name
  line: number             // Line number
  step?: number            // Optional step number (1-6)
}
```

---

### 3. FileSystemBrowser Component

**File:** `demo-app/frontend/components/learning-center/FileSystemBrowser.tsx`

**Props:**
```typescript
interface FileSystemBrowserProps {
  initialPath?: string  // Initial path to browse (default: '/')
}
```

**Features:**
- Tree view of pydantic_library directory
- Click to expand directories
- Click files to view contents in modal dialog
- Syntax highlighting metadata (language detection)
- Download file button
- File size display
- Icon indicators for file types (Python, YAML, JSON, Markdown)

**Usage Example:**
```tsx
import FileSystemBrowser from '@/components/learning-center/FileSystemBrowser'

export default function HelpPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Browse Generated Files</h1>
      <FileSystemBrowser initialPath="/" />
    </div>
  )
}
```

---

## Integration Steps

### Step 1: Add to Main Layout

Integrate LiveLogViewer into your root layout:

**File:** `demo-app/frontend/app/layout.tsx`

```tsx
import LiveLogViewer from '@/components/learning-center/LiveLogViewer'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <LiveLogViewer maxHeight="400px" initialExpanded={false} />
      </body>
    </html>
  )
}
```

### Step 2: Add to Workflow Page

Integrate ContextPanel into your workflow page:

**File:** `demo-app/frontend/app/page.tsx` or `demo-app/frontend/app/workflow/page.tsx`

```tsx
import ContextPanel from '@/components/learning-center/ContextPanel'
import { useWorkflowStore } from '@/lib/workflow-store'

export default function WorkflowPage() {
  const { currentStep } = useWorkflowStore()

  return (
    <div className="relative min-h-screen">
      {/* Main workflow content with padding for panel */}
      <div className="pr-96">
        <WorkflowSteps />
      </div>

      {/* Context Panel */}
      <ContextPanel currentStep={currentStep} />
    </div>
  )
}
```

### Step 3: Add to Help/Docs Page (Optional)

Add FileSystemBrowser to a help or documentation page:

**File:** `demo-app/frontend/app/help/page.tsx` (create if doesn't exist)

```tsx
import FileSystemBrowser from '@/components/learning-center/FileSystemBrowser'

export default function HelpPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Documentation</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <FileSystemBrowser initialPath="/" />
        {/* Other help content */}
      </div>
    </div>
  )
}
```

---

## Backend Configuration

### Log Handler Installation

The WebSocket log handler is automatically installed when the Learning Center router is imported.

**Location:** `demo-app/backend/app/routers/learning_center.py` (lines 135-142)

```python
# Install WebSocket log handler
ws_log_handler = WebSocketLogHandler(log_broadcaster)
ws_log_handler.setLevel(logging.INFO)
ws_log_handler.setFormatter(logging.Formatter('%(message)s'))

# Add handler to root logger so we capture all logs
root_logger = logging.getLogger()
root_logger.addHandler(ws_log_handler)
```

**Configuration Options:**
- Change log level: `ws_log_handler.setLevel(logging.DEBUG)` to capture DEBUG logs
- Change buffer size: `log_broadcaster.max_buffer_size = 2000`

---

## Step Number Detection

The log handler attempts to detect step numbers from:
1. Logger name (e.g., `app.routers.step2_research`)
2. Log message (e.g., "Starting Step 2: Ontology Research")

**Recommendations for Step Detection:**
- Name loggers with step numbers: `logger = logging.getLogger(__name__ + '.step2')`
- Include step number in log messages: `logger.info("Step 2: Starting ontology research")`

**Example:**
```python
# In your step router
logger = logging.getLogger(__name__)
logger.info("Step 2: Starting ontology research")  # Will be tagged with step=2
```

---

## Security Considerations

### File Browsing Security

The file browsing endpoints include security checks:

```python
# Path sanitization
clean_path = path.lstrip("/").lstrip("\\")
target_path = pydantic_library_path / clean_path

# Security check - prevent path traversal
target_path = target_path.resolve()
if not str(target_path).startswith(str(pydantic_library_path.resolve())):
    raise HTTPException(status_code=403, detail="Access denied: Path escapes pydantic_library")
```

**This prevents:**
- Path traversal attacks (`../../etc/passwd`)
- Accessing files outside `pydantic_library`
- Directory escaping via symlinks

---

## Styling and Theming

All components use shadcn/ui components with Tailwind CSS classes. They automatically adapt to:
- Light/dark themes (using `dark:` variants)
- Responsive layouts (using breakpoint classes)
- Custom color schemes (via CSS variables)

**To customize colors:**

Edit `demo-app/frontend/app/globals.css`:

```css
:root {
  --primary: 210 100% 50%;  /* Customize primary color */
  --accent: 180 100% 50%;   /* Customize accent color */
}
```

---

## Troubleshooting

### WebSocket Connection Issues

**Problem:** LiveLogViewer shows "Disconnected"

**Solutions:**
1. Check backend is running on port 8000
2. Check CORS settings in `demo-app/backend/app/main.py`:
   ```python
   cors_origins: str = "http://localhost:3000,http://localhost:3001"
   ```
3. Check browser console for WebSocket errors
4. Verify WebSocket endpoint: `ws://localhost:8000/api/learning-center/logs/stream`

### File Browsing 403 Errors

**Problem:** "Access denied: Path escapes pydantic_library"

**Solutions:**
1. Verify `pydantic_library_path` setting in `.env`:
   ```
   PYDANTIC_LIBRARY_PATH=../pydantic_library
   ```
2. Check that path is relative to backend directory
3. Ensure pydantic_library directory exists

### ContextPanel Not Loading Help

**Problem:** "Failed to fetch help content"

**Solutions:**
1. Verify backend endpoint: `http://localhost:8000/api/learning-center/help/step/1`
2. Check that `currentStep` is 1-6 (not 0 or >6)
3. Check browser console for fetch errors
4. Verify CORS settings

---

## Performance Considerations

### Log Buffer Size

Default buffer size: 1000 entries

**To increase:**
```python
# In learning_center.py
log_broadcaster = LogBroadcaster()
log_broadcaster.max_buffer_size = 5000  # Increase to 5000
```

**Memory usage:** ~1KB per log entry = 5MB for 5000 entries

### WebSocket Connections

Each connected client maintains a WebSocket connection. The `LogBroadcaster` tracks all active connections and cleans up disconnected clients automatically.

**Max recommended connections:** 50-100 (for small apps)

---

## Next Steps (Phase 2)

Phase 2 will add:
1. Inline tooltips for technical terms
2. Per-step context panels (integrated into each Step component)
3. Code snippet viewer with syntax highlighting
4. Error troubleshooting guides

See `docs/LEARNING_CENTER_DESIGN.md` for full roadmap.

---

## API Reference

### Backend Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/learning-center/files/browse` | Browse directory structure |
| GET | `/api/learning-center/files/read` | Read file contents |
| GET | `/api/learning-center/help/step/{num}` | Get step help |
| GET | `/api/learning-center/help/all` | Get all step help |
| WS | `/api/learning-center/logs/stream` | WebSocket log stream |
| POST | `/api/learning-center/logs/clear` | Clear log buffer |
| GET | `/api/learning-center/logs/count` | Get log statistics |
| GET | `/api/learning-center/health` | Health check |

### Frontend Components

| Component | Location | Purpose |
|-----------|----------|---------|
| ContextPanel | `components/learning-center/ContextPanel.tsx` | Step-specific help sidebar |
| LiveLogViewer | `components/learning-center/LiveLogViewer.tsx` | Real-time log streaming drawer |
| FileSystemBrowser | `components/learning-center/FileSystemBrowser.tsx` | File tree browser with viewer |

---

## Example: Full Integration

**Backend:** `demo-app/backend/app/main.py`

```python
from app.routers import learning_center

app.include_router(learning_center.router, prefix="/api/learning-center", tags=["Learning Center"])
```

**Frontend:** `demo-app/frontend/app/page.tsx`

```tsx
'use client'

import { useWorkflowStore } from '@/lib/workflow-store'
import ContextPanel from '@/components/learning-center/ContextPanel'
import LiveLogViewer from '@/components/learning-center/LiveLogViewer'
import WorkflowSteps from '@/components/workflow/WorkflowSteps'

export default function Home() {
  const { currentStep } = useWorkflowStore()

  return (
    <div className="relative min-h-screen">
      {/* Main content with padding for context panel */}
      <div className="container mx-auto p-6 pr-96">
        <h1 className="text-3xl font-bold mb-6">Pydantic Model Generator</h1>
        <WorkflowSteps />
      </div>

      {/* Learning Center Components */}
      <ContextPanel
        currentStep={currentStep}
        onFileClick={(path) => console.log('View file:', path)}
      />
      <LiveLogViewer maxHeight="400px" initialExpanded={false} />
    </div>
  )
}
```

---

## Testing

### Test WebSocket Connection

```bash
# Using wscat (npm install -g wscat)
wscat -c ws://localhost:8000/api/learning-center/logs/stream
```

### Test File Browsing

```bash
curl "http://localhost:8000/api/learning-center/files/browse?path=/"
```

### Test Help Content

```bash
curl "http://localhost:8000/api/learning-center/help/step/1"
```

---

## Support

For issues or questions:
1. Check backend logs: `demo-app/backend/logs/`
2. Check browser console for JavaScript errors
3. Verify all environment variables in `.env`
4. Test API endpoints directly with curl
5. Check WebSocket connection with browser DevTools (Network tab)

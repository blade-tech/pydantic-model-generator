# Learning Center Design: Self-Documenting Application

## Philosophy: The App IS the Learning Center

Rather than a separate documentation section, every page of the working application should teach developers how it works through **contextual, progressive disclosure**.

---

## Core Design Principles

### 1. **Context-Aware Help Panels**
- Right sidebar with content that changes based on current step
- Shows relevant files, logs, and examples for CURRENT step only
- Always accessible but not intrusive

### 2. **Progressive Disclosure**
```
Default View: Clean, focused on the task
    ↓ User clicks "Show Details"
Expanded View: Files being used, logs, technical context
    ↓ User clicks "View Code"
Code View: Actual source code with syntax highlighting
```

### 3. **Live Feedback Loop**
- As actions happen, show what's happening behind the scenes
- Real-time log streaming (filtered to relevant step)
- File system changes (what was created/modified)
- API calls being made (with request/response)

### 4. **Inline Documentation**
- Tooltips on technical terms
- "What is this?" icons next to complex concepts
- Expandable code snippets showing examples

---

## Per-Step Enhancement Pattern

Each workflow step (1-6) should have:

### **Main Content Area** (Left, 70%)
- The actual workflow UI (unchanged)
- Clean, focused on the task

### **Context Panel** (Right, 30%, Collapsible)

```
┌─────────────────────────────────────────┐
│ 📖 What's Happening                     │
│ ─────────────────────────────────────── │
│ Brief 2-3 line explanation              │
│                                          │
│ 📁 Files Being Used                     │
│ ─────────────────────────────────────── │
│ [Expandable]                            │
│ • Read: backend/app/services/X.py       │
│ • Write: pydantic_library/schemas/...   │
│                                          │
│ 📦 Libraries                            │
│ ─────────────────────────────────────── │
│ • Anthropic Claude API (streaming)      │
│ • FastAPI (REST endpoints)              │
│                                          │
│ 📜 Live Logs                            │
│ ─────────────────────────────────────── │
│ [Auto-scrolling, filtered]              │
│ INFO: Starting research...              │
│ INFO: Claude API called...              │
│                                          │
│ 🔗 Deep Dive                            │
│ ─────────────────────────────────────── │
│ • View Source Code                      │
│ • View Full Logs                        │
│ • View API Docs                         │
└─────────────────────────────────────────┘
```

---

## Specific Enhancements by Step

### **Step 1: Business Outcome Input**

**Context Panel Shows:**
- ✅ Example inputs (collapsible)
- ✅ What happens when you click "Research"
- ✅ Files that will be created
- 📝 Best practices for outcome descriptions

**Enhancement Ideas:**
- Textarea with smart examples dropdown
- "Load Example" buttons for common use cases
- Character counter with guidance

---

### **Step 2: Ontology Research**

**Context Panel Shows:**
- 🔄 Live Claude API streaming status
- 📚 Which ontologies are being searched (DoCO, FaBiO, PROV-O, FIBO, SKOS)
- 📁 Backend file: `app/routers/research.py`
- 📜 Filtered logs (only Step 2 logs)

**Enhancement Ideas:**
- Show Claude's reasoning in real-time
- Highlight matched entities as they're found
- Link to ontology documentation

**Inline Documentation:**
```tsx
<Tooltip content="Document Components Ontology - standard for academic documents">
  <span className="underline decoration-dotted">DoCO</span>
</Tooltip>
```

---

### **Step 3: OutcomeSpec Generation**

**Context Panel Shows:**
- 📝 What is an OutcomeSpec? (expandable explanation)
- 📁 File being created: `schemas/overlays/{name}_outcomespec.yaml`
- 🔧 Libraries: PyYAML, Pydantic
- 📜 Generation logs

**Enhancement Ideas:**
- Side-by-side: Generated YAML + Visual tree view
- Highlight key sections (outcome_questions, validation_queries)
- "Edit YAML" button for advanced users

---

### **Step 4: LinkML Schema Generation**

**Context Panel Shows:**
- 📝 What is LinkML? (expandable)
- 📁 File being created: `pydantic_library/schemas/overlays/{name}_overlay.yaml`
- 🔧 Claude prompt being used (viewable)
- ⚠️ Common errors + solutions
- 📜 Generation logs

**Enhancement Ideas:**
- Show the prompt being sent to Claude (collapsible)
- Highlight slot definitions in generated YAML
- Validate as you type (if manual edit mode)
- "Validate Schema" button (runs gen-pydantic --validate)

**Critical Documentation:**
```
💡 Key Concept: Slot Definitions
Every slot referenced in a class's `slots:` list MUST be
defined in the top-level `slots:` section.

Example:
  classes:
    MyClass:
      slots:
        - my_field    # ← Must exist below!

  slots:
    my_field:         # ← Definition here
      range: string
```

---

### **Step 5: Pydantic Model Generation**

**Context Panel Shows:**
- 🔧 Command being run: `gen-pydantic {schema_file}`
- 📁 Files:
  - Input: `schemas/overlays/{name}_overlay.yaml`
  - Output: `generated/pydantic/overlays/{name}_models.py`
- 📜 Subprocess stdout/stderr (live streaming)
- ⚠️ Error troubleshooting (if gen-pydantic fails)

**Enhancement Ideas:**
- **Show generated Python code** in a collapsible panel
- Syntax highlighting for Python
- Line numbers
- "Copy to Clipboard" button
- "Download File" button
- **Diff viewer** if regenerating existing overlay

**Error Display Enhancement:**
```tsx
{stderr && (
  <Alert variant="destructive">
    <AlertCircle className="h-4 w-4" />
    <AlertTitle>gen-pydantic Error</AlertTitle>
    <AlertDescription>
      <pre className="text-xs">{stderr}</pre>

      {/* Contextual help based on error type */}
      {stderr.includes("No such slot") && (
        <div className="mt-2 p-2 bg-blue-50 rounded">
          <p className="font-semibold">Common Fix:</p>
          <p>This error means a slot is referenced in a class but not defined
          in the `slots:` section. Go back to Step 4 and regenerate.</p>
          <Button onClick={goToStep4}>← Go to Step 4</Button>
        </div>
      )}
    </AlertDescription>
  </Alert>
)}
```

---

### **Step 6: Testing & Validation**

**Context Panel Shows:**
- 🧪 What tests are being run
- 📁 Files:
  - Test file: `tests/test_{name}.py`
  - Models: `generated/pydantic/overlays/{name}_models.py`
- 📜 Pytest output (live streaming)
- ✅ Test results breakdown

**Enhancement Ideas:**
- **Visual test results** (pass/fail counts with icons)
- Expandable test details (each test's assertions)
- "View Test File" button
- "Re-run Failed Tests" button
- Code coverage visualization

---

## Global Navigation Enhancement

### **Top Bar Addition:**
```
┌────────────────────────────────────────────────────────────┐
│ Pydantic Generator   [Step 1][Step 2]...[Step 6]   [📚 Help]│
└────────────────────────────────────────────────────────────┘
                                                         ↑
                                                   Always visible
                                                   Opens help sidebar
```

### **Help Sidebar (Global, Toggleable):**
- Quick reference for current step
- Keyboard shortcuts
- API documentation links
- Troubleshooting guide
- File system browser

---

## File System Browser Component

**Location:** Help sidebar, always accessible

**Features:**
```
📁 pydantic_library/
  ├─ 📁 schemas/
  │  └─ 📁 overlays/
  │     ├─ 📄 business_contra_overlay.yaml [View] [Download]
  │     └─ 📄 customer_support_overlay.yaml [View] [Download]
  │
  ├─ 📁 generated/
  │  └─ 📁 pydantic/
  │     └─ 📁 overlays/
  │        ├─ 🐍 business_contra_models.py [View] [Download]
  │        └─ 🐍 customer_support_models.py [View] [Download]
  │
  └─ 📁 tests/
     ├─ 🧪 test_business_contra.py [View] [Run]
     └─ 🧪 test_customer_support.py [View] [Run]
```

**Interactions:**
- Click [View] → Opens modal with syntax-highlighted code
- Click [Download] → Downloads file
- Click [Run] → Runs tests (for test files)
- Right-click file → "Copy Path", "Show in Workflow"

---

## Live Log Viewer Component

**Location:** Bottom drawer, always accessible

**Features:**
- 🔴 Real-time log streaming via WebSocket
- 🎯 Filter by step (Step 1-6)
- 🎨 Color-coded by level (INFO=blue, ERROR=red, DEBUG=gray)
- 🔍 Search logs
- 📋 Copy logs
- 💾 Download logs

**UI:**
```
┌─────────────────────────────────────────────────────────────┐
│ 📜 Live Logs  [Filter: All ▼] [Search...] [Clear] [Download]│
├─────────────────────────────────────────────────────────────┤
│ 12:30:45 [INFO] Starting ontology research...               │
│ 12:30:46 [INFO] Claude API called (model: claude-sonnet-4)  │
│ 12:30:48 [ERROR] gen-pydantic failed: ValueError...         │
│          ↳ [Show Context] [Copy] [Troubleshoot]             │
└─────────────────────────────────────────────────────────────┘
```

---

## Inline Tooltips & Explanations

**Pattern:**
```tsx
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger asChild>
      <span className="underline decoration-dotted cursor-help">
        ProvenanceFields mixin
      </span>
    </TooltipTrigger>
    <TooltipContent className="max-w-sm">
      <p>A LinkML mixin that automatically adds tracking fields:</p>
      <ul className="list-disc ml-4 mt-1">
        <li><code>created_at</code>: When entity was created</li>
        <li><code>created_by</code>: Who created it</li>
        <li><code>source_uri</code>: Where data came from</li>
      </ul>
      <a href="/docs/provenance" className="text-blue-500 mt-2 inline-block">
        Learn more →
      </a>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

**Use tooltips for:**
- Technical terms (LinkML, gen-pydantic, OutcomeSpec)
- Library names (Anthropic, FastAPI, PyYAML)
- File paths (click to view)
- Error codes (click for solution)

---

## Code Snippet Component

**Reusable pattern:**
```tsx
<CodeSnippet
  language="python"
  title="Example: Creating a Pydantic Model"
  file="generated/pydantic/overlays/example_models.py"
  lines="15-30"
  highlightLines={[18, 22]}
>
  {codeString}
</CodeSnippet>
```

**Features:**
- Syntax highlighting (via Prism.js or Shiki)
- Line numbers
- Copy button
- File path badge (clickable to view full file)
- Highlight specific lines
- Expandable/collapsible

---

## Error Handling Enhancement

**Pattern: Contextual Error Help**

When an error occurs, show:
1. ❌ Error message (clear, concise)
2. 📋 Full error output (collapsible)
3. 💡 Common causes (specific to this error)
4. 🔧 Suggested fixes (with code examples)
5. 🔗 Related documentation
6. 🔙 Go back to previous step (if applicable)

**Example:**
```tsx
<ErrorPanel error={error}>
  <ErrorTitle>gen-pydantic Validation Failed</ErrorTitle>
  <ErrorMessage>{error.message}</ErrorMessage>

  <ErrorDetails collapsible>
    <pre>{error.stderr}</pre>
  </ErrorDetails>

  <ErrorHelp>
    <HelpSection title="Common Causes">
      • Missing slot definitions in LinkML schema
      • Invalid range for slot (e.g., undefined enum)
      • Duplicate slot names
    </HelpSection>

    <HelpSection title="How to Fix">
      <p>Go back to Step 4 and ensure all slots are defined:</p>
      <CodeSnippet language="yaml">
        {`slots:
  my_field:
    range: string`}
      </CodeSnippet>
    </HelpSection>

    <HelpActions>
      <Button onClick={goToStep4}>← Fix Schema (Step 4)</Button>
      <Button variant="outline" onClick={viewDocs}>
        View LinkML Docs
      </Button>
    </HelpActions>
  </ErrorHelp>
</ErrorPanel>
```

---

## Implementation Priority

### **Phase 1: Foundation (Week 1)**
1. ✅ Context panel component (collapsible sidebar)
2. ✅ Live log viewer (bottom drawer with filtering)
3. ✅ File system browser (help sidebar)
4. ✅ Enhanced error display with contextual help

### **Phase 2: Per-Step Context (Week 2)**
1. Add context panels to Steps 1-3
2. Add inline tooltips for technical terms
3. Add "Show Details" toggles

### **Phase 3: Advanced Features (Week 3)**
1. Add context panels to Steps 4-6
2. Code snippet viewer with syntax highlighting
3. Real-time log streaming via WebSocket
4. File diff viewer

### **Phase 4: Polish (Week 4)**
1. Keyboard shortcuts
2. Search functionality
3. Export/download features
4. Performance optimization

---

## API Endpoints Needed

### **New Backend Endpoints:**

```python
# GET /api/logs/stream
# WebSocket endpoint for real-time log streaming

# GET /api/files/browse?path=/pydantic_library
# Browse file system

# GET /api/files/read?path=/pydantic_library/schemas/...
# Read file contents with syntax highlighting

# GET /api/files/download?path=...
# Download file

# GET /api/help/step/{step_number}
# Get contextual help for a specific step

# GET /api/help/error/{error_type}
# Get troubleshooting info for error type
```

---

## UI Components Needed

### **New Components:**
1. `ContextPanel.tsx` - Right sidebar with collapsible sections
2. `LiveLogViewer.tsx` - Bottom drawer with log streaming
3. `FileSystemBrowser.tsx` - Tree view of pydantic_library
4. `CodeSnippet.tsx` - Syntax-highlighted code display
5. `ErrorPanel.tsx` - Enhanced error display with help
6. `HelpSidebar.tsx` - Global help overlay
7. `StepIndicator.tsx` - Visual progress through steps

### **Enhanced Components:**
- All Step components get context panel integration
- Add tooltips throughout
- Add "Show Details" toggles

---

## Success Metrics

**A successful learning experience means:**
- ✅ Developer can understand what's happening at each step without external docs
- ✅ Errors provide actionable solutions, not just messages
- ✅ File system is transparent (can see what's being created/modified)
- ✅ Logs are accessible and filterable
- ✅ Source code is viewable in context
- ✅ Examples are readily available
- ✅ First-time user can complete workflow without asking for help

---

## Open Questions for Discussion

1. **Context Panel Visibility:** Always visible or default collapsed?
2. **Log Level:** Show DEBUG logs by default or hide them?
3. **Code Viewer:** Modal overlay or inline expansion?
4. **Mobile Support:** How to handle context panel on small screens?
5. **Performance:** Real-time log streaming vs. polling? WebSocket vs. SSE?

---

## Next Steps

1. Review this design with team
2. Create mockups/wireframes for each step
3. Prioritize which features to implement first
4. Start with Phase 1 foundation components

# Pydantic Model Generator Demo - Frontend

**Next.js 14 + TypeScript + shadcn/ui + Tailwind CSS**

---

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local` if needed (default API URL is http://localhost:8000)

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Features

- **6-Step Workflow**: Visual pipeline from business text to Pydantic models
- **Human-in-the-Loop**: Approval gates at each transformation step
- **Live AI Logs**: Server-sent events streaming Claude's reasoning
- **Library Dashboard**: View pydantic_library coverage
- **Settings Panel**: Manage environment variables

---

## Tech Stack

- **Next.js 14**: App Router with Server Components
- **TypeScript**: Type-safe development
- **shadcn/ui**: Accessible React components built on Radix UI
- **Tailwind CSS**: Utility-first styling
- **Zustand**: State management (for workflow state)
- **Sonner**: Toast notifications

---

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Homepage
│   └── globals.css         # Global styles + Tailwind
│
├── components/             # React components
│   ├── ui/                 # shadcn/ui components (to be added)
│   ├── workflow/           # Workflow step components (to be added)
│   └── ...
│
├── lib/                    # Utilities
│   └── utils.ts            # className merger (cn)
│
├── public/                 # Static assets
│
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── tailwind.config.ts      # Tailwind config
├── components.json         # shadcn/ui config
└── next.config.js          # Next.js config
```

---

## Adding shadcn/ui Components

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add toast
```

Or add all at once:
```bash
npx shadcn-ui@latest add button card input textarea tabs progress alert dialog scroll-area separator badge toast
```

---

## Development

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### Build for Production
```bash
npm run build
npm start
```

---

## API Integration

Frontend communicates with FastAPI backend at `NEXT_PUBLIC_API_URL`.

**Endpoints**:
- `POST /api/research` - Claude ontology research
- `POST /api/generate-outcome-spec` - Generate OutcomeSpec
- `POST /api/generate-linkml` - Generate LinkML schema
- `POST /api/generate-pydantic` - Generate Pydantic models
- `POST /api/run-tests` - Run pytest
- `GET /api/library-coverage` - Get library stats
- `POST /api/graphiti/ingest` - Ingest to Graphiti
- `GET /api/graphiti/status` - Get ingestion status

---

## Next Steps

1. Add shadcn/ui components
2. Build workflow step components
3. Implement SSE client for Claude streaming
4. Add state management with Zustand
5. Build library coverage dashboard
6. Add settings panel

---

**Status**: Initial setup complete

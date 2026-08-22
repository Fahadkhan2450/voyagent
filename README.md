# Voyagent - Multi-Agent Travel Planner (Web App)

Full-stack version of the multi-agent travel planner: a React frontend
talking to a FastAPI backend that runs your existing LangGraph pipeline
(Flight Agent -> Hotel Agent -> Itinerary Agent -> Final Response Agent).

```
voyagent_web/
├── backend/            FastAPI app wrapping the agent graph
│   ├── main.py          POST /api/plan, GET /api/health
│   ├── state.py         TravelState (unchanged)
│   ├── graph.py         LangGraph wiring (unchanged)
│   ├── agents/          the 4 agents (unchanged)
│   ├── tools/           tavily_client.py (unchanged)
│   ├── api/index.py     Vercel serverless entrypoint (optional)
│   ├── vercel.json       Vercel config for the backend (optional)
│   ├── requirements.txt
│   └── .env.example
└── frontend/            React + Vite + Tailwind UI
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   └── components/
    │       ├── TripForm.jsx
    │       ├── ProgressPath.jsx
    │       └── ResultsView.jsx
    ├── package.json
    └── .env.example
```

None of your agent logic changed - `main.py` only adds an HTTP layer on
top of the `build_graph()` / `new_state()` functions you already had.

## Local development

**1. Backend**

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# edit .env: add GROQ_API_KEY and TAVILY_API_KEY
uvicorn main:app --reload --port 8000
```

Check it's alive: http://localhost:8000/api/health should return `{"status":"ok"}`.
Interactive API docs: http://localhost:8000/docs

**2. Frontend** (new terminal)

```bash
cd frontend
npm install
cp .env.example .env
# default VITE_API_URL=http://localhost:8000 is already correct for local dev
npm run dev
```

Open http://localhost:5173 - fill in the boarding-pass form and submit.

## Deploying

### Frontend -> Vercel (recommended path)

1. Push this repo to GitHub.
2. In Vercel: **New Project** -> import the repo -> set **Root Directory**
   to `frontend`.
3. Framework preset: Vite (auto-detected).
4. Add an environment variable: `VITE_API_URL` = your deployed backend URL
   (see below).
5. Deploy.

### Backend -> where to actually run it

**Important:** Vercel's Hobby plan serverless functions time out at
**10 seconds**. This pipeline runs 3 sequential Tavily searches + 1 Groq
call, which can take 10-20+ seconds combined - so `/api/plan` risks
timing out on Vercel's free tier. Two options:

**Option A - deploy the backend somewhere built for longer requests
(recommended):**
[Render](https://render.com), [Railway](https://railway.app), or
[Fly.io](https://fly.io) all have free tiers well suited to this:
- Root directory: `backend`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add env vars: `GROQ_API_KEY`, `TAVILY_API_KEY`, and `FRONTEND_ORIGIN`
  (your Vercel frontend URL, e.g. `https://voyagent.vercel.app`) for CORS.
- Copy the resulting URL into the frontend's `VITE_API_URL`.

**Option B - deploy the backend on Vercel too (works if you're on Pro,
or your queries tend to run fast):**
1. In Vercel: **New Project** -> import the repo -> set **Root Directory**
   to `backend`. `vercel.json` + `api/index.py` are already set up for
   the Python runtime.
2. Add env vars: `GROQ_API_KEY`, `TAVILY_API_KEY`, `FRONTEND_ORIGIN`.
3. Deploy, then point the frontend's `VITE_API_URL` at this backend's
   Vercel URL.

Either way, **CORS is already handled** - `main.py` reads `FRONTEND_ORIGIN`
from the environment and allows that origin, in addition to `localhost:5173`
for local dev.

## Design notes

- Palette: deep dusk navy/teal background with a warm amber accent -
  evokes travel at dusk without leaning on generic "AI app" defaults.
- Type: Fraunces (display) + Inter (body) + IBM Plex Mono (labels/data).
- Signature element: the flight-path progress bar under the form -
  Flight / Hotel / Itinerary / Response are a real sequence (the actual
  agent pipeline order), so the waypoint markers encode real information,
  not decoration.
- Respects `prefers-reduced-motion` (the animated progress dot is disabled
  for users who've turned off motion at the OS level).

## What's next

- Streaming: right now the frontend just shows a looping progress
  animation while it waits for one JSON response. If you want the
  progress bar to reflect *real* agent-by-agent completion, switch
  `/api/plan` to a streaming response (Server-Sent Events or
  `StreamingResponse`) and emit an event after each node in the graph.
- Persistence: no database yet (by design, per the original project
  scope). See the original project's README for how to add it back
  without touching agent code.

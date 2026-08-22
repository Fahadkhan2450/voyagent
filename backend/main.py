"""
Voyagent API - wraps the existing LangGraph multi-agent pipeline
(flight_agent -> hotel_agent -> itinerary_agent -> final_response_agent)
in a single POST /api/plan endpoint for the React frontend.

No agent code changes needed here - this file only adds an HTTP layer
on top of build_graph() / new_state(), exactly as planned.
"""

import os
from typing import Optional, List

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from state import new_state
from graph import build_graph

app = FastAPI(title="Voyagent API", version="1.0.0")

# ---------------------------------------------------------------------------
# CORS - the frontend (Vite dev server locally, your Vercel domain in prod)
# needs to be allowed to call this API from the browser.
# Set FRONTEND_ORIGIN to your deployed frontend URL, e.g.
# https://voyagent.vercel.app
# ---------------------------------------------------------------------------
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
extra_origin = os.getenv("FRONTEND_ORIGIN")
if extra_origin:
    allowed_origins.append(extra_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the graph once at startup, reuse for every request.
_graph = build_graph()


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int = 1
    budget: Optional[str] = None
    trip_length_days: Optional[str] = None
    interests: List[str] = Field(default_factory=list)


class ResultItem(BaseModel):
    title: str = ""
    url: str = ""
    snippet: str = ""


class TripResponse(BaseModel):
    final_response: str
    flight_results: List[dict]
    hotel_results: List[dict]
    itinerary: List[dict]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/plan", response_model=TripResponse)
def plan_trip(req: TripRequest):
    if not req.origin or not req.destination or not req.departure_date:
        raise HTTPException(
            status_code=400,
            detail="origin, destination and departure_date are required.",
        )

    initial_state = new_state(req.model_dump())

    try:
        result = _graph.invoke(initial_state)
    except RuntimeError as e:
        # e.g. GROQ_API_KEY / TAVILY_API_KEY missing on the server
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {e}")

    return TripResponse(
        final_response=result.get("final_response", ""),
        flight_results=result.get("flight_results", []),
        hotel_results=result.get("hotel_results", []),
        itinerary=result.get("itinerary", []),
    )

"""
Voyagent API
FastAPI HTTP layer for the LangGraph multi-agent travel planning pipeline.
"""

import os
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from state import new_state
from graph import build_graph


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Voyagent API",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

allowed_origins = [
    # Local Vite development
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Production frontend URL
frontend_origin = os.getenv("FRONTEND_ORIGIN")

if frontend_origin:
    frontend_origin = frontend_origin.rstrip("/")

    if frontend_origin not in allowed_origins:
        allowed_origins.append(frontend_origin)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------------------------

_graph = build_graph()


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class TripRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int = 1
    budget: Optional[str] = None
    trip_length_days: Optional[str] = None
    interests: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

class TripResponse(BaseModel):
    final_response: str
    flight_results: List[dict]
    hotel_results: List[dict]
    itinerary: List[dict]


# ---------------------------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Voyagent API",
        "message": "Voyagent API is running",
    }


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Voyagent API",
    }


# ---------------------------------------------------------------------------
# Trip Planning Endpoint
# ---------------------------------------------------------------------------

@app.post("/api/plan", response_model=TripResponse)
def plan_trip(req: TripRequest):

    # Validate required fields
    if not req.origin.strip():
        raise HTTPException(
            status_code=400,
            detail="Origin is required.",
        )

    if not req.destination.strip():
        raise HTTPException(
            status_code=400,
            detail="Destination is required.",
        )

    if not req.departure_date.strip():
        raise HTTPException(
            status_code=400,
            detail="Departure date is required.",
        )

    try:
        # Convert request into the shared LangGraph state
        initial_state = new_state(req.model_dump())

        # Run the complete multi-agent pipeline
        result = _graph.invoke(initial_state)

        # Return results to React
        return TripResponse(
            final_response=result.get("final_response", ""),
            flight_results=result.get("flight_results", []),
            hotel_results=result.get("hotel_results", []),
            itinerary=result.get("itinerary", []),
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Planning failed: {str(e)}",
        )
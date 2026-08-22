"""
TravelState - the single shared state object every agent reads from
and writes to. This is the only channel agents use to communicate,
which keeps each agent decoupled from the others' internal logic.

No database here on purpose (per project requirements) - state lives
in memory for the duration of one run. See README.md "Adding
persistence later" for how to swap this for a real DB without
touching any agent code.
"""

from typing import TypedDict, List, Dict, Any


class TravelState(TypedDict, total=False):
    user_query: Dict[str, Any]          # origin, destination, dates, budget, interests...
    flight_results: List[Dict[str, Any]]  # written by flight_agent
    hotel_results: List[Dict[str, Any]]   # written by hotel_agent
    itinerary: List[Dict[str, Any]]       # written by itinerary_agent
    final_response: str                   # written by final_response_agent
    messages: List[Dict[str, str]]        # running trace/log across all agents


def new_state(user_query: Dict[str, Any]) -> TravelState:
    """Build a fresh, empty TravelState for one planning session."""
    return TravelState(
        user_query=user_query,
        flight_results=[],
        hotel_results=[],
        itinerary=[],
        final_response="",
        messages=[],
    )

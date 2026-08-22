"""
Itinerary Agent
---------------
Responsibility : gather activities / points of interest to build a
                 day-wise plan for the destination.
Data source    : Tavily Search API (free tier).

Note: the original design also called for the Google Maps API
(routing/geolocation between stops). Same reasoning as the Hotel
Agent - Google Maps requires a billing-enabled project, so it's left
out to keep the project entirely free. Tavily search is enough to
surface top attractions and activity ideas; the Final Response Agent
turns these into a day-wise structure via the LLM. Swap in a
`google_maps_client.py` later if you want real routing/travel-time
data once billing is set up.

Writes to: state["itinerary"]
"""

from state import TravelState
from tools.tavily_client import search


def itinerary_agent(state: TravelState) -> TravelState:
    query = state.get("user_query", {})
    destination = query.get("destination", "")
    interests = query.get("interests") or []
    trip_length = query.get("trip_length_days")

    search_query = f"top things to do and places to visit in {destination}"
    if interests:
        search_query += " for " + ", ".join(interests)

    raw_results = search(search_query, max_results=6)

    itinerary_items = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": (r.get("content", "") or "")[:400],
        }
        for r in raw_results
    ]

    state["itinerary"] = itinerary_items
    state.setdefault("messages", []).append(
        {
            "role": "system",
            "content": f"Itinerary Agent gathered {len(itinerary_items)} activity/POI "
            f"suggestion(s) for {destination}"
            + (f" ({trip_length} day trip)." if trip_length else "."),
        }
    )
    return state

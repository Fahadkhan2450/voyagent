"""
Hotel Agent
-----------
Responsibility : find accommodation options for the destination.
Data source    : Tavily Search API (free tier).

Note: the original design also called for the Google Places API for
structured venue data (ratings, coordinates, etc.). Google Places
requires a billing-enabled Cloud project even though it has a monthly
free credit, so it's intentionally left out here to keep the whole
project free with no credit card required. Tavily search alone is
enough to surface real hotel names, price ranges and review context.
If you later add a Google Cloud billing account, drop a
`google_places_client.py` into tools/ and merge its results here.

Writes to: state["hotel_results"]
"""

from state import TravelState
from tools.tavily_client import search


def hotel_agent(state: TravelState) -> TravelState:
    query = state.get("user_query", {})
    destination = query.get("destination", "")
    budget = query.get("budget")
    checkin_date = query.get("departure_date", "")

    search_query = f"best hotels to stay in {destination}"
    if budget:
        search_query += f" under ${budget} total budget"
    if checkin_date:
        search_query += f" around {checkin_date}"

    raw_results = search(search_query, max_results=5)

    hotel_results = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": (r.get("content", "") or "")[:400],
        }
        for r in raw_results
    ]

    state["hotel_results"] = hotel_results
    state.setdefault("messages", []).append(
        {
            "role": "system",
            "content": f"Hotel Agent found {len(hotel_results)} accommodation result(s) "
            f"for {destination}.",
        }
    )
    return state

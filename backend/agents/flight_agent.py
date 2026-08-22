"""
Flight Agent
------------
Responsibility : find flight options matching origin, destination,
                 dates and (loosely) budget.
Data source    : Tavily Search API (free tier).

Note: this originally used the Amadeus Self-Service "Flight Offers
Search" API. Amadeus decommissioned its entire self-service developer
portal on July 17, 2026 (new registrations were paused a month prior)
- there is no more free, no-credit-card flight *pricing* API left on
the market as of this writing (Kiwi's free tier closed around the
same time; the remaining options like SearchApi's Google Flights
engine or FlightAPI.io only give a one-time free credit, then charge
per request). To keep this project genuinely, indefinitely free, the
Flight Agent now uses the same Tavily Search client as the Hotel and
Itinerary agents - it can surface real flight price ranges and
airline info from search results (e.g. Google Flights / airline
listing pages) without needing a dedicated paid provider.

If you later get access to a paid or enterprise flight API, this is
the only file you'd need to change - the shared state contract
(writes to flight_results) stays the same.

Writes to: state["flight_results"]
"""

from state import TravelState
from tools.tavily_client import search


def flight_agent(state: TravelState) -> TravelState:
    query = state.get("user_query", {})

    origin = query.get("origin", "")
    destination = query.get("destination", "")
    departure_date = query.get("departure_date", "")
    return_date = query.get("return_date")
    budget = query.get("budget")

    search_query = f"flights from {origin} to {destination} on {departure_date}"
    if return_date:
        search_query += f" returning {return_date}"
    if budget:
        search_query += f" under ${budget}"
    search_query += " prices airlines"

    raw_results = search(search_query, max_results=5)

    flight_results = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": (r.get("content", "") or "")[:400],
        }
        for r in raw_results
    ]

    state["flight_results"] = flight_results
    state.setdefault("messages", []).append(
        {
            "role": "system",
            "content": f"Flight Agent found {len(flight_results)} flight-related "
            f"result(s) for {origin} \u2192 {destination} on {departure_date}.",
        }
    )
    return state

"""
Free web-search client, backed by Tavily Search API.

Tavily has a free tier (no credit card) with a generous monthly
request allowance - sign up at https://tavily.com to get an API key.
Both the Hotel Agent and the Itinerary Agent use this same client for
different queries.

The key lives only in the server's environment (TAVILY_API_KEY),
configured once in your deployment platform's dashboard (e.g. Render's
Environment tab). It is never exposed to the frontend or the browser.
"""

import os
from tavily import TavilyClient

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError(
                "TAVILY_API_KEY not set. Get a free key at https://tavily.com"
            )
        _client = TavilyClient(api_key=api_key)
    return _client


def search(query: str, max_results: int = 5) -> list[dict]:
    """Run a Tavily web search and return a list of {title, url, content}."""
    try:
        client = _get_client()
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )
        return response.get("results", [])
    except Exception as e:
        print(f"[tavily_client] search failed: {e}")
        return []

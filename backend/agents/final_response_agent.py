"""
Final Response Agent
---------------------
Responsibility : read flight_results, hotel_results and itinerary from
                 the shared state and synthesise ONE coherent,
                 natural-language travel plan.
Data source    : none (no external API call) - reads only from state.
LLM            : GROQ (free tier, fast inference) - this is the
                 user-facing step, so low latency matters most here.
Writes to      : state["final_response"]
"""

import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from state import TravelState

SYSTEM_PROMPT = """You are Voyagent, an AI travel planning assistant.

You are given:
- the user's original request
- raw flight search results (from a Flight Agent)
- raw hotel search results (from a Hotel Agent)
- raw activity/points-of-interest search results (from an Itinerary Agent)

Your job is to synthesise ALL of this into ONE clear, well-formatted,
natural-language travel plan.

Guidelines:
- Summarise flight options concisely (route + price) - don't dump raw data.
- Recommend 2-3 hotel options from the hotel results, briefly explaining why
  each fits the user's request.
- Turn the activity/POI results into an actual day-wise itinerary if a trip
  length was given; otherwise group them into a simple "things to do" list.
- If any category came back empty, say so honestly rather than inventing data.
- Keep the tone friendly and practical. Use short paragraphs and bullet points.
- End with 1-2 practical tips (best time to visit, budget note, visa/weather
  heads-up) if relevant.

Formatting rules (the output is rendered as GitHub-flavoured Markdown, not HTML):
- Never write raw HTML tags (no <ul>, <li>, <br>, <div>, etc.) anywhere,
  including inside table cells - they will NOT render and will show up as
  literal text to the user.
- Inside a markdown table cell, if you need multiple items, separate them
  with "; " on one line - do not nest a list inside a cell.
- For anything long or multi-line (like a full day-by-day itinerary),
  prefer a real markdown list or separate table rows over cramming
  content into one cell.
- Use standard markdown table syntax ( | col | col | ) with a header
  separator row, and keep cell content short enough to stay readable
  in a narrow table.
"""


def _build_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Get a free key at https://console.groq.com/keys")
    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.6, api_key=api_key)


def final_response_agent(state: TravelState) -> TravelState:
    llm = _build_llm()

    context = f"""User request: {state.get('user_query')}

Flight results:
{state.get('flight_results')}

Hotel results:
{state.get('hotel_results')}

Itinerary / activity results:
{state.get('itinerary')}
"""

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=context),
        ]
    )

    state["final_response"] = response.content
    state.setdefault("messages", []).append(
        {"role": "assistant", "content": response.content}
    )
    return state
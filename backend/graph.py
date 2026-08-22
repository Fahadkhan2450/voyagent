"""
Builds the multi-agent graph:

    START -> flight_agent -> hotel_agent -> itinerary_agent
          -> final_response_agent -> END

Sequential for simplicity/reliability. Since Hotel and Itinerary
agents don't depend on each other's output, you can switch them to
run in parallel later (see README.md "Running agents in parallel").
"""

from langgraph.graph import StateGraph, END

from state import TravelState
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.itinerary_agent import itinerary_agent
from agents.final_response_agent import final_response_agent


def build_graph():
    graph = StateGraph(TravelState)

    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_response_agent", final_response_agent)

    graph.set_entry_point("flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "final_response_agent")
    graph.add_edge("final_response_agent", END)

    return graph.compile()

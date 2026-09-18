from __future__ import annotations
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class RouterState(TypedDict):
    ticket: str
    category: str
    assigned: str
    messages: list[str]

def node_classify(state: RouterState):
    text = state["ticket"].lower()
    category = "General Support"
    if "billing" in text or "refund" in text or "charge" in text:
        category = "Billing Department"
    elif "error" in text or "crash" in text or "code" in text or "api" in text:
        category = "Technical Department"
    return {"category": category, "messages": state["messages"] + [f"Node Classified Category: {category}"]}

def node_billing(state: RouterState):
    return {"assigned": "Billing Rep Sarah", "messages": state["messages"] + ["Node Billing handled and assigned to Sarah."]}

def node_tech(state: RouterState):
    return {"assigned": "Engineer David", "messages": state["messages"] + ["Node Technical error assigned to David."]}

def node_general(state: RouterState):
    return {"assigned": "Support Rep Emily", "messages": state["messages"] + ["Node General inquiry assigned to Emily."]}

def edge_route(state: RouterState):
    if state["category"] == "Billing Department":
        return "billing"
    elif state["category"] == "Technical Department":
        return "tech"
    else:
        return "general"

def build_support_router_graph():
    builder = StateGraph(RouterState)
    builder.add_node("classify", node_classify)
    builder.add_node("billing", node_billing)
    builder.add_node("tech", node_tech)
    builder.add_node("general", node_general)

    builder.set_entry_point("classify")
    builder.add_conditional_edges(
        "classify",
        edge_route,
        {
            "billing": "billing",
            "tech": "tech",
            "general": "general"
        }
    )
    builder.add_edge("billing", END)
    builder.add_edge("tech", END)
    builder.add_edge("general", END)

    return builder.compile()

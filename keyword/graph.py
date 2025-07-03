from langgraph.graph import StateGraph, START, END
from state import KeywordState
from agent import keyword_agent

def build_keyword_graph():
    """Build the keyword research graph"""
    
    # Create the graph
    graph_builder = StateGraph(KeywordState)
    
    # Add the keyword agent node
    graph_builder.add_node("keyword_agent", keyword_agent)
    
    # Define the flow: START -> keyword_agent -> END
    graph_builder.add_edge(START, "keyword_agent")
    graph_builder.add_edge("keyword_agent", END)
    
    # Compile the graph
    graph = graph_builder.compile()
    
    return graph



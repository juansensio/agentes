from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class KeywordState(TypedDict):
    """State for the keyword research agent"""
    
    # Messages for agent communication
    messages: Annotated[list, add_messages]
    
    # Business idea input
    business_idea: str
    
    # Agent outputs
    keywords: List[str]
    questions: List[str]
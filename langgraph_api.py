from typing import Dict, Any, List, Literal, TypedDict, Optional
from langgraph.graph import StateGraph, END, START

# Import our agents
from agents.researcher import research_agent
from agents.designer import curriculum_designer
from agents.creator import content_creator
from agents.reviewer import reviewer

# Define the state schema
class AgentState(TypedDict):
    # Input values
    brief: str
    target_audience: str
    course_duration: str
   
    # Intermediate values
    research_results: Optional[List[Dict[str, Any]]]
    course_outline: Optional[Dict[str, Any]]
    modules_content: Optional[List[Dict[str, Any]]]
   
    # Final output
    final_course: Optional[Dict[str, Any]]
   
    # Control flow
    next: Literal["research", "design_curriculum", "create_content", "review", "end"]

def create_course_graph():
    """Create the course generation workflow graph."""
    # Define the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("research", research_agent)
    workflow.add_node("design_curriculum", curriculum_designer)
    workflow.add_node("create_content", content_creator)
    workflow.add_node("review", reviewer)
    
    # Define edges based on the 'next' field in state
    
    workflow.add_edge(START,"research")
    workflow.add_edge("research", "design_curriculum")
    workflow.add_edge("design_curriculum", "create_content")
    workflow.add_edge("create_content", "review")
    workflow.add_edge("review", END)

    # Compile the graph
    return workflow.compile()
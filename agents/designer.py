from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

# Define models for course structure
class Lesson(BaseModel):
    title: str = Field(..., description="Title of the lesson")
    sub_title: List[str] = Field(..., description="Sub-titles or key points of the lesson")
    content: str = Field(default=None, description="Content of the lesson")
    resources: List[str] = Field(default_factory=list, description="List of resources for the lesson")

class Module(BaseModel):
    title: str = Field(..., description="Title of the module")
    description: str = Field(..., description="Brief description of the module")
    lessons: List[Lesson] = Field(..., description="List of lessons in the module")
    time: str = Field(..., description="Time required for the module")

class Course(BaseModel):
    course_title: str = Field(..., description="Course title")
    description: str = Field(..., description="Course description")
    modules: List[Module] = Field(..., description="List of course modules")
    references: List[str] = Field(default_factory=list, description="List of references for the course")

# Create structured output LLM
designer = llm.with_structured_output(Course)

def curriculum_designer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Curriculum designer agent that creates a course outline."""
    print("🏫 Curriculum Designer: Creating course outline...")
    
    brief = state["brief"]
    target_audience = state["target_audience"]
    course_duration = state["course_duration"]
    research_results = state["research_results"]
    
    # Combine research results into a single text
    research_text = "\n\n".join([f"Query: {r['query']}\nResults: {r['result']}" for r in research_results])
    
    # Generate course outline
    curriculum_prompt = f"""
    Course Brief: {brief}
    Target Audience: {target_audience}
    Course Duration: {course_duration}
    
    Research Information:
    {research_text}
    
    Create a well-structured course outline with modules appropriate for the course duration. For each module, include multiple lesson topics with sub-titles or key points.
    """
    
    curriculum_messages = [
        SystemMessage(content="You are a curriculum design expert. Based on the research provided and course brief, create a structured course outline with an appropriate number of modules for the given course duration. Each module should have a clear title, description, time allocation, and multiple lesson topics with sub-titles or key points."),
        HumanMessage(content=curriculum_prompt)
    ]
    
    print("🧠 Designing curriculum...")
    outline_response = designer.invoke(curriculum_messages)
    
    # Get the course outline
    course_outline = outline_response.model_dump()
    
    # Update state
    state["course_outline"] = course_outline
    state["next"] = "create_content"
    print("✅ Curriculum design completed")
    return state
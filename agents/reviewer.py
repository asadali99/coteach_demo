from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,  # Lower temperature for more consistent reviewing
)

def reviewer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Review agent that checks and finalizes the course content."""
    print("🔍 Reviewer: Checking and finalizing course content...")
    
    course_outline = state["course_outline"]
    
    # Create a deep copy of the course outline to finalize
    final_course = course_outline.copy()
    
    # Review prompt
    review_prompt = f"""
    Please review this course on "{course_outline['course_title']}" for the following:
    
    1. Coherence: Ensure modules and lessons flow logically
    2. Completeness: Ensure all key topics are covered
    3. Accuracy: Ensure content is accurate and up-to-date
    4. Clarity: Ensure explanations are clear for the target audience
    5. Engagement: Ensure content is engaging and interesting
    
    Make any final improvements or adjustments before the course is delivered.
    
    Course Description: {course_outline['description']}
    Target Audience: {state['target_audience']}
    Course Duration: {state['course_duration']}
    """
    
    review_messages = [
        SystemMessage(content="You are a meticulous educational content reviewer with expertise in quality control for educational materials. Your task is to review this course, identify any issues, and suggest improvements."),
        HumanMessage(content=review_prompt)
    ]
    
    print("🧠 Conducting final review...")
    review_response = llm.invoke(review_messages)
    
    # Add the review to the final course
    final_course["review_notes"] = review_response.content
    
    # Add metadata
    final_course["metadata"] = {
        "target_audience": state["target_audience"],
        "course_duration": state["course_duration"],
        "brief": state["brief"]
    }
    
    # Update state
    state["final_course"] = final_course
    state["next"] = "end"
    print("✅ Review completed. Course generation finished.")
    return state
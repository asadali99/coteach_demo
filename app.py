from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Import our LangGraph workflow
from langgraph_api import create_course_graph

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Course Generator API", 
              description="API for generating educational courses using multi-agent LangGraph system")

# Input model for course generation request
class CourseRequest(BaseModel):
    brief: str
    target_audience: str
    course_duration: str

# Response model for generated course
class CourseResponse(BaseModel):
    course_title: str
    description: str
    modules: List[Dict[str, Any]]
    references: List[str]

@app.get("/")
async def root():
    return {"message": "Course Generator API is running"}

@app.post("/generate_course", response_model=CourseResponse)
async def generate_course(request: CourseRequest):
    try:
        # Create and run the course generation graph
        course_graph = create_course_graph()
        
        # Initialize the state
        initial_state = {
            "brief": request.brief,
            "target_audience": request.target_audience,
            "course_duration": request.course_duration,
            "research_results": None,
            "course_outline": None,
            "modules_content": None,
            "final_course": None,
            "next": "research"
        }
        
        # Execute the graph
        result = course_graph.invoke(initial_state)
        
        # Return the final course
        if not result.get("final_course"):
            raise HTTPException(status_code=500, detail="Failed to generate course")
        
        return result["final_course"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
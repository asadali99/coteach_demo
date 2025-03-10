
import os
from typing import Dict, Any, List
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

# Define a structured query model
class Query(BaseModel):
    description: str = Field(
        description="Specific very detailed research query that will help create a comprehensive course.",
    )

class Queries(BaseModel):
    queries: List[Query] = Field(
        description="List of research queries.",
    )

# Create structured output LLM
researcher = llm.with_structured_output(Queries)

@tool
def search_internet(query: str) -> str:
    """Search the internet for information related to the course topic using Tavily Search API."""
    print(f"🔍 Searching for: '{query}'")
   
    # Get API key from environment variable
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("⚠️ Tavily API key not found. Falling back to mock results.")
        return f"Search results for: {query}\n\n" + \
               "1. Recent academic papers on this topic...\n" + \
               "2. Industry best practices include...\n" + \
               "3. Educational methodologies relevant to this area...\n"
   
    # Prepare the request
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "max_results": 20,
        "include_answer": "advanced",
        "include_raw_content": True,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }
   
    # Make the request
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
   
    # Parse the response
    data = response.json()
    
    # Format the results
    results = f"Search results for: {query}\n\n"
   
    # Include the synthesized answer if available
    if "answer" in data and data["answer"]:
        results += f"SUMMARY: {data['answer']}\n\n"
       
    if "results" in data:
        for i, result in enumerate(data["results"], 1):
            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "No URL")
           
            results += f"{i}. {title}\n"
            results += f"   {content[:200]}...\n"  # Limit content length
            results += f"   URL: {url}\n\n"
    else:
        results += "No results found."
       
    return results

def research_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Research agent that generates queries and searches for information."""
    print("🔍 Research Agent: Starting research...")
    
    brief = state["brief"]
    target_audience = state["target_audience"]
   
    # Generate research queries based on the brief
    research_prompt = f"Generate research queries for a course on: {brief} targeting {target_audience}"
    research_messages = [
        SystemMessage(content="You are a specialized research agent. Your task is to identify key areas to research for a course on the given topic. Generate 7 specific research queries that will help create a comprehensive course."),
        HumanMessage(content=research_prompt)
    ]
   
    print("🧠 Generating research queries...")
    research_response = researcher.invoke(research_messages)
   
    # Extract queries from the structured response
    query_objects = research_response.model_dump().get("queries", [])
    queries = [query_obj.get("description", "") for query_obj in query_objects]
    queries = [q for q in queries if q]
   
    print(f"🔍 Generated {len(queries)} research queries")
    for i, query in enumerate(queries):
        print(f"  {i+1}. {query}")
   
    # Search for each query
    results = []
    for query in queries:
        search_result = search_internet(query)
        results.append({
            "query": query,
            "result": search_result
        })
   
    # Update state
    state["research_results"] = results
    state["next"] = "design_curriculum"
    print("✅ Research completed")
    return state
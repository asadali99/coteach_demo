from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

def content_creator(state: Dict[str, Any]) -> Dict[str, Any]:
    """Content creator agent that generates detailed content for each lesson."""
    print("📝 Content Creator: Generating module and lesson content...")
    
    brief = state["brief"]
    target_audience = state["target_audience"]
    course_outline = state["course_outline"]
    research_results = state["research_results"]
    
    # Combine research results for reference
    research_text = "\n\n".join([f"Query: {r['query']}\nResults: {r['result']}" for r in research_results])
    
    # Create content for each module and lesson
    for i, module in enumerate(course_outline["modules"]):
        print(f"📝 Creating content for module {i+1}: {module['title']}")
        
        for j, lesson in enumerate(module["lessons"]):
            print(f"  Lesson {j+1}: {lesson['title']}")
            
            # Format the sub-titles for the prompt
            sub_titles = "\n".join([f"- {st}" for st in lesson["sub_title"]])
            
            lesson_prompt = f"""
            Create detailed content for:
            Course: {course_outline['course_title']}
            Module: {module['title']}
            Lesson: {lesson['title']}
            
            Key points to cover:
            {sub_titles}
            
            Time allocation: {module['time']} (for the entire module with {len(module['lessons'])} lessons)
            Target Audience: {target_audience}
            
            Use this research information as reference:
            {research_text}
            """
            
            content_messages = [
                SystemMessage(content="You are a content creation expert. Generate comprehensive educational content that is clear, engaging, and tailored to the target audience. Include explanations, examples, and practical applications where appropriate."),
                HumanMessage(content=lesson_prompt)
            ]
            
            print(f"    🧠 Generating content for this lesson...")
            content_response = llm.invoke(content_messages)
            lesson["content"] = content_response.content
            
            # Generate resources recommendation
            resources_prompt = f"""
            Recommend 3-5 specific resources (books, articles, videos, tools) that would be helpful for students studying:
            
            Course: {course_outline['course_title']}
            Module: {module['title']}
            Lesson: {lesson['title']}
            
            Target Audience: {target_audience}
            """
            
            resources_messages = [
                SystemMessage(content="You are an educational resource specialist. Recommend specific, relevant resources for this lesson topic."),
                HumanMessage(content=resources_prompt)
            ]
            
            print(f"    📚 Generating resources for this lesson...")
            resources_response = llm.invoke(resources_messages)
            
            # Extract resources from the response (this is simplified)
            resources_lines = resources_response.content.strip().split("\n")
            resources = [line for line in resources_lines if line.strip() and not line.strip().startswith("#")]
            lesson["resources"] = resources[:5]  # Limit to 5 resources
    
    # Update state
    state["next"] = "review"
    print("✅ Content creation completed")
    return state
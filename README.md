# Course Generator - Multi-Agent System

A sophisticated multi-agent system built with LangGraph and FastAPI that automatically generates comprehensive educational courses from brief descriptions. The system researches relevant content, organizes it into modules, and produces structured educational material.

## Features

- **Multi-Agent Architecture**: Leverages specialized AI agents for different aspects of course creation
- **Intelligent Research**: Searches for up-to-date information using Tavily Search API
- **Comprehensive Course Generation**: Creates complete course structures with modules, lessons, and content
- **RESTful API**: Easy-to-use FastAPI endpoints for course generation
- **Configurable Parameters**: Customize course duration, target audience, and more

## System Architecture

The system employs a sequential workflow of specialized agents:

1. **Research Agent**: Generates research queries and gathers information
2. **Curriculum Designer**: Creates a structured course outline with modules
3. **Content Creator**: Develops detailed lesson content and resources
4. **Reviewer**: Performs final quality checks and improvements

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (optional but recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/asadali99/coteach_demo.git
   cd coteach_demo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     OPENAI_API_KEY=your-openai-api-key
     TAVILY_API_KEY=your-tavily-api-key
     ```

## Usage

### Running the API Server

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### Generate a Course

**Endpoint**: `POST /generate_course`

**Request Body**:
```json
{
  "brief": "A microfinance course for beginners who need to learn from basics",
  "target_audience": "College students with no financial background",
  "course_duration": "6 weeks"
}
```

**Response**:
```json
{
  "course_title": "Introduction to Microfinance: Fundamentals and Applications",
  "description": "A comprehensive introduction to microfinance principles...",
  "modules": [
    {
      "title": "Module 1: Understanding Microfinance Basics",
      "description": "An introduction to the core concepts...",
      "time": "1 week",
      "lessons": [
        {
          "title": "What is Microfinance?",
          "sub_title": ["Definition and scope", "Key principles"],
          "content": "Microfinance is the provision of financial services...",
          "resources": ["Book: Microfinance Handbook", "Video: Introduction to Microfinance"]
        },
        ...
      ]
    },
    ...
  ],
  "references": [
    "Source 1: Journal of Microfinance Studies",
    "Source 2: World Bank Microfinance Reports",
    ...
  ]
}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
course-generator/
├── agents/                     # Agent implementations
│   ├── __init__.py
│   ├── researcher.py           # Research agent
│   ├── designer.py             # Curriculum designer agent
│   ├── creator.py              # Content creator agent
│   └── reviewer.py             # Reviewer agent
├── example_requests/           # Example API requests
│   ├── microfinance_course.json  # Example request for a microfinance course
│   ├── RAG_course.json           # Example request for a RAG course
│   └── response_rag_course.json  # Example response for the RAG course
├── .env                        # Environment variables (not in repo)
├── app.py                      # FastAPI application
├── langgraph_api.py            # LangGraph workflow definition
├── langgraph.json              # LangGraph configuration
└── requirements.txt            # Project dependencies
```

## Technologies Used

- **LangGraph**: Orchestration of AI agents
- **LangChain**: Building blocks for LLM applications
- **OpenAI**: Large language models for content generation
- **FastAPI**: Modern web framework for APIs
- **Pydantic**: Data validation and settings management
- **Tavily API**: Search engine for research

## Development

### Adding a New Agent

1. Create a new agent module in the `agents/` directory
2. Define the agent function with appropriate state handling
3. Add the agent to the workflow in `langgraph_api.py`
4. Update the `__init__.py` file to expose the new agent
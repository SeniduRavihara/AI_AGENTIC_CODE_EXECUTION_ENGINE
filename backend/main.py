"""
FastAPI Server for AI Python Code Execution
Real AI agents using Google Gemini
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agents import CoordinatorAgent

# Initialize FastAPI app
app = FastAPI(
    title="AI Python Interpreter",
    description="Real AI agents using Gemini for Python code execution simulation",
    version="1.0.0"
)

# Initialize AI coordinator
try:
    coordinator = CoordinatorAgent()
except ValueError as e:
    print(f"❌ AI initialization failed: {e}")
    print("Set GEMINI_API_KEY environment variable")
    coordinator = None


class CodeRequest(BaseModel):
    code: str
    language: str = "python"


class CodeResponse(BaseModel):
    success: bool
    final_variables: Dict[str, Any]
    execution_steps: list
    ai_reasoning: str
    confidence: float
    execution_time: float
    timestamp: str
    coordinator: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Python Interpreter Server",
        "description": "Real AI agents using Gemini for Python code execution",
        "status": "running",
        "endpoints": {
            "/execute": "POST - Execute Python code with AI",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if coordinator is None:
        return {
            "status": "unhealthy",
            "error": "AI coordinator not initialized",
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "status": "healthy",
        "ai_model": "models/gemini-2.5-flash",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """Execute Python code using AI agents"""
    
    if coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="AI coordinator not initialized. Check GEMINI_API_KEY."
        )
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language.lower() != "python":
        raise HTTPException(status_code=400, detail="Only Python code is supported")
    
    try:
        start_time = datetime.now()
        
        # Execute code with AI
        result = await coordinator.execute_code(request.code)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return CodeResponse(
            success=result.get("success", False),
            final_variables=result.get("final_variables", {}),
            execution_steps=result.get("execution_steps", []),
            ai_reasoning=result.get("ai_reasoning", ""),
            confidence=result.get("confidence", 0.0),
            execution_time=execution_time,
            timestamp=result["coordinator"]["timestamp"],
            coordinator=result["coordinator"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/execute-simple")
async def execute_simple(code: str):
    """Simple endpoint - just pass code as string"""
    
    if coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="AI coordinator not initialized. Check GEMINI_API_KEY."
        )
    
    if not code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        start_time = datetime.now()
        
        result = await coordinator.execute_code(code)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": result.get("success", False),
            "final_variables": result.get("final_variables", {}),
            "ai_reasoning": result.get("ai_reasoning", ""),
            "confidence": result.get("confidence", 0.0),
            "execution_time": execution_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY not found!")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print("Set it with: set GEMINI_API_KEY=your_key_here")
        exit(1)
    
    print("🚀 Starting AI Python Interpreter Server...")
    print("🤖 Using Google Gemini for AI reasoning")
    print("📡 Server: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

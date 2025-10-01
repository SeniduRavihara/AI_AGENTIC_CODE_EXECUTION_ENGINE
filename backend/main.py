"""
FastAPI Server for AI Python Code Execution
Real AI agents using Google Gemini
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agents.multi_language_coordinator import MultiLanguageCoordinator
from agents.python.python_coordinator import PythonCoordinator
from agents.java.java_coordinator import JavaCoordinator
from agents.dsa_coordinator import DSACoordinator

# Initialize FastAPI app
app = FastAPI(
    title="AI Python Interpreter",
    description="Real AI agents using Gemini for Python code execution simulation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI coordinators
try:
    # Multi-language coordinator with dedicated language coordinators
    multi_coordinator = MultiLanguageCoordinator()
    python_coordinator = PythonCoordinator()
    java_coordinator = JavaCoordinator()
    dsa_coordinator = DSACoordinator()
    print("🚀 Multi-Language AI Interpreter System initialized!")
    print("🧠 DSA Optimization System ready!")
except ValueError as e:
    print(f"❌ AI initialization failed: {e}")
    print("Set GEMINI_API_KEY environment variable")
    multi_coordinator = None
    python_coordinator = None
    java_coordinator = None
    dsa_coordinator = None


class CodeRequest(BaseModel):
    code: str
    language: str = "python"

class DSARequest(BaseModel):
    code: str
    language: str = "python"
    problem_type: str = "general"  # sorting, graph, dp, tree, array, etc.
    input_data: Optional[Any] = None
    optimization_level: str = "auto"  # auto, sequential, parallel, aggressive


class CodeResponse(BaseModel):
    success: bool
    final_variables: Dict[str, Any]
    console_output: list
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
    if multi_coordinator is None:
        return {
            "status": "unhealthy",
            "error": "Multi-language coordinator not initialized",
            "timestamp": datetime.now().isoformat()
        }
    
    # Check pipeline status
    pipeline_status = multi_coordinator.get_pipeline_status() if multi_coordinator else {"multi_language_coordinator": False}
    
    return {
        "status": "healthy",
        "ai_model": "models/gemini-2.5-flash",
        "multi_language_support": pipeline_status.get("multi_language_coordinator", False),
        "supported_languages": pipeline_status.get("supported_languages", {}),
        "interpreter_architecture": "Multi-Language Agent Pipeline System",
        "language_details": pipeline_status.get("language_details", {}),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/execute", response_model=CodeResponse)
async def execute_code(request: CodeRequest):
    """Execute code using multi-language AI interpreter system"""
    
    if multi_coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="Multi-language coordinator not initialized. Check GEMINI_API_KEY."
        )
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language.lower() not in ["python", "java"]:
        raise HTTPException(status_code=400, detail="Only Python and Java code are supported")
    
    try:
        start_time = datetime.now()
        
        # Use multi-language coordinator for proper language routing
        print(f"🔄 Using {request.language.title()} Interpreter via Multi-Language Coordinator")
        result = await multi_coordinator.execute_code(request.code, request.language, use_pipeline=True)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return CodeResponse(
            success=result.get("success", False),
            final_variables=result.get("final_variables", {}),
            console_output=result.get("console_output", []),
            execution_steps=result.get("execution_steps", []),
            ai_reasoning=result.get("ai_reasoning", ""),
            confidence=result.get("confidence", 0.0),
            execution_time=execution_time,
            timestamp=result["coordinator"]["timestamp"],
            coordinator=result["coordinator"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.post("/execute-pipeline")
async def execute_pipeline(request: CodeRequest):
    """Execute code using language-specific FULL interpreter pipeline (experimental)"""
    
    if request.language.lower() == "python" and python_coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="Python coordinator not available."
        )
    elif request.language.lower() == "java" and java_coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="Java coordinator not available."
        )
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        start_time = datetime.now()
        print(f"🔬 Using FULL {request.language.title()} Interpreter Pipeline (Experimental)")
        
        # Route to specific coordinator
        if request.language.lower() == "python":
            result = await python_coordinator.execute_code(request.code, use_pipeline=True)
        elif request.language.lower() == "java":
            result = await java_coordinator.execute_code(request.code, use_pipeline=True)
        else:
            raise HTTPException(status_code=400, detail=f"Language {request.language} not supported")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return CodeResponse(
            success=result.get("success", False),
            final_variables=result.get("final_variables", {}),
            console_output=result.get("console_output", []),
            execution_steps=result.get("execution_steps", []),
            ai_reasoning=result.get("ai_reasoning", ""),
            confidence=result.get("confidence", 0.0),
            execution_time=execution_time,
            timestamp=result["coordinator"]["timestamp"],
            coordinator=result["coordinator"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")


@app.post("/execute-dsa")
async def execute_dsa_problem(request: DSARequest):
    """Execute DSA problems with intelligent optimization and parallel processing"""
    
    if dsa_coordinator is None:
        raise HTTPException(
            status_code=500,
            detail="DSA coordinator not initialized. Check GEMINI_API_KEY."
        )
    
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if request.language.lower() not in ["python", "java"]:
        raise HTTPException(status_code=400, detail="Only Python and Java code are supported")
    
    if request.problem_type not in ["general", "sorting", "graph", "dp", "tree", "array", "string", "math"]:
        raise HTTPException(status_code=400, detail="Invalid problem type")
    
    if request.optimization_level not in ["auto", "sequential", "parallel", "aggressive"]:
        raise HTTPException(status_code=400, detail="Invalid optimization level")
    
    try:
        start_time = datetime.now()
        
        print(f"🧠 DSA Problem Execution Request")
        print(f"📝 Problem Type: {request.problem_type}")
        print(f"⚙️ Optimization: {request.optimization_level}")
        
        result = await dsa_coordinator.execute_dsa_problem(
            code=request.code,
            language=request.language,
            problem_type=request.problem_type,
            input_data=request.input_data,
            optimization_level=request.optimization_level
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            **result,
            "total_execution_time": execution_time,
            "dsa_endpoint": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DSA execution failed: {str(e)}")


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

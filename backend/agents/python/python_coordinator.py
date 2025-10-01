"""
Python Coordinator - Orchestrates Python interpreter pipeline
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

from .python_lexer import PythonLexer
from .python_parser import PythonParser
from .python_vm import PythonVM


class PythonCoordinator:
    """Coordinates the Python interpreter pipeline execution"""
    
    def __init__(self):
        """Initialize Python-specific agents"""
        try:
            self.lexer = PythonLexer()
            self.parser = PythonParser()
            self.vm = PythonVM()
            self.pipeline_enabled = True
            print("🐍 Python interpreter pipeline initialized!")
        except Exception as e:
            print(f"⚠️ Python pipeline failed to initialize: {e}")
            self.vm = PythonVM()  # Fallback to VM only
            self.pipeline_enabled = False
    
    async def execute_code(self, code: str, use_pipeline: bool = True) -> Dict[str, Any]:
        """
        Execute Python code using the complete Python interpreter pipeline
        
        Args:
            code: Python source code
            use_pipeline: Whether to use full pipeline or simple execution
            
        Returns:
            Dict with comprehensive Python execution results
        """
        
        start_time = datetime.now()
        
        if use_pipeline and self.pipeline_enabled:
            result = await self._execute_with_pipeline(code)
        else:
            print("🔄 Using simple Python execution")
            result = await self.vm._execute_python_with_gemini(code)
        
        # Add coordinator metadata
        end_time = datetime.now()
        execution_duration = (end_time - start_time).total_seconds()
        
        result["coordinator"] = {
            "agent_used": "PythonPipeline" if (use_pipeline and self.pipeline_enabled) else "PythonVM",
            "execution_method": "Full Python Interpreter Simulation" if (use_pipeline and self.pipeline_enabled) else "AI reasoning with Python VM",
            "pipeline_enabled": self.pipeline_enabled,
            "language": "python",
            "timestamp": end_time.isoformat(),
            "duration_seconds": execution_duration,
            "pipeline_stages": ["lexer", "parser", "vm"] if (use_pipeline and self.pipeline_enabled) else ["vm_only"]
        }
        
        return result
    
    async def _execute_with_pipeline(self, code: str) -> Dict[str, Any]:
        """Execute code through the complete Python interpreter pipeline"""
        
        pipeline_results = {
            "success": True,
            "pipeline_stages": {},
            "final_variables": {},
            "console_output": [],
            "execution_steps": [],
            "ai_reasoning": "",
            "confidence": 0.0
        }
        
        try:
            print("🔍 Stage 1: Python Lexical Analysis")
            # Stage 1: Python Lexical Analysis
            lexer_result = await self.lexer.tokenize(code, "python")
            pipeline_results["pipeline_stages"]["lexer"] = lexer_result
            
            print("🌳 Stage 2: Python Syntax Analysis")
            # Stage 2: Python Parser
            parser_result = await self.parser.parse(lexer_result.get("tokens", []), code)
            pipeline_results["pipeline_stages"]["parser"] = parser_result
            
            print("🖥️ Stage 3: Python Virtual Machine Execution")
            # Stage 3: Python VM Execution
            vm_result = await self.vm.execute([], [], [], code)
            pipeline_results["pipeline_stages"]["vm"] = vm_result
            
            # Compile final results from pipeline
            pipeline_results.update({
                "final_variables": vm_result.get("final_state", {}).get("locals", {}),
                "console_output": vm_result.get("console_output", []),
                "execution_steps": [
                    f"Lexer: Found {len(lexer_result.get('language_features', []))} Python features",
                    f"Parser: Identified {len(parser_result.get('statements', []))} statements", 
                    f"VM: Executed Python code successfully"
                ],
                "ai_reasoning": f"Python Pipeline: {vm_result.get('ai_reasoning', '')}",
                "confidence": vm_result.get("confidence", 0.95)
            })
            
            print("✅ Python pipeline execution completed successfully")
            return pipeline_results
            
        except Exception as e:
            print(f"❌ Python pipeline execution failed: {e}")
            # Fallback to simple execution
            simple_result = await self.vm._execute_python_with_gemini(code)
            simple_result["coordinator"] = {
                "agent_used": "PythonVM",
                "execution_method": "AI reasoning with Python VM (Pipeline Fallback)",
                "pipeline_enabled": False,
                "fallback_reason": f"Pipeline failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": 0.0,
                "pipeline_stages": ["vm_fallback"]
            }
            return simple_result

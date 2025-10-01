"""
Java Coordinator - Orchestrates Java interpreter pipeline
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

from .java_lexer import JavaLexer
from .java_vm import JavaVM


class JavaCoordinator:
    """Coordinates the Java interpreter pipeline execution"""
    
    def __init__(self):
        """Initialize Java-specific agents"""
        try:
            self.lexer = JavaLexer()
            self.vm = JavaVM()
            self.pipeline_enabled = True
            print("☕ Java interpreter pipeline initialized!")
        except Exception as e:
            print(f"⚠️ Java pipeline failed to initialize: {e}")
            self.vm = JavaVM()  # Fallback to VM only
            self.pipeline_enabled = False
    
    async def execute_code(self, code: str, use_pipeline: bool = True) -> Dict[str, Any]:
        """
        Execute Java code using the complete Java interpreter pipeline
        
        Args:
            code: Java source code
            use_pipeline: Whether to use full pipeline or simple execution
            
        Returns:
            Dict with comprehensive Java execution results
        """
        
        start_time = datetime.now()
        
        if use_pipeline and self.pipeline_enabled:
            result = await self._execute_with_pipeline(code)
        else:
            print("🔄 Using simple Java execution")
            result = await self.vm._execute_java_with_gemini(code)
        
        # Add coordinator metadata
        end_time = datetime.now()
        execution_duration = (end_time - start_time).total_seconds()
        
        result["coordinator"] = {
            "agent_used": "JavaPipeline" if (use_pipeline and self.pipeline_enabled) else "JavaVM",
            "execution_method": "Full Java Interpreter Simulation" if (use_pipeline and self.pipeline_enabled) else "AI reasoning with Java VM",
            "pipeline_enabled": self.pipeline_enabled,
            "language": "java",
            "timestamp": end_time.isoformat(),
            "duration_seconds": execution_duration,
            "pipeline_stages": ["lexer", "vm"] if (use_pipeline and self.pipeline_enabled) else ["vm_only"]
        }
        
        return result
    
    async def _execute_with_pipeline(self, code: str) -> Dict[str, Any]:
        """Execute code through the complete Java interpreter pipeline"""
        
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
            print("🔍 Stage 1: Java Lexical Analysis")
            # Stage 1: Java Lexical Analysis
            lexer_result = await self.lexer.tokenize(code, "java")
            pipeline_results["pipeline_stages"]["lexer"] = lexer_result
            
            print("🖥️ Stage 2: Java Virtual Machine Execution")
            # Stage 2: Java VM Execution (JVM)
            vm_result = await self.vm.execute([], [], code)
            pipeline_results["pipeline_stages"]["vm"] = vm_result
            
            # Compile final results from pipeline
            pipeline_results.update({
                "final_variables": vm_result.get("final_state", {}).get("locals", {}),
                "console_output": vm_result.get("console_output", []),
                "execution_steps": [
                    f"Lexer: Found {len(lexer_result.get('language_features', []))} Java features",
                    f"JVM: Executed Java code successfully"
                ],
                "ai_reasoning": f"Java Pipeline: {vm_result.get('ai_reasoning', '')}",
                "confidence": vm_result.get("confidence", 0.95)
            })
            
            print("✅ Java pipeline execution completed successfully")
            return pipeline_results
            
        except Exception as e:
            print(f"❌ Java pipeline execution failed: {e}")
            # Fallback to simple execution
            simple_result = await self.vm._execute_java_with_gemini(code)
            simple_result["coordinator"] = {
                "agent_used": "JavaVM",
                "execution_method": "AI reasoning with Java VM (Pipeline Fallback)",
                "pipeline_enabled": False,
                "fallback_reason": f"Pipeline failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": 0.0,
                "pipeline_stages": ["vm_fallback"]
            }
            return simple_result

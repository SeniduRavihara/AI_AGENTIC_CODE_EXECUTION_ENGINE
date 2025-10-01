"""
Enhanced Interpreter Coordinator - Orchestrates AI Python Interpreter Pipeline
Mimics the complete Python interpreter execution flow
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

from .lexer_agent import LexerAgent
from .parser_agent import ParserAgent
from .compiler_agent import CompilerAgent
from .vm_agent import VMAgent
from .runtime_agent import RuntimeAgent
from .gemini_agent import GeminiAgent  # Fallback for simple execution


class InterpreterCoordinator:
    """
    Enhanced coordinator that mimics Python interpreter's complete pipeline:
    Source Code → Lexer → Parser → Compiler → VM → Runtime Environment
    """
    
    def __init__(self):
        """Initialize all interpreter agents"""
        try:
            self.lexer_agent = LexerAgent()
            self.parser_agent = ParserAgent()
            self.compiler_agent = CompilerAgent()
            self.vm_agent = VMAgent()
            self.runtime_agent = RuntimeAgent()
            self.gemini_agent = GeminiAgent()  # Fallback
            self.pipeline_enabled = True
        except Exception as e:
            print(f"⚠️ Enhanced pipeline failed to initialize: {e}")
            print("📱 Falling back to simple GeminiAgent execution")
            self.gemini_agent = GeminiAgent()
            self.pipeline_enabled = False
    
    async def execute_code(self, code: str, language: str = "python", use_pipeline: bool = True) -> Dict[str, Any]:
        """
        Execute code using the complete interpreter pipeline for any supported language
        
        Args:
            code: Source code
            language: Programming language (python, java, etc.)
            use_pipeline: Whether to use full interpreter pipeline or simple execution
            
        Returns:
            Dict with comprehensive execution results
        """
        
        start_time = datetime.now()
        
        # Choose execution method
        if use_pipeline and self.pipeline_enabled:
            result = await self._execute_with_pipeline(code, language)
        else:
            print(f"🔄 Using simple execution (GeminiAgent) for {language.title()}")
            if language.lower() == "java":
                # For Java, we can use a direct prompt to GeminiAgent
                result = await self._execute_java_simple(code)
            else:
                result = await self.gemini_agent.execute_python_code(code)
        
        # Add coordinator metadata
        end_time = datetime.now()
        execution_duration = (end_time - start_time).total_seconds()
        
        result["coordinator"] = {
            "agent_used": "InterpreterPipeline" if (use_pipeline and self.pipeline_enabled) else "GeminiAgent",
            "execution_method": f"Full {language.title()} Interpreter Simulation" if (use_pipeline and self.pipeline_enabled) else f"AI reasoning with Google Gemini ({language.title()})",
            "pipeline_enabled": self.pipeline_enabled,
            "language": language,
            "timestamp": end_time.isoformat(),
            "duration_seconds": execution_duration,
            "pipeline_stages": ["lexer", "parser", "compiler", "vm", "runtime"] if (use_pipeline and self.pipeline_enabled) else ["gemini_ai"]
        }
        
        return result
    
    async def _execute_with_pipeline(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code through the complete interpreter pipeline for any language"""
        
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
            print(f"🔍 Stage 1: Lexical Analysis ({language.title()} Tokenization)")
            # Stage 1: Lexical Analysis
            lexer_result = await self.lexer_agent.tokenize(code, language)
            pipeline_results["pipeline_stages"]["lexer"] = lexer_result
            
            if not lexer_result["success"]:
                return self._handle_pipeline_error("lexer", lexer_result, pipeline_results)
            
            print(f"🌳 Stage 2: Syntax Analysis ({language.title()} AST Generation)")
            # Stage 2: Syntax Analysis (Parser)
            parser_result = await self.parser_agent.parse(
                lexer_result.get("tokens", []), code, language
            )
            pipeline_results["pipeline_stages"]["parser"] = parser_result
            
            if not parser_result["success"]:
                return self._handle_pipeline_error("parser", parser_result, pipeline_results)
            
            print(f"⚙️ Stage 3: Compilation ({language.title()} Bytecode Generation)")
            # Stage 3: Compilation
            compiler_result = await self.compiler_agent.compile(
                parser_result.get("ast", {}), code, language
            )
            pipeline_results["pipeline_stages"]["compiler"] = compiler_result
            
            if not compiler_result["success"]:
                return self._handle_pipeline_error("compiler", compiler_result, pipeline_results)
            
            vm_name = "JVM" if language.lower() == "java" else "PVM"
            print(f"🖥️ Stage 4: Virtual Machine Execution ({vm_name})")
            # Stage 4: VM Execution
            vm_result = await self.vm_agent.execute(
                compiler_result.get("bytecode", []),
                compiler_result.get("constants", []),
                compiler_result.get("names", []),
                code,
                language
            )
            pipeline_results["pipeline_stages"]["vm"] = vm_result
            
            if not vm_result["success"]:
                return self._handle_pipeline_error("vm", vm_result, pipeline_results)
            
            runtime_name = "JVM Runtime" if language.lower() == "java" else "Python Runtime"
            print(f"🏃 Stage 5: Runtime Environment Management ({runtime_name})")
            # Stage 5: Runtime Environment
            runtime_result = await self.runtime_agent.manage_runtime(
                vm_result.get("final_state", {}), code, language
            )
            pipeline_results["pipeline_stages"]["runtime"] = runtime_result
            
            # Compile final results from pipeline
            pipeline_results.update({
                "final_variables": vm_result.get("final_state", {}).get("locals", {}),
                "console_output": vm_result.get("console_output", []),
                "execution_steps": self._generate_execution_steps(pipeline_results),
                "ai_reasoning": self._generate_comprehensive_reasoning(pipeline_results),
                "confidence": self._calculate_pipeline_confidence(pipeline_results)
            })
            
            print("✅ Pipeline execution completed successfully")
            return pipeline_results
            
        except Exception as e:
            print(f"❌ Pipeline execution failed: {e}")
            print("🔄 Falling back to simple GeminiAgent execution")
            
            # Fallback to simple execution
            try:
                simple_result = await self.gemini_agent.execute_python_code(code)
                simple_result["coordinator"] = {
                    "agent_used": "GeminiAgent",
                    "execution_method": "AI reasoning with Google Gemini (Pipeline Fallback)",
                    "pipeline_enabled": False,
                    "fallback_reason": f"Pipeline failed: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                    "duration_seconds": 0.0,
                    "pipeline_stages": ["gemini_fallback"]
                }
                return simple_result
            except Exception as fallback_error:
                print(f"❌ Fallback execution also failed: {fallback_error}")
                return self._handle_pipeline_error("fallback", {"error": str(fallback_error)}, pipeline_results)
    
    def _handle_pipeline_error(self, stage: str, error_result: dict, pipeline_results: dict) -> dict:
        """Handle errors in pipeline execution"""
        pipeline_results.update({
            "success": False,
            "error_stage": stage,
            "error": error_result.get("error", f"Failed at {stage} stage"),
            "ai_reasoning": f"Pipeline failed at {stage} stage: {error_result.get('error', 'Unknown error')}",
            "confidence": 0.0
        })
        return pipeline_results
    
    def _generate_execution_steps(self, pipeline_results: dict) -> list:
        """Generate execution steps from pipeline results"""
        steps = []
        
        # Lexer steps
        if "lexer" in pipeline_results["pipeline_stages"]:
            lexer_data = pipeline_results["pipeline_stages"]["lexer"]
            steps.append(f"Lexer: Tokenized {len(lexer_data.get('tokens', []))} tokens")
        
        # Parser steps
        if "parser" in pipeline_results["pipeline_stages"]:
            parser_data = pipeline_results["pipeline_stages"]["parser"]
            steps.append(f"Parser: Generated AST with {len(parser_data.get('statements', []))} statements")
        
        # Compiler steps
        if "compiler" in pipeline_results["pipeline_stages"]:
            compiler_data = pipeline_results["pipeline_stages"]["compiler"]
            steps.append(f"Compiler: Generated {len(compiler_data.get('bytecode', []))} bytecode instructions")
        
        # VM steps
        if "vm" in pipeline_results["pipeline_stages"]:
            vm_data = pipeline_results["pipeline_stages"]["vm"]
            steps.append(f"VM: Executed {len(vm_data.get('execution_trace', []))} instructions")
        
        # Runtime steps
        if "runtime" in pipeline_results["pipeline_stages"]:
            runtime_data = pipeline_results["pipeline_stages"]["runtime"]
            steps.append(f"Runtime: Managed {len(runtime_data.get('namespaces', {}).get('locals', {}))} variables")
        
        return steps
    
    def _generate_comprehensive_reasoning(self, pipeline_results: dict) -> str:
        """Generate comprehensive AI reasoning from all pipeline stages"""
        reasoning_parts = []
        
        for stage, data in pipeline_results["pipeline_stages"].items():
            if stage in data and "analysis" in str(data):
                analysis_key = f"{stage}_analysis"
                if analysis_key in data:
                    reasoning_parts.append(f"**{stage.title()} Stage**: {data[analysis_key]}")
        
        if reasoning_parts:
            return "\n\n".join(reasoning_parts)
        else:
            return "AI successfully executed the code through the complete Python interpreter pipeline, mimicking lexical analysis, parsing, compilation, virtual machine execution, and runtime management."
    
    def _calculate_pipeline_confidence(self, pipeline_results: dict) -> float:
        """Calculate overall confidence based on pipeline stage success"""
        total_stages = 5  # lexer, parser, compiler, vm, runtime
        successful_stages = len([
            stage for stage in ["lexer", "parser", "compiler", "vm", "runtime"]
            if stage in pipeline_results["pipeline_stages"] and 
               pipeline_results["pipeline_stages"][stage].get("success", False)
        ])
        
        return successful_stages / total_stages
    
    async def _execute_java_simple(self, code: str) -> Dict[str, Any]:
        """Execute Java code using simple Gemini execution"""
        # Use the VMAgent's Java execution method
        try:
            from .vm_agent import VMAgent
            vm_agent = VMAgent()
            return await vm_agent._execute_java_with_gemini(self.gemini_agent, code)
        except Exception as e:
            return {
                "success": False,
                "final_variables": {},
                "console_output": [],
                "execution_steps": [],
                "ai_reasoning": f"Java execution failed: {str(e)}",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_pipeline_status(self) -> dict:
        """Get current pipeline status"""
        return {
            "pipeline_enabled": self.pipeline_enabled,
            "agents_available": {
                "lexer": hasattr(self, 'lexer_agent'),
                "parser": hasattr(self, 'parser_agent'),
                "compiler": hasattr(self, 'compiler_agent'),
                "vm": hasattr(self, 'vm_agent'),
                "runtime": hasattr(self, 'runtime_agent'),
                "gemini": hasattr(self, 'gemini_agent')
            }
        }

"""
DSA Coordinator - High-level coordinator for Data Structures & Algorithms problems
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from .shared.dsa_orchestrator import DSAOrchestrator
from .python.python_coordinator import PythonCoordinator
from .java.java_coordinator import JavaCoordinator


class DSACoordinator:
    """
    Specialized coordinator for handling large-scale DSA problems with dynamic agent creation
    """
    
    def __init__(self):
        """Initialize DSA coordinator with orchestrator and language coordinators"""
        try:
            self.dsa_orchestrator = DSAOrchestrator()
            self.python_coordinator = PythonCoordinator()
            self.java_coordinator = JavaCoordinator()
            self.enabled = True
            print("🧠 DSA Coordinator with Dynamic Agent Factory initialized!")
        except Exception as e:
            print(f"⚠️ DSA Coordinator failed to initialize: {e}")
            self.enabled = False
    
    async def execute_dsa_problem(self, code: str, language: str = "python", 
                                problem_type: str = "general", input_data: Any = None,
                                optimization_level: str = "auto") -> Dict[str, Any]:
        """
        Execute DSA problem with intelligent optimization and parallel processing
        
        Args:
            code: DSA algorithm code
            language: Programming language (python, java)
            problem_type: Type of DSA problem (sorting, graph, dp, tree, etc.)
            input_data: Input dataset (can be very large)
            optimization_level: auto, sequential, parallel, or aggressive
            
        Returns:
            Comprehensive execution results with performance analysis
        """
        
        start_time = datetime.now()
        
        if not self.enabled:
            return self._create_fallback_response("DSA Coordinator not available")
        
        print(f"🧠 DSA Problem Execution Started")
        print(f"📝 Language: {language}")
        print(f"🎯 Problem Type: {problem_type}")
        print(f"⚙️ Optimization Level: {optimization_level}")
        
        try:
            # Determine execution approach based on problem characteristics
            execution_approach = await self._determine_execution_approach(
                code, language, problem_type, input_data, optimization_level
            )
            
            if execution_approach["use_orchestrator"]:
                # Use advanced DSA orchestrator with dynamic agents
                result = await self._execute_with_orchestrator(
                    code, language, problem_type, input_data, execution_approach
                )
            else:
                # Use standard language coordinator
                result = await self._execute_with_language_coordinator(
                    code, language, execution_approach
                )
            
            # Add DSA coordinator metadata
            end_time = datetime.now()
            execution_duration = (end_time - start_time).total_seconds()
            
            result["dsa_coordinator"] = {
                "execution_approach": execution_approach,
                "problem_type": problem_type,
                "language": language,
                "optimization_level": optimization_level,
                "total_duration": execution_duration,
                "orchestrator_used": execution_approach["use_orchestrator"],
                "agents_created": result.get("agent_factory_status", {}).get("total_agents", 0),
                "timestamp": end_time.isoformat()
            }
            
            return result
            
        except Exception as e:
            return self._create_error_response(f"DSA execution failed: {str(e)}")
    
    async def _determine_execution_approach(self, code: str, language: str, problem_type: str, 
                                          input_data: Any, optimization_level: str) -> Dict[str, Any]:
        """Determine the best execution approach for the DSA problem"""
        
        # Estimate problem complexity
        input_size = self._estimate_input_size(input_data) if input_data else self._estimate_code_complexity(code)
        
        # Determine if we should use the orchestrator
        use_orchestrator = False
        
        if optimization_level == "aggressive":
            use_orchestrator = True
        elif optimization_level == "parallel" and input_size > 10000:
            use_orchestrator = True
        elif optimization_level == "auto":
            # Auto-decide based on problem characteristics
            if input_size > 50000:  # Large input
                use_orchestrator = True
            elif problem_type in ["sorting", "graph", "dp", "tree"] and input_size > 10000:
                use_orchestrator = True
            elif "nested loop" in code.lower() or "for" in code and "for" in code:
                use_orchestrator = True
        
        approach = {
            "use_orchestrator": use_orchestrator,
            "estimated_input_size": input_size,
            "problem_complexity": self._analyze_problem_complexity(code, problem_type),
            "parallel_potential": self._assess_parallel_potential(code, problem_type),
            "optimization_strategy": optimization_level,
            "reason": self._get_approach_reason(use_orchestrator, input_size, problem_type)
        }
        
        print(f"🎯 Execution Approach: {'Orchestrator' if use_orchestrator else 'Standard'}")
        print(f"📊 Estimated Input Size: {input_size}")
        print(f"🔍 Reason: {approach['reason']}")
        
        return approach
    
    async def _execute_with_orchestrator(self, code: str, language: str, problem_type: str, 
                                       input_data: Any, approach: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using the DSA orchestrator with dynamic agent creation"""
        
        print("🚀 Using DSA Orchestrator with Dynamic Agents")
        
        # First, optimize the code if needed
        if approach["optimization_strategy"] in ["auto", "aggressive"]:
            optimization_result = await self.dsa_orchestrator.optimize_for_problem_type(code, problem_type)
            if optimization_result.get("success", False):
                code = optimization_result.get("optimized_code", code)
                print("🔧 Code optimized successfully")
        
        # Execute with orchestrator
        orchestrator_result = await self.dsa_orchestrator.execute_large_dsa_problem(
            code, input_data or [], problem_type
        )
        
        # Also get standard execution for comparison
        standard_result = await self._execute_with_language_coordinator(code, language, approach)
        
        # Combine results
        combined_result = {
            **orchestrator_result,
            "standard_execution": standard_result,
            "execution_method": "DSA Orchestrator with Dynamic Agents",
            "optimization_applied": approach["optimization_strategy"] in ["auto", "aggressive"]
        }
        
        return combined_result
    
    async def _execute_with_language_coordinator(self, code: str, language: str, 
                                               approach: Dict[str, Any]) -> Dict[str, Any]:
        """Execute using standard language coordinator"""
        
        print(f"🔄 Using Standard {language.title()} Coordinator")
        
        if language.lower() == "python":
            result = await self.python_coordinator.execute_code(code, use_pipeline=True)
        elif language.lower() == "java":
            result = await self.java_coordinator.execute_code(code, use_pipeline=True)
        else:
            return self._create_error_response(f"Language {language} not supported")
        
        result["execution_method"] = f"Standard {language.title()} Coordinator"
        return result
    
    def _estimate_input_size(self, input_data: Any) -> int:
        """Estimate the size of input data"""
        if input_data is None:
            return 0
        elif isinstance(input_data, (list, tuple)):
            return len(input_data)
        elif isinstance(input_data, str):
            return len(input_data)
        elif isinstance(input_data, dict):
            return len(str(input_data))
        else:
            return len(str(input_data))
    
    def _estimate_code_complexity(self, code: str) -> int:
        """Estimate code complexity based on structure"""
        lines = len(code.split('\n'))
        nested_loops = code.count('for') * code.count('while')
        return lines * 100 + nested_loops * 1000
    
    def _analyze_problem_complexity(self, code: str, problem_type: str) -> str:
        """Analyze the computational complexity of the problem"""
        if "sort" in code.lower() or problem_type == "sorting":
            return "O(n log n)"
        elif nested_count := (code.count('for') + code.count('while')):
            if nested_count >= 2:
                return "O(n²)" if nested_count == 2 else "O(n³)"
            else:
                return "O(n)"
        elif "binary" in code.lower() or "search" in code.lower():
            return "O(log n)"
        else:
            return "O(n)"
    
    def _assess_parallel_potential(self, code: str, problem_type: str) -> str:
        """Assess how suitable the problem is for parallel processing"""
        if problem_type in ["sorting", "graph", "tree"]:
            return "high"
        elif "independent" in code.lower() or problem_type == "dp":
            return "medium"
        elif "sequential" in code.lower():
            return "low"
        else:
            return "medium"
    
    def _get_approach_reason(self, use_orchestrator: bool, input_size: int, problem_type: str) -> str:
        """Get human-readable reason for the chosen approach"""
        if use_orchestrator:
            if input_size > 50000:
                return f"Large input size ({input_size}) benefits from parallel processing"
            elif problem_type in ["sorting", "graph", "dp", "tree"]:
                return f"{problem_type} problems can be efficiently parallelized"
            else:
                return "Complex algorithm detected, using optimization strategies"
        else:
            return "Standard execution sufficient for this problem size and complexity"
    
    async def get_dsa_statistics(self) -> Dict[str, Any]:
        """Get comprehensive DSA execution statistics"""
        if not self.enabled:
            return {"status": "disabled"}
        
        return {
            "orchestrator_stats": self.dsa_orchestrator.get_orchestrator_stats(),
            "python_coordinator": getattr(self.python_coordinator, 'pipeline_enabled', False),
            "java_coordinator": getattr(self.java_coordinator, 'pipeline_enabled', False),
            "dsa_coordinator_enabled": self.enabled
        }
    
    def _create_fallback_response(self, message: str) -> Dict[str, Any]:
        """Create fallback response when DSA coordinator is unavailable"""
        return {
            "success": False,
            "error": message,
            "execution_method": "Fallback - DSA Coordinator Unavailable",
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "success": False,
            "error": error_message,
            "execution_method": "DSA Coordinator - Error",
            "timestamp": datetime.now().isoformat()
        }

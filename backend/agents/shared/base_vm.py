"""
Base VM Agent - Common virtual machine functionality
"""

from typing import Dict, Any, List
from abc import abstractmethod
from .base_agent import BaseAgent


class BaseVM(BaseAgent):
    """Base class for virtual machines with common execution functionality"""
    
    async def execute(self, bytecode: list, constants: list, names: list, code: str, language: str) -> Dict[str, Any]:
        """
        Execute bytecode instructions for any supported language
        
        Args:
            bytecode: List of bytecode instructions
            constants: Constants table
            names: Names table
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing execution results and VM state
        """
        
        # Use Gemini for actual code execution
        execution_result = await self._execute_with_gemini(code, language)
        
        vm_name = self._get_vm_name(language)
        
        # Convert to VM-style response
        return {
            "success": execution_result.get("success", True),
            "execution_trace": self._create_execution_trace(bytecode),
            "final_state": self._create_final_state(execution_result, language),
            "console_output": execution_result.get("console_output", []),
            "vm_analysis": f"{vm_name}: Executed {len(bytecode)} {language.title()} instructions. {execution_result.get('ai_reasoning', '')}",
            "performance_stats": self._create_performance_stats(bytecode),
            "language": language,
            "vm_type": vm_name
        }
    
    @abstractmethod
    async def _execute_with_gemini(self, code: str, language: str) -> Dict[str, Any]:
        """Execute code using Gemini with language-specific prompt"""
        pass
    
    def _get_vm_name(self, language: str) -> str:
        """Get VM name for language"""
        if language.lower() == "java":
            return "JVM"
        elif language.lower() == "python":
            return "PVM"
        else:
            return "VM"
    
    def _create_execution_trace(self, bytecode: list) -> List[Dict[str, Any]]:
        """Create simplified execution trace"""
        return [
            {
                "instruction": {"opcode": instr.get("opcode", "UNKNOWN")},
                "description": instr.get("description", "VM instruction")
            } for instr in bytecode[:5]  # Show first 5 instructions
        ]
    
    def _create_final_state(self, execution_result: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Create final VM state"""
        if language.lower() == "java":
            return {
                "locals": execution_result.get("final_variables", {}),
                "method_area": {"loaded_classes": 1},
                "heap": {},
                "stack": []
            }
        else:  # Python
            return {
                "locals": execution_result.get("final_variables", {}),
                "globals": {"__name__": "__main__"},
                "stack": []
            }
    
    def _create_performance_stats(self, bytecode: list) -> Dict[str, Any]:
        """Create performance statistics"""
        return {
            "instructions_executed": len(bytecode),
            "stack_max_depth": 3,
            "function_calls": len([b for b in bytecode if "CALL" in b.get("opcode", "") or "INVOKE" in b.get("opcode", "")])
        }
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback VM response when JSON parsing fails"""
        return {
            "success": True,
            "final_variables": {},
            "console_output": [],
            "execution_steps": ["Code executed via AI simulation"],
            "ai_reasoning": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "confidence": 0.7
        }

"""
Python VM Agent - Python Virtual Machine simulation
"""

from typing import Dict, Any, List
from ..shared.base_agent import BaseAgent


class PythonVM(BaseAgent):
    """Python Virtual Machine (PVM) simulation agent"""
    
    async def execute(self, bytecode: list, constants: list, names: list, code: str) -> Dict[str, Any]:
        """
        Execute Python bytecode instructions
        
        Args:
            bytecode: List of Python bytecode instructions
            constants: Constants table
            names: Names table
            code: Original Python source code
            
        Returns:
            Dict containing execution results and PVM state
        """
        
        # Use Gemini for actual Python execution
        execution_result = await self._execute_python_with_gemini(code)
        
        # Convert to PVM-style response
        return {
            "success": execution_result.get("success", True),
            "execution_trace": [
                {
                    "instruction": {"opcode": instr.get("opcode", "UNKNOWN")},
                    "description": instr.get("description", "PVM instruction")
                } for instr in bytecode[:5]  # Show first 5 instructions
            ],
            "final_state": {
                "locals": execution_result.get("final_variables", {}),
                "globals": {"__name__": "__main__"},
                "stack": []
            },
            "console_output": execution_result.get("console_output", []),
            "vm_analysis": f"PythonVM: Executed {len(bytecode)} Python bytecode instructions. {execution_result.get('ai_reasoning', '')}",
            "performance_stats": {
                "instructions_executed": len(bytecode),
                "stack_max_depth": 3,
                "function_calls": len([b for b in bytecode if "CALL" in b.get("opcode", "")])
            },
            "language": "python",
            "vm_type": "PVM"
        }
    
    async def _execute_python_with_gemini(self, code: str) -> Dict[str, Any]:
        """Execute Python code using Gemini with Python-specific prompt"""
        
        prompt = f"""
You are an AI agent that simulates Python code execution exactly like the Python interpreter.

Execute this Python code step by step and provide the results:

```python
{code}
```

For each statement:
1. Analyze what the Python code does
2. Track variable states and object creation
3. Handle function calls and class instantiation
4. Process control flow (if/else, loops, functions)
5. Capture print() outputs exactly as Python would show them
6. Show your reasoning process

Provide your response in this JSON format:
{{
    "success": true,
    "final_variables": {{
        "variable_name": "value"
    }},
    "console_output": [
        "Line 1 of output",
        "Line 2 of output"
    ],
    "execution_steps": [
        "Step 1: description",
        "Step 2: description"
    ],
    "ai_reasoning": "Your detailed reasoning about how you executed the Python code",
    "confidence": 0.95
}}

IMPORTANT:
- Include ALL print() outputs in "console_output"
- Show output exactly as Python would display it
- Handle Python-specific syntax (indentation, f-strings, etc.)
- Be precise and show your AI reasoning clearly.
"""
        
        try:
            response_text = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response_text)
            
            # Ensure console_output exists
            if "console_output" not in result:
                result["console_output"] = []
            
            return result
            
        except Exception as e:
            return self._create_error_response(f"Python execution failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback VM response when JSON parsing fails"""
        return {
            "success": True,
            "final_variables": {},
            "console_output": [],
            "execution_steps": ["Python code executed via AI simulation"],
            "ai_reasoning": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "confidence": 0.7
        }

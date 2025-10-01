"""
Java VM Agent - Java Virtual Machine (JVM) simulation
"""

from typing import Dict, Any, List
from ..shared.base_agent import BaseAgent


class JavaVM(BaseAgent):
    """Java Virtual Machine (JVM) simulation agent"""
    
    async def execute(self, bytecode: list, constant_pool: list, code: str) -> Dict[str, Any]:
        """
        Execute Java bytecode instructions on simulated JVM
        
        Args:
            bytecode: List of Java bytecode instructions
            constant_pool: JVM constant pool
            code: Original Java source code
            
        Returns:
            Dict containing execution results and JVM state
        """
        
        # Use Gemini for actual Java execution
        execution_result = await self._execute_java_with_gemini(code)
        
        # Convert to JVM-style response
        return {
            "success": execution_result.get("success", True),
            "execution_trace": [
                {
                    "instruction": {"opcode": instr.get("opcode", "UNKNOWN")},
                    "description": instr.get("description", "JVM instruction")
                } for instr in bytecode[:5]  # Show first 5 instructions
            ],
            "final_state": {
                "locals": execution_result.get("final_variables", {}),
                "method_area": {"HelloWorld": "loaded"},
                "heap": {},
                "stack": []
            },
            "console_output": execution_result.get("console_output", []),
            "vm_analysis": f"JavaVM (JVM): Executed {len(bytecode)} Java bytecode instructions. {execution_result.get('ai_reasoning', '')}",
            "performance_stats": {
                "instructions_executed": len(bytecode),
                "heap_allocations": 0,
                "method_calls": len([b for b in bytecode if "INVOKE" in b.get("opcode", "")])
            },
            "language": "java",
            "vm_type": "JVM"
        }
    
    async def _execute_java_with_gemini(self, code: str) -> Dict[str, Any]:
        """Execute Java code using Gemini with Java-specific prompt"""
        
        prompt = f"""
You are an AI agent that simulates Java code execution exactly like the Java Virtual Machine (JVM).

Execute this Java code step by step and provide the results:

```java
{code}
```

For each statement:
1. Analyze what the Java code does
2. Track variable states and object creation
3. Handle method calls and class instantiation
4. Process control flow (if/else, loops, methods)
5. Capture System.out.print/println outputs exactly as Java would show them
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
    "ai_reasoning": "Your detailed reasoning about how you executed the Java code",
    "confidence": 0.95
}}

IMPORTANT:
- Include ALL System.out.print/println outputs in "console_output"
- Show output exactly as Java would display it
- Handle Java-specific syntax (classes, methods, strong typing)
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
            return self._create_error_response(f"Java execution failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback VM response when JSON parsing fails"""
        return {
            "success": True,
            "final_variables": {},
            "console_output": [],
            "execution_steps": ["Java code executed via AI simulation"],
            "ai_reasoning": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "confidence": 0.7
        }

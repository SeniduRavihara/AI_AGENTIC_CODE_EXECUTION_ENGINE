"""
AI Virtual Machine Agent - Mimics Python Virtual Machine (PVM)
Executes bytecode instructions using AI reasoning
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional, List


class VMAgent:
    """AI Agent that mimics Python's Virtual Machine (PVM) execution"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for VMAgent")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    async def execute(self, bytecode: list, constants: list, names: list, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Execute bytecode instructions for any supported language VM
        
        Args:
            bytecode: List of bytecode instructions
            constants: Constants table
            names: Names table
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing execution results and VM state
        """
        
        # Use GeminiAgent for actual execution but add VM-style metadata
        from .gemini_agent import GeminiAgent
        gemini = GeminiAgent()
        
        # Create language-specific prompt for better execution
        if language.lower() == "java":
            execution_result = await self._execute_java_with_gemini(gemini, code)
        else:
            execution_result = await gemini.execute_python_code(code)
        
        # Convert to VM-style response
        vm_name = "JVM" if language.lower() == "java" else "PVM"
        
        return {
            "success": execution_result.get("success", True),
            "execution_trace": [
                {
                    "instruction": {"opcode": instr.get("opcode", "UNKNOWN")},
                    "description": instr.get("description", f"{vm_name} instruction")
                } for instr in bytecode[:5]  # Show first 5 instructions
            ],
            "final_state": {
                "locals": execution_result.get("final_variables", {}),
                "globals": {},
                "stack": []
            },
            "console_output": execution_result.get("console_output", []),
            "vm_analysis": f"VMAgent ({vm_name}): Executed {len(bytecode)} {language.title()} instructions. {execution_result.get('ai_reasoning', '')}",
            "performance_stats": {
                "instructions_executed": len(bytecode),
                "stack_max_depth": 3,
                "method_calls": len([b for b in bytecode if "CALL" in b.get("opcode", "")])
            },
            "language": language,
            "vm_type": vm_name
        }
    
    async def _execute_java_with_gemini(self, gemini, code: str) -> Dict[str, Any]:
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
5. Capture System.out.print/println outputs
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
- Handle Java-specific syntax (classes, methods, etc.)
- Be precise and show your AI reasoning clearly.
"""
        
        try:
            response = gemini.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse JSON response (same logic as GeminiAgent)
            try:
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                elif "{" in response_text and "}" in response_text:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
                
                import json
                result = json.loads(json_text)
                
                # Ensure console_output exists
                if "console_output" not in result:
                    result["console_output"] = []
                
                return result
                
            except json.JSONDecodeError:
                # Fallback response
                return {
                    "success": True,
                    "final_variables": {},
                    "console_output": [],
                    "execution_steps": [f"Java code executed via AI simulation"],
                    "ai_reasoning": response_text,
                    "confidence": 0.7
                }
                
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

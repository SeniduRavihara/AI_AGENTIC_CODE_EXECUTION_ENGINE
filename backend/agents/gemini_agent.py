"""
Real AI Agent using Google Gemini
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional


class GeminiAgent:
    """Real AI Agent using Google Gemini for code execution simulation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required. Set it as environment variable.")
        
        # Configure Gemini for AI Studio (not Vertex AI)
        genai.configure(api_key=self.api_key)
        # Use the working model from your backend
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    async def execute_python_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code using AI reasoning
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict with execution results, variables, and AI reasoning
        """
        
        prompt = f"""
You are an AI agent that simulates Python code execution. 

Execute this Python code step by step and provide the results:

```python
{code}
```

For each line of code:
1. Analyze what the code does
2. Track variable changes
3. Evaluate expressions
4. Handle control flow (if/else, loops)
5. Show your reasoning process

Provide your response in this JSON format:
{{
    "success": true,
    "final_variables": {{
        "variable_name": "value"
    }},
    "execution_steps": [
        "Step 1: description",
        "Step 2: description"
    ],
    "ai_reasoning": "Your detailed reasoning about how you executed the code",
    "confidence": 0.95
}}

Be precise and show your AI reasoning clearly.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in markdown
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
                
                result = json.loads(json_text)
                
                # Validate required fields
                if not all(key in result for key in ["success", "final_variables", "ai_reasoning"]):
                    raise ValueError("Invalid response format")
                
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                # Fallback: create a structured response from raw text
                return {
                    "success": True,
                    "final_variables": self._extract_variables_from_text(response_text),
                    "execution_steps": [f"AI executed: {line.strip()}" for line in code.split('\n') if line.strip()],
                    "ai_reasoning": response_text,
                    "confidence": 0.7
                }
                
        except Exception as e:
            return {
                "success": False,
                "final_variables": {},
                "execution_steps": [],
                "ai_reasoning": f"AI execution failed: {str(e)}",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _extract_variables_from_text(self, text: str) -> Dict[str, Any]:
        """Extract variables from AI response text"""
        variables = {}
        
        # Look for common variable patterns
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if '=' in line and any(var in line for var in ['x', 'y', 'z', 'a', 'b', 'c', 'result', 'value']):
                try:
                    if 'x =' in line:
                        value = self._extract_value(line.split('x =')[1].strip())
                        if value != "unknown":
                            variables['x'] = value
                    elif 'y =' in line:
                        value = self._extract_value(line.split('y =')[1].strip())
                        if value != "unknown":
                            variables['y'] = value
                    elif 'z =' in line:
                        value = self._extract_value(line.split('z =')[1].strip())
                        if value != "unknown":
                            variables['z'] = value
                except:
                    pass
        
        return variables
    
    def _extract_value(self, value_str: str) -> Any:
        """Extract and convert value from string"""
        value_str = value_str.strip()
        
        # Remove quotes
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        if value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]
        
        # Convert numbers
        if value_str.isdigit():
            return int(value_str)
        if value_str.replace('.', '').isdigit():
            return float(value_str)
        
        # Convert booleans
        if value_str.lower() in ['true', 'false']:
            return value_str.lower() == 'true'
        
        return value_str

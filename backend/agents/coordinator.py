"""
AI Coordinator Agent for orchestrating code execution
"""

from typing import Dict, Any
from .gemini_agent import GeminiAgent


class CoordinatorAgent:
    """Coordinates AI agents for Python code execution"""
    
    def __init__(self, api_key: str = None):
        self.gemini_agent = GeminiAgent(api_key)
    
    async def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code using AI coordination
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict with execution results
        """
        
        # Use Gemini agent to execute the code
        result = await self.gemini_agent.execute_python_code(code)
        
        # Add coordination metadata
        result["coordinator"] = {
            "agent_used": "GeminiAgent",
            "execution_method": "AI reasoning with Google Gemini",
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

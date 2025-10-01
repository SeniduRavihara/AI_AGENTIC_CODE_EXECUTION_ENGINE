"""
Base Agent - Common functionality for all AI agents
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all AI agents with common Gemini functionality"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for AI agents")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    async def _generate_with_gemini(self, prompt: str) -> str:
        """Generate content using Gemini AI"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from AI with fallback handling"""
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
            
            # Truncate if too long to prevent JSON parsing issues
            if len(json_text) > 50000:  # 50KB limit
                raise ValueError("Response too long for JSON parsing")
            
            return json.loads(json_text)
            
        except (json.JSONDecodeError, ValueError) as e:
            # Return fallback response structure
            return self._create_fallback_response(response_text, str(e))
    
    @abstractmethod
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails"""
        pass
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create a standardized error response"""
        return {
            "success": False,
            "error": error_message,
            "timestamp": "2025-09-28T18:00:00"
        }

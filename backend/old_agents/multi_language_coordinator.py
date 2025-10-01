"""
Multi-Language Coordinator - Routes execution to appropriate language-specific coordinators
"""

from datetime import datetime
from typing import Dict, Any

from .python.python_coordinator import PythonCoordinator
from .java.java_coordinator import JavaCoordinator


class MultiLanguageCoordinator:
    """
    Routes code execution to appropriate language-specific coordinator
    """
    
    def __init__(self):
        """Initialize language-specific coordinators"""
        self.coordinators = {}
        
        try:
            self.coordinators["python"] = PythonCoordinator()
        except Exception as e:
            print(f"⚠️ Python coordinator initialization failed: {e}")
            self.coordinators["python"] = None
        
        try:
            self.coordinators["java"] = JavaCoordinator()
        except Exception as e:
            print(f"⚠️ Java coordinator initialization failed: {e}")
            self.coordinators["java"] = None
        
        print("🌐 Multi-language interpreter coordinator initialized!")
    
    async def execute_code(self, code: str, language: str = "python", use_pipeline: bool = True) -> Dict[str, Any]:
        """
        Execute code using the appropriate language-specific coordinator
        
        Args:
            code: Source code
            language: Programming language (python, java)
            use_pipeline: Whether to use full pipeline or simple execution
            
        Returns:
            Dict with comprehensive execution results
        """
        
        start_time = datetime.now()
        language = language.lower()
        
        # Route to appropriate coordinator
        if language in self.coordinators and self.coordinators[language] is not None:
            print(f"🔄 Routing to {language.title()} coordinator")
            result = await self.coordinators[language].execute_code(code, use_pipeline)
        else:
            # Fallback error response
            result = {
                "success": False,
                "final_variables": {},
                "console_output": [],
                "execution_steps": [],
                "ai_reasoning": f"Language '{language}' is not supported or coordinator failed to initialize",
                "confidence": 0.0,
                "error": f"Unsupported language: {language}"
            }
        
        # Add multi-language coordinator metadata
        end_time = datetime.now()
        execution_duration = (end_time - start_time).total_seconds()
        
        if "coordinator" not in result:
            result["coordinator"] = {}
        
        result["coordinator"]["multi_language_router"] = {
            "requested_language": language,
            "coordinator_available": language in self.coordinators and self.coordinators[language] is not None,
            "total_duration": execution_duration,
            "routing_timestamp": end_time.isoformat()
        }
        
        return result
    
    def get_supported_languages(self) -> Dict[str, bool]:
        """Get list of supported languages and their availability"""
        return {
            language: coordinator is not None 
            for language, coordinator in self.coordinators.items()
        }
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status for all languages"""
        status = {
            "multi_language_coordinator": True,
            "supported_languages": self.get_supported_languages(),
            "language_details": {}
        }
        
        for language, coordinator in self.coordinators.items():
            if coordinator is not None:
                status["language_details"][language] = {
                    "available": True,
                    "pipeline_enabled": getattr(coordinator, 'pipeline_enabled', False)
                }
            else:
                status["language_details"][language] = {
                    "available": False,
                    "pipeline_enabled": False
                }
        
        return status

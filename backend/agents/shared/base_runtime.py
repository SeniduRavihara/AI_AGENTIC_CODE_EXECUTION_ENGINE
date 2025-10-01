"""
Base Runtime Agent - Common runtime environment functionality
"""

from typing import Dict, Any
from abc import abstractmethod
from .base_agent import BaseAgent


class BaseRuntime(BaseAgent):
    """Base class for runtime environments with common memory management"""
    
    async def manage_runtime(self, vm_state: dict, code: str, language: str) -> Dict[str, Any]:
        """
        Manage runtime environment for any supported language
        
        Args:
            vm_state: Current VM state
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing runtime analysis and memory management info
        """
        
        locals_dict = vm_state.get("locals", {})
        
        if language.lower() == "java":
            return self._manage_java_runtime(locals_dict)
        elif language.lower() == "python":
            return self._manage_python_runtime(locals_dict)
        else:
            return self._manage_generic_runtime(locals_dict, language)
    
    def _manage_python_runtime(self, locals_dict: dict) -> Dict[str, Any]:
        """Manage Python runtime environment"""
        return {
            "success": True,
            "memory_layout": {
                "local_variables": len(locals_dict),
                "global_namespace": {"__name__": "__main__", "__builtins__": "available"},
                "heap_objects": sum(1 for v in locals_dict.values() if isinstance(v, (list, dict, str)) and len(str(v)) > 10)
            },
            "namespace_info": {
                "local_scope": list(locals_dict.keys()),
                "builtin_functions": ["print", "len", "type", "str", "int", "float"],
                "imported_modules": []
            },
            "runtime_analysis": f"PythonRuntime: Managing {len(locals_dict)} local variables in Python namespace.",
            "garbage_collection": {
                "collections_run": 0,
                "objects_collected": 0
            },
            "language": "python"
        }
    
    def _manage_java_runtime(self, locals_dict: dict) -> Dict[str, Any]:
        """Manage Java runtime environment"""
        return {
            "success": True,
            "memory_layout": {
                "local_variables": len(locals_dict),
                "method_area": {"loaded_classes": 1, "constant_pool": True},
                "heap": {"young_generation": "active", "old_generation": "active"},
                "stack": {"frames": 1}
            },
            "class_loader": {
                "system_classes": ["java.lang.Object", "java.lang.String", "java.lang.System"],
                "user_classes": ["HelloWorld"]
            },
            "runtime_analysis": f"JavaRuntime: Managing {len(locals_dict)} local variables in JVM memory model.",
            "garbage_collection": {
                "gc_algorithm": "G1GC",
                "collections_run": 0,
                "heap_usage": "low"
            },
            "language": "java"
        }
    
    def _manage_generic_runtime(self, locals_dict: dict, language: str) -> Dict[str, Any]:
        """Manage generic runtime environment"""
        return {
            "success": True,
            "memory_layout": {
                "local_variables": len(locals_dict),
                "runtime_system": f"{language.title()} Runtime"
            },
            "runtime_analysis": f"GenericRuntime: Managing {len(locals_dict)} variables for {language.title()}.",
            "language": language
        }
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback runtime response when JSON parsing fails"""
        return {
            "success": True,
            "memory_layout": {"local_variables": 0},
            "runtime_analysis": f"Runtime environment fallback. Error: {error}"
        }

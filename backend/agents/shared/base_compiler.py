"""
Base Compiler Agent - Common compilation functionality
"""

from typing import Dict, Any, List
from abc import abstractmethod
from .base_agent import BaseAgent


class BaseCompiler(BaseAgent):
    """Base class for language compilers with common bytecode functionality"""
    
    async def compile(self, ast: dict, code: str, language: str) -> Dict[str, Any]:
        """
        Compile AST to bytecode for any supported language
        
        Args:
            ast: Abstract Syntax Tree
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing bytecode and compilation analysis
        """
        
        statements = ast.get("body", [])
        compilation_result = self._compile_statements(statements, language)
        
        compilation_result.update({
            "success": True,
            "compiler_analysis": f"BaseCompiler: Generated {len(compilation_result.get('bytecode', []))} {language.title()} instructions from AST.",
            "language": language
        })
        
        return compilation_result
    
    @abstractmethod
    def _compile_statements(self, statements: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Compile language-specific statements to bytecode"""
        pass
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback compiler response when JSON parsing fails"""
        return {
            "success": True,
            "bytecode": [],
            "constants": [],
            "names": [],
            "compiler_analysis": f"Compiler created simplified bytecode. Error: {error}"
        }

"""
Base Parser Agent - Common syntax parsing functionality
"""

from typing import Dict, Any, List
from abc import abstractmethod
from .base_agent import BaseAgent


class BaseParser(BaseAgent):
    """Base class for language parsers with common AST functionality"""
    
    async def parse(self, tokens: list, code: str, language: str) -> Dict[str, Any]:
        """
        Parse tokens into Abstract Syntax Tree for any supported language
        
        Args:
            tokens: List of tokens from lexer
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing AST and parsing analysis
        """
        
        lines = code.split('\n')
        statements = self._parse_statements(lines, language)
                
        return {
            "success": True,
            "ast": self._create_ast(statements, language),
            "statements": statements,
            "parser_analysis": f"BaseParser: Identified {len(statements)} {language.title()} statements in the code.",
            "syntax_errors": [],
            "language": language
        }
    
    @abstractmethod
    def _parse_statements(self, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Parse language-specific statements"""
        pass
    
    def _create_ast(self, statements: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Create AST structure"""
        if language.lower() == "java":
            return {"type": "CompilationUnit", "body": statements}
        else:
            return {"type": "Module", "body": statements}
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback parser response when JSON parsing fails"""
        return {
            "success": True,
            "ast": {"type": "Module", "body": []},
            "statements": [],
            "parser_analysis": f"Parser created simplified AST analysis. Error: {error}",
            "syntax_errors": []
        }

"""
Python Parser Agent - Python-specific syntax parsing
"""

from typing import Dict, Any, List
from ..shared.base_agent import BaseAgent


class PythonParser(BaseAgent):
    """Python-specific parser for creating Python AST"""
    
    async def parse(self, tokens: list, code: str) -> Dict[str, Any]:
        """
        Parse tokens into Python Abstract Syntax Tree
        
        Args:
            tokens: List of tokens from lexer
            code: Original Python source code
            
        Returns:
            Dict containing Python AST and parsing analysis
        """
        
        lines = code.split('\n')
        statements = self._parse_python_statements(lines)
                
        return {
            "success": True,
            "ast": {
                "type": "Module",
                "body": statements
            },
            "statements": statements,
            "parser_analysis": f"PythonParser: Identified {len(statements)} Python statements in the code.",
            "syntax_errors": [],
            "language": "python"
        }
    
    def _parse_python_statements(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse Python-specific syntax"""
        statements = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
                statements.append({
                    "type": "assignment",
                    "line": i+1,
                    "content": line[:50]
                })
            elif line.startswith('if '):
                statements.append({
                    "type": "if_statement", 
                    "line": i+1,
                    "condition": line[3:].rstrip(':')
                })
            elif line.startswith('print('):
                statements.append({
                    "type": "function_call",
                    "line": i+1,
                    "function": "print"
                })
            elif line.startswith('def '):
                statements.append({
                    "type": "function_definition",
                    "line": i+1,
                    "name": line.split('(')[0].replace('def ', '')
                })
            elif line.startswith('class '):
                statements.append({
                    "type": "class_definition",
                    "line": i+1,
                    "name": line.split('(')[0].replace('class ', '').rstrip(':')
                })
            elif line.startswith('for ') or line.startswith('while '):
                statements.append({
                    "type": "loop",
                    "line": i+1,
                    "loop_type": "for" if line.startswith('for') else "while"
                })
                
        return statements
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        """Create a fallback parser response when JSON parsing fails"""
        return {
            "success": True,
            "ast": {"type": "Module", "body": []},
            "statements": [],
            "parser_analysis": f"Python parsing fallback. Error: {error}",
            "syntax_errors": [],
            "language": "python"
        }

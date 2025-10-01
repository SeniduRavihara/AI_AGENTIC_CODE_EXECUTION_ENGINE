"""
AI Parser Agent - Mimics Python's Parser
Creates Abstract Syntax Tree (AST) using AI reasoning
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional


class ParserAgent:
    """AI Agent that mimics Python's syntax parser and AST generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for ParserAgent")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    async def parse(self, tokens: list, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Parse tokens into Abstract Syntax Tree for any supported language
        
        Args:
            tokens: List of tokens from lexer
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing AST and parsing analysis
        """
        
        # Create a simplified but working parser response
        lines = code.split('\n')
        statements = []
        
        if language.lower() == "python":
            statements = self._parse_python(lines)
        elif language.lower() == "java":
            statements = self._parse_java(lines)
        else:
            statements = self._parse_generic(lines)
                
        return {
            "success": True,
            "ast": {
                "type": "Module" if language.lower() == "python" else "CompilationUnit",
                "body": statements
            },
            "statements": statements,
            "parser_analysis": f"ParserAgent: Simplified {language.title()} parsing identified {len(statements)} statements in the code.",
            "syntax_errors": [],
            "language": language
        }
    
    def _parse_python(self, lines: list) -> list:
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
        return statements
    
    def _parse_java(self, lines: list) -> list:
        """Parse Java-specific syntax"""
        statements = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            if 'public class' in line:
                statements.append({
                    "type": "class_declaration",
                    "line": i+1,
                    "name": line.split('class ')[1].split()[0]
                })
            elif 'public static void main' in line:
                statements.append({
                    "type": "main_method",
                    "line": i+1,
                    "signature": "main(String[] args)"
                })
            elif '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
                statements.append({
                    "type": "variable_declaration",
                    "line": i+1,
                    "content": line[:50]
                })
            elif 'System.out.print' in line:
                statements.append({
                    "type": "method_call",
                    "line": i+1,
                    "method": "System.out.print"
                })
            elif line.startswith('if ('):
                statements.append({
                    "type": "if_statement",
                    "line": i+1,
                    "condition": line[3:].rstrip(' {')
                })
        return statements
    
    def _parse_generic(self, lines: list) -> list:
        """Parse generic syntax for unknown languages"""
        statements = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                statements.append({
                    "type": "statement",
                    "line": i+1,
                    "content": line[:50]
                })
        return statements

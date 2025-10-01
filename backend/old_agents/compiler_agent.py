"""
AI Compiler Agent - Mimics Python's Bytecode Compiler
Converts AST to Python bytecode instructions using AI reasoning
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Any, Optional


class CompilerAgent:
    """AI Agent that mimics Python's bytecode compiler"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for CompilerAgent")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    async def compile(self, ast: dict, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Compile AST to bytecode/intermediate code for any supported language
        
        Args:
            ast: Abstract Syntax Tree from parser
            code: Original source code
            language: Programming language
            
        Returns:
            Dict containing bytecode and compilation analysis
        """
        
        # Create simplified bytecode from AST statements
        if language.lower() == "python":
            compilation_result = self._compile_python(ast)
        elif language.lower() == "java":
            compilation_result = self._compile_java(ast)
        else:
            compilation_result = self._compile_generic(ast)
        
        compilation_result.update({
            "success": True,
            "compiler_analysis": f"CompilerAgent: Generated {len(compilation_result.get('bytecode', []))} {language.title()} instructions from AST.",
            "language": language
        })
        
        return compilation_result
    
    def _compile_python(self, ast: dict) -> dict:
        """Generate Python bytecode"""
        bytecode = []
        names = []
        constants = []
        
        for stmt in ast.get("body", []):
            if stmt.get("type") == "assignment":
                bytecode.append({
                    "opcode": "LOAD_CONST",
                    "line": stmt.get("line", 1),
                    "description": "Load value for assignment"
                })
                bytecode.append({
                    "opcode": "STORE_NAME", 
                    "line": stmt.get("line", 1),
                    "description": "Store in variable"
                })
            elif stmt.get("type") == "function_call":
                bytecode.append({
                    "opcode": "CALL_FUNCTION",
                    "line": stmt.get("line", 1),
                    "description": f"Call {stmt.get('function', 'function')}"
                })
                
        return {
            "bytecode": bytecode,
            "constants": constants,
            "names": names,
            "optimizations": []
        }
    
    def _compile_java(self, ast: dict) -> dict:
        """Generate Java bytecode (JVM instructions)"""
        bytecode = []
        constant_pool = []
        
        for stmt in ast.get("body", []):
            if stmt.get("type") == "class_declaration":
                bytecode.append({
                    "opcode": "CLASS_DECLARE",
                    "line": stmt.get("line", 1),
                    "description": f"Declare class {stmt.get('name', 'Unknown')}"
                })
            elif stmt.get("type") == "variable_declaration":
                bytecode.append({
                    "opcode": "ISTORE",  # Integer store
                    "line": stmt.get("line", 1),
                    "description": "Store value in local variable"
                })
            elif stmt.get("type") == "method_call":
                if "System.out.print" in stmt.get("method", ""):
                    bytecode.append({
                        "opcode": "INVOKEVIRTUAL",
                        "line": stmt.get("line", 1),
                        "description": "Invoke System.out.println"
                    })
            elif stmt.get("type") == "main_method":
                bytecode.append({
                    "opcode": "METHOD_ENTRY",
                    "line": stmt.get("line", 1),
                    "description": "Enter main method"
                })
                
        return {
            "bytecode": bytecode,
            "constant_pool": constant_pool,
            "class_file": True,
            "optimizations": []
        }
    
    def _compile_generic(self, ast: dict) -> dict:
        """Generate generic intermediate code"""
        bytecode = []
        
        for i, stmt in enumerate(ast.get("body", [])):
            bytecode.append({
                "opcode": "EXECUTE",
                "line": stmt.get("line", i+1),
                "description": f"Execute {stmt.get('type', 'statement')}"
            })
            
        return {
            "bytecode": bytecode,
            "constants": [],
            "optimizations": []
        }

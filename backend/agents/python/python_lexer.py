"""
Python Lexer Agent - Python-specific lexical analysis
"""

from typing import List
from ..shared.base_lexer import BaseLexer


class PythonLexer(BaseLexer):
    """Python-specific lexer for tokenizing Python code"""
    
    def _identify_language_features(self, code: str, language: str) -> List[str]:
        """Identify Python-specific features in the code"""
        features = []
        
        if "def " in code:
            features.append("function_definition")
        if "class " in code:
            features.append("class_definition")
        if "import " in code:
            features.append("imports")
        if "if " in code:
            features.append("conditionals")
        if "for " in code or "while " in code:
            features.append("loops")
        if "print(" in code:
            features.append("print_statements")
        if "lambda" in code:
            features.append("lambda_functions")
        if "with " in code:
            features.append("context_managers")
        if "try:" in code:
            features.append("exception_handling")
        if "yield" in code:
            features.append("generators")
        if "@" in code:
            features.append("decorators")
        if "f\"" in code or "f'" in code:
            features.append("f_strings")
            
        return features

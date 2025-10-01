"""
Java Lexer Agent - Java-specific lexical analysis
"""

from typing import List
from ..shared.base_lexer import BaseLexer


class JavaLexer(BaseLexer):
    """Java-specific lexer for tokenizing Java code"""
    
    def _identify_language_features(self, code: str, language: str) -> List[str]:
        """Identify Java-specific features in the code"""
        features = []
        
        if "public class" in code:
            features.append("class_declaration")
        if "public static void main" in code:
            features.append("main_method")
        if "System.out.print" in code:
            features.append("console_output")
        if "import " in code:
            features.append("imports")
        if "new " in code:
            features.append("object_creation")
        if "if (" in code:
            features.append("conditional_statements")
        if "for (" in code or "while (" in code:
            features.append("loops")
        if "try {" in code:
            features.append("exception_handling")
        if "interface " in code:
            features.append("interfaces")
        if "extends " in code:
            features.append("inheritance")
        if "implements " in code:
            features.append("interface_implementation")
        if "@" in code and not code.count("@") == code.count("@Override"):
            features.append("annotations")
        if "synchronized" in code:
            features.append("thread_synchronization")
        if "final " in code:
            features.append("final_variables")
        if "static " in code:
            features.append("static_members")
        if "private " in code or "protected " in code or "public " in code:
            features.append("access_modifiers")
            
        return features

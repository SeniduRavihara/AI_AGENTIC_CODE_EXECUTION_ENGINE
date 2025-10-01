"""
Java Parser Agent - Java-specific syntax parsing
"""

from typing import Dict, Any, List
from ..shared.base_parser import BaseParser


class JavaParser(BaseParser):
    """Java-specific parser for creating Java AST"""
    
    def _parse_statements(self, lines: List[str], language: str) -> List[Dict[str, Any]]:
        """Parse Java-specific syntax"""
        statements = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('/*'):
                continue
                
            if "public class" in line:
                class_name = line.split("class")[1].split("{")[0].strip()
                statements.append({
                    "type": "class_declaration",
                    "line": i+1,
                    "name": class_name
                })
            elif "public static void main" in line:
                statements.append({
                    "type": "main_method",
                    "line": i+1,
                    "signature": "main(String[] args)"
                })
            elif "System.out.print" in line:
                statements.append({
                    "type": "print_statement",
                    "line": i+1,
                    "method": "System.out.println" if "println" in line else "System.out.print"
                })
            elif "=" in line and not any(op in line for op in ["==", "!=", ">=", "<="]):
                statements.append({
                    "type": "variable_assignment",
                    "line": i+1,
                    "content": line[:50]
                })
            elif "if (" in line:
                condition = line[line.find("(")+1:line.rfind(")")]
                statements.append({
                    "type": "if_statement",
                    "line": i+1,
                    "condition": condition
                })
            elif "for (" in line:
                statements.append({
                    "type": "for_loop",
                    "line": i+1,
                    "loop_type": "for"
                })
            elif "while (" in line:
                statements.append({
                    "type": "while_loop",
                    "line": i+1,
                    "loop_type": "while"
                })
                
        return statements

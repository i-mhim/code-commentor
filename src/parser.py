from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List


class NotPythonCodeError(Exception):
    """Raised when a file does not contain valid Python code."""


class CodeExtractor(ast.NodeVisitor):
    """AST visitor that extracts function definitions and bodies."""

    def __init__(self, source_code: str) -> None:
        """Initialize the extractor with source code text."""
        self.source_code = source_code.splitlines()
        self.functions: List[Dict[str, object]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Triggered every time the parser finds a function."""
        start_line = node.lineno - 1
        end_line = node.end_lineno
        func_body = "\n".join(self.source_code[start_line:end_line])

        self.functions.append(
            {
                "name": node.name,
                "body": func_body,
                "has_docstring": ast.get_docstring(node) is not None,
            }
        )
        self.generic_visit(node)

def get_functions_from_file(file_path: Path) -> List[Dict[str, object]]:
    """Return function metadata extracted from a Python source file."""
    with file_path.open("r", encoding="utf-8") as f:
        code = f.read()

    try:
        ast.parse(code)
    except SyntaxError as exc:
        raise NotPythonCodeError(
            "File does not contain valid Python code."
        ) from exc

    extractor = CodeExtractor(code)
    extractor.visit(ast.parse(code))
    return extractor.functions


if __name__ == "__main__":
    funcs = get_functions_from_file(Path("tests/sample_messy_code.py"))
    for f in funcs:
        print(f"Found function: {f['name']} | Docstring exists: {f['has_docstring']}")
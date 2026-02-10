import ast
import inspect

class CodeExtractor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code.splitlines()
        self.functions = []

    def visit_FunctionDef(self, node):
        """Triggered every time the parser finds a function."""
        # Extract the specific lines of code for this function
        start_line = node.lineno - 1
        end_line = node.end_lineno
        func_body = "\n".join(self.source_code[start_line:end_line])

        self.functions.append({
            "name": node.name,
            "body": func_body,
            "has_docstring": ast.get_docstring(node) is not None
        })
        self.generic_visit(node)

def get_functions_from_file(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    extractor = CodeExtractor(code)
    extractor.visit(tree)
    return extractor.functions

# Quick test
if __name__ == "__main__":
    funcs = get_functions_from_file("tests/sample_messy_code.py")
    for f in funcs:
        print(f"Found function: {f['name']} | Docstring exists: {f['has_docstring']}")
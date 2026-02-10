import ast

class DocstringInjector(ast.NodeTransformer):
    def __init__(self, documentation_map):
        """
        documentation_map: A dictionary where 
        key = function name, value = AI docstring
        """
        self.doc_map = documentation_map

    def visit_FunctionDef(self, node):
        # Check if we have a docstring for this function
        if node.name in self.doc_map:
            new_docstring = self.doc_map[node.name]
            # Create a constant string node for the docstring
            doc_node = ast.Expr(value=ast.Constant(value=new_docstring))
            
            # If function has no docstring, insert it at the beginning
            if not ast.get_docstring(node):
                node.body.insert(0, doc_node)
        
        return node

def apply_docs_to_file(file_path, doc_map):
    with open(file_path, "r") as f:
        source = f.read()
    
    tree = ast.parse(source)
    transformer = DocstringInjector(doc_map)
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    
    return ast.unparse(new_tree)
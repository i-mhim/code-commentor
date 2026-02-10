from parser import get_functions_from_file
from generator import DocGenerator
import pathlib

def main():
    # 1. Initialize our AI engine
    gen = DocGenerator(model_name="llama3")
    
    # 2. Pick a file to document (make sure this file exists in /tests)
    target_file = "tests/sample_messy_code.py"
    print(f"🔍 Analyzing {target_file}...")
    
    # 3. Extract the "messy" functions
    functions = get_functions_from_file(target_file)
    
    readme_content = f"# Documentation for {target_file}\n\n"
    readme_content += "## ⚙️ Function Overview\n\n"

    # 4. Loop through functions and get AI summaries
    for func in functions:
        print(f"🤖 Generating documentation for: {func['name']}...")
        
        # We send the raw code 'body' to Llama 3
        ai_doc = gen.generate_docstring(func['body'])
        
        # Append to our README string
        readme_content += f"### `def {func['name']}`\n"
        readme_content += f"{ai_doc}\n\n"
        readme_content += "```python\n"
        readme_content += f"{func['body']}\n"
        readme_content += "```\n\n---\n\n"

    # 5. Save the final README
    output_path = pathlib.Path("output/README.md")
    output_path.parent.mkdir(exist_ok=True) # Create folder if it doesn't exist
    
    with open(output_path, "w") as f:
        f.write(readme_content)
    
    print(f"Success! Documentation saved to {output_path}")

if __name__ == "__main__":
    main()
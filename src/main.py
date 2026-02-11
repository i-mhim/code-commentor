import pathlib
from parser import get_functions_from_file
from generator import DocGenerator

def main():
    gen = DocGenerator(model_name="llama3")
    test_folder = pathlib.Path("tests")
    
    # 1. Iterate through every .py file in the tests directory
    for file_path in test_folder.glob("*.py"):
        print(f"🔍 Analyzing: {file_path.name}...")
        
        # 2. INITIALIZE readme_content here! 
        # This ensures each file gets its own clean documentation.
        readme_content = f"# Documentation for {file_path.name}\n\n"
        readme_content += "## ⚙️ Function Overview\n\n"
        
        # 3. Extract functions from the current file
        functions = get_functions_from_file(file_path)
        
        if not functions:
            print(f"⚠️ No functions found in {file_path.name}")
            continue

        # 4. Loop through functions and build the content
        for func in functions:
            print(f"  🤖 Documenting: {func['name']}...")
            ai_doc = gen.generate_docstring(func['body'])
            
            readme_content += f"### `def {func['name']}`\n"
            readme_content += f"{ai_doc}\n\n"
            readme_content += "```python\n"
            readme_content += f"{func['body']}\n"
            readme_content += "```\n\n---\n\n"

        # 5. Save the specific README for this file
        output_path = pathlib.Path("output") / f"README_{file_path.stem}.md"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(readme_content)
            
        print(f"✅ Created: {output_path.name}")

if __name__ == "__main__":
    main()``
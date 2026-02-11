import pathlib
from parser import get_functions_from_file
from generator import DocGenerator

def main():
    gen = DocGenerator(model_name="llama3")
    
    # 1. Target the entire folder instead of one file
    test_folder = pathlib.Path("tests")
    
    # 2. Loop through every .py file in that folder
    for file_path in test_folder.glob("*.py"):
        print(f"🔍 Processing: {file_path.name}")
        
        functions = get_functions_from_file(file_path)
        
        # ... (rest of your generation logic) ...
        
        # Save each README with a unique name
        output_name = f"README_{file_path.stem}.md"
        output_path = pathlib.Path("output") / output_name
        
        with open(output_path, "w") as f:
            f.write(readme_content)
            
    print("✅ All files documented!")
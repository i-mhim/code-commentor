import argparse
import pathlib
from .parser import get_functions_from_file
from .generator import DocGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI-powered docstrings for Python files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Python file or directory to analyze (defaults to ./tests).",
    )
    args = parser.parse_args()

    gen = DocGenerator(model_name="llama3")

    # Determine target path
    target = pathlib.Path(args.path) if args.path else pathlib.Path("tests")

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = list(target.glob("*.py"))
    else:
        print(f"❌ Path not found: {target}")
        return

    if not files:
        print(f"⚠️ No .py files found in {target}")
        return

    # Iterate through each selected .py file
    for file_path in files:
        print(f"🔍 Analyzing: {file_path}...")

        readme_content = f"# Documentation for {file_path.name}\n\n"
        readme_content += "## ⚙️ Function Overview\n\n"

        functions = get_functions_from_file(file_path)

        if not functions:
            print(f"⚠️ No functions found in {file_path.name}")
            continue

        for func in functions:
            print(f"  🤖 Documenting: {func['name']}...")
            ai_doc = gen.generate_docstring(func["body"])

            readme_content += f"### `def {func['name']}`\n"
            readme_content += f"{ai_doc}\n\n"
            readme_content += "```python\n"
            readme_content += f"{func['body']}\n"
            readme_content += "```\n\n---\n\n"

        output_path = pathlib.Path("output") / f"README_{file_path.stem}.md"
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "w") as f:
            f.write(readme_content)

        print(f"✅ Created: {output_path.name}")

if __name__ == "__main__":
    main()
import argparse
import pathlib
from typing import List

from .generator import DocGenerator
from .language_detector import LanguageDetector, LanguageLabel
from .parser import NotPythonCodeError, get_functions_from_file


def looks_like_code(text: str) -> bool:
    """Heuristic check to see if input resembles source code."""
    code_markers = [
        "def ",
        "class ",
        "import ",
        "#include",
        "public ",
        "function ",
        "=>",
        ";",
        "{",
        "}",
    ]
    return any(marker in text for marker in code_markers)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate AI-powered docstrings for source files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to analyze (defaults to ./tests).",
    )
    args = parser.parse_args()

    gen = DocGenerator(model_name="llama3")
    detector = LanguageDetector()

    # Determine target path
    target = pathlib.Path(args.path) if args.path else pathlib.Path("tests")

    if target.is_file():
        files: List[pathlib.Path] = [target]
    elif target.is_dir():
        files = list(target.glob("*"))
    else:
        print(f"❌ Path not found: {target}")
        return

    if not files:
        print(f"⚠️ No files found in {target}")
        return

    # Iterate through each selected file
    for file_path in files:
        print(f"🔍 Analyzing: {file_path}...")

        try:
            raw_text = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"❌ Could not read {file_path}: {exc}")
            continue

        if not looks_like_code(raw_text):
            print(
                f"⚠️ {file_path.name} does not appear to contain source code "
                "from any programming language. Skipping."
            )
            continue

        language: LanguageLabel = detector.detect_language(raw_text)

        if language in ("not_code", "unknown"):
            print(
                f"⚠️ {file_path.name} is not recognized as source code. Skipping."
            )
            continue

        if language != "python":
            print(
                f"⚠️ {file_path.name} detected as {language}, "
                "but currently only Python files are supported. Skipping."
            )
            continue

        readme_content = f"# Documentation for {file_path.name}\n\n"
        readme_content += "## ⚙️ Function Overview\n\n"

        try:
            functions = get_functions_from_file(file_path)
        except NotPythonCodeError:
            print(
                f"⚠️ {file_path.name} appears to contain code, but not valid "
                "Python. Currently only Python files are supported."
            )
            continue

        if not functions:
            print(f"⚠️ No functions found in {file_path.name}")
            continue

        for func in functions:
            print(f"  🤖 Documenting: {func['name']}...")
            ai_doc = gen.generate_docstring(func["body"], language=language)

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
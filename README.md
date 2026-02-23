# Docstring Generator Project

This project analyzes Python files and uses a local LLM (via LangChain + Ollama) to generate Google-style docstrings.  
Generated documentation is written to Markdown files under the `output` directory.

## Prerequisites

- **Python**: 3.11 (or compatible 3.10+)
- **Ollama** installed and running locally
  - Model: `llama3` (or adjust `model_name` in `src/generator.py`)
- **Internet access** is not required at runtime once dependencies are installed, but you may need it to install packages.

## Installation

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Make sure your local Ollama server is running and that the `llama3` model is available:

```bash
ollama pull llama3
ollama serve
```

## Running the tool locally

From the project root, with your virtual environment activated:

```bash
python -m src.main
```

The script will:

- Look at all `.py` files in the `tests` directory.
- Extract functions from each file.
- Ask the LLM to generate docstrings for each function.
- Write a Markdown file per input file under `output/`, named `README_<filename>.md`.

## Running with Docker

You can also run the tool inside a container. This is useful for deployment or to avoid polluting your host Python environment.

1. **Build the image**:

```bash
docker build -t docstring-generator .
```

2. **Run the container** (assuming Ollama is running on the host at the default port):

```bash
docker run --rm \
  -v "$(pwd)/tests:/app/tests" \
  -v "$(pwd)/output:/app/output" \
  -p 11434:11434 \
  docstring-generator
```

This:

- Mounts your local `tests` and `output` directories into the container so you can control inputs and see outputs on the host.
- Exposes the default Ollama port so the container can talk to the Ollama server running on the host.

> **Note**: If your Ollama server is not reachable from inside the container by default, you may need additional Docker networking configuration depending on your OS.

## Project structure

- `src/main.py` – CLI entrypoint that scans `tests` and generates documentation.
- `src/parser.py` – Extracts function definitions and bodies from Python source files.
- `src/generator.py` – Uses LangChain + Ollama to generate docstrings from function code.
- `src/formatter.py` – AST transformer that can inject generated docstrings back into code (not used directly by `main` yet).
- `tests/` – Example Python files used as input for documentation generation.
- `output/` – Generated Markdown documentation files.
- `requirements.txt` – Python dependencies.
- `Dockerfile` – Container image definition for deployment.

## Deployment notes

- **Entrypoint**: The default command in the Docker image is `python -m src.main`.
- **Dependencies**: Managed via `requirements.txt`. Rebuild the Docker image after changing dependencies.
- **Ollama**: This project assumes a local Ollama instance with the `llama3` model. If you change the model name or host/port, update `src/generator.py` and/or your Docker networking configuration accordingly.


from __future__ import annotations

from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class DocGenerator:
    """Generates Google-style docstrings for functions using an Ollama model."""

    def __init__(self, model_name: str = "llama3") -> None:
        """Initialize the generator with the main Ollama model."""
        self.llm = ChatOllama(model=model_name, temperature=0.2)
        self.parser = StrOutputParser()

        system_prompt = (
            "You are an expert {language} developer. Analyze the provided function "
            "and write a high-quality, concise Google-style docstring. "
            "Return ONLY the docstring starting and ending with triple quotes."
        )
        user_prompt = "Function Code:\n{code}"

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

        # LCEL chain template; language is bound at call time.
        self._chain = prompt_template | self.llm | self.parser

    def generate_docstring(self, function_code: str, language: str = "python") -> str:
        """Send code to the LLM and return a clean docstring."""
        try:
            return self._chain.invoke(
                {
                    "code": function_code,
                    "language": language.capitalize(),
                }
            )
        except Exception as exc:  # pragma: no cover - defensive
            return f'"""Docstring generation failed: {exc}"""'


if __name__ == "__main__":
    gen = DocGenerator()
    sample_code = "def add(a, b): return a + b"
    print(gen.generate_docstring(sample_code))
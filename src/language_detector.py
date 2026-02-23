from __future__ import annotations

from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


LanguageLabel = Literal[
    "python",
    "javascript",
    "typescript",
    "java",
    "c",
    "cpp",
    "go",
    "rust",
    "php",
    "ruby",
    "shell",
    "not_code",
    "unknown",
]


class LanguageDetector:
    """Detects the primary programming language of a code snippet using a small LLM."""

    def __init__(self, model_name: str = "llama3.2:1b") -> None:
        """Initialize the detector with a lightweight Ollama model."""
        self._llm = ChatOllama(model=model_name, temperature=0.0)
        self._parser = StrOutputParser()

        system_prompt = (
            "You are a strict programming language detector. "
            "You MUST answer with exactly one token from this list:\n"
            "python, javascript, typescript, java, c, cpp, go, rust, php, ruby, shell, not_code.\n"
            "If the text is not source code, respond with 'not_code'. "
            "Do not add any explanations."
        )
        user_prompt = "Code snippet:\n```text\n{code}\n```\nLanguage:"

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

        # LCEL chain
        self._chain = prompt_template | self._llm | self._parser

    def detect_language(self, content: str, max_chars: int = 2000) -> LanguageLabel:
        """Return the detected language label for the given content."""
        snippet = content[:max_chars]

        try:
            raw_result = self._chain.invoke({"code": snippet})
        except Exception as exc:  # pragma: no cover - defensive
            print(f"⚠️ Language detection failed: {exc}")
            return "unknown"

        label = raw_result.strip().lower()

        allowed: set[str] = {
            "python",
            "javascript",
            "typescript",
            "java",
            "c",
            "cpp",
            "go",
            "rust",
            "php",
            "ruby",
            "shell",
            "not_code",
        }

        if label not in allowed:
            return "unknown"

        return label  # type: ignore[return-value]


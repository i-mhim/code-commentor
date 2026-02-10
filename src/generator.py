from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class DocGenerator:
    def __init__(self, model_name="llama3"):
        # Connect to your local Ollama instance
        self.llm = ChatOllama(model=model_name, temperature=0.2)
        self.parser = StrOutputParser()

    def generate_docstring(self, function_code):
        """Sends code to Llama 3 and returns a clean docstring."""
        
        system_prompt = (
            "You are an expert Python developer. Analyze the provided function "
            "and write a high-quality, concise Google-style docstring. "
            "Return ONLY the docstring starting and ending with triple quotes."
        )
        
        user_prompt = "Function Code:\n{code}"

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])

        # Create a simple chain
        chain = prompt_template | self.llm | self.parser
        
        return chain.invoke({"code": function_code})

# Test logic
if __name__ == "__main__":
    gen = DocGenerator()
    sample_code = "def add(a, b): return a + b"
    print(gen.generate_docstring(sample_code))
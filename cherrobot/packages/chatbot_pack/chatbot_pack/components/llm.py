from langchain_groq import ChatGroq

class LLM:
    _instance = None

    def __init__(self):
        # Ensure the singleton instance is created only once
        if LLM._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        
        # Configuración de ChatGroq
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        # Store the singleton instance
        LLM._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LLM()
        return cls._instance.llm

from langchain_groq import ChatGroq

class LLM:
    """
    Singleton class for managing a single instance of the ChatGroq large language model (LLM).
    
    This class ensures only one instance of the LLM is created, which can be accessed
    through the `get_instance` method. It is useful for avoiding repeated model initializations,
    which can be resource-intensive, by keeping a single instance accessible throughout the application.
    
    Attributes:
        _instance (LLM): The singleton instance of this class.
        llm (ChatGroq): The initialized ChatGroq language model with specific configurations.
    """
    
    _instance = None  # Class-level attribute to hold the singleton instance

    def __init__(self):
        """
        Initializes the ChatGroq language model with predefined settings.

        Raises:
            Exception: If an instance of LLM already exists, enforcing the singleton pattern.
        """
        if LLM._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        
        # ChatGroq model configuration
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
        """
        Returns the singleton instance of the ChatGroq language model.
        
        If the instance does not yet exist, it is created upon the first call.
        
        Returns:
            ChatGroq: The single initialized instance of the ChatGroq language model.
        """
        if cls._instance is None:
            cls._instance = LLM()
        return cls._instance.llm


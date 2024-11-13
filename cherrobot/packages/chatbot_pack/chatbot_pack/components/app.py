import os

from .vector_store import VectorStore
from .chain_rag import get_retriever_chain, get_rag_chain
from dotenv import load_dotenv
from .llm import LLM
from .stateful_chain import ConversationalRAGSessionManager

load_dotenv()

class ConversationalRAGChatbot:
    """
    Encapsulates the configuration and initialization of the Conversational RAG Chatbot.
    
    This class manages all components required for the chatbot, including LLM, VectorStore, retriever chain,
    and RAG chain, and provides a single access point to the conversational RAG chain with session management.
    """

    def __init__(self):
        """
        Initializes the ConversationalRAGChatbot with all required components, including:
        - Account credentials
        - Document and web paths for the VectorStore
        - The singleton LLM instance
        - The VectorStore instance
        - The retriever and RAG chains
        """
        # Load account credentials from environment variables
        self.account_id = os.getenv("CF_ACCOUNT_ID")
        self.api_token = os.getenv("CF_API_TOKEN")

        # Document paths for VectorStore
        self.file_path = "packages/chatbot_pack/chatbot_pack/sourceFiles/AIEngineer.pdf"
        self.web_paths = ("https://www.promtior.ai/service", "https://www.promtior.ai/")

        # Initialize the singleton LLM instance
        self.llm = LLM.get_instance()

        # Initialize VectorStore as a singleton with specified file and web paths
        self.vector_store = VectorStore(
            self.file_path, self.web_paths, self.account_id, self.api_token
        ).get_instance(self.file_path, self.web_paths, self.account_id, self.api_token)

        # Configure the retriever chain using the vector store and LLM
        self.retriever = get_retriever_chain(self.vector_store, self.llm)

        # Configure the RAG chain combining the retriever and the LLM for answering queries
        self.rag_chain = get_rag_chain(self.retriever, self.llm)

        # Initialize the session manager for conversational RAG interactions
        self.session_manager = ConversationalRAGSessionManager(self.rag_chain)

    def get_conversational_chain(self):
        """
        Returns the configured conversational RAG chain with session management.
        
        This method provides access to the RAG chain that maintains session context across interactions.
        
        Returns:
            RunnableWithMessageHistory: The conversational RAG chain configured to handle session-based chat interactions.
        """
        return self.session_manager.get_conversational_chain()

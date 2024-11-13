from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

class ConversationalRAGSessionManager:
    """
    Manages conversational sessions for a Retrieval-Augmented Generation (RAG) chatbot. 
    
    This class keeps track of session histories, allowing each user session to maintain 
    its own chat history, which is used to provide contextually relevant answers. 
    It wraps a RAG chain with a message history manager, making it easier to manage 
    multiple chat sessions with persistent histories.
    
    Attributes:
        store (dict): Dictionary to store chat histories for each session.
        conversational_rag_chain (RunnableWithMessageHistory): Configured RAG chain that 
            utilizes session history to generate context-aware responses.
    """

    def __init__(self, rag_chain):
        """
        Initializes the session manager with a specified RAG chain and configures 
        the conversational chain to manage session histories.
        
        Args:
            rag_chain: The RAG chain responsible for answering user queries based 
                       on retrieved documents and contextual question reformulation.
        """
        # Session history store
        self.store = {}

        # Configure the conversational chain with message history
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Retrieves or creates the message history for a given session ID.
        
        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            BaseChatMessageHistory: The chat message history for the session, 
            which will be created if it does not already exist.
        """
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()  # Create a new history if it doesn't exist
        return self.store[session_id]

    def get_conversational_chain(self):
        """
        Returns the configured conversational chain with message history management.
        
        This chain can be used to handle chat interactions in a way that maintains 
        session context across multiple interactions.
        
        Returns:
            RunnableWithMessageHistory: The RAG chain configured to utilize session 
            histories for generating contextually relevant responses.
        """
        return self.conversational_rag_chain


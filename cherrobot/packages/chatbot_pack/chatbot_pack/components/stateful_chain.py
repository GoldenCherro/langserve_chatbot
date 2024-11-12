from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

class ConversationalRAGSessionManager:
    def __init__(self, rag_chain):
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
        """Retrieves or creates the message history for a given session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()  # Create a new history if it doesn't exist
        return self.store[session_id]

    def get_conversational_chain(self):
        """Returns the configured conversational chain."""
        return self.conversational_rag_chain

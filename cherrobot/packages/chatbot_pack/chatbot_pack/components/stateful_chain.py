import os
from dotenv import load_dotenv
from .vector_store import VectorStore
from .chain_rag import get_retriever_chain, get_rag_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_groq import ChatGroq

load_dotenv()

account_id = os.getenv("CF_ACCOUNT_ID")
api_token = os.getenv("CF_API_TOKEN")

file_path = "packages/chatbot_pack/chatbot_pack/sourceFiles/AIEngineer.pdf"
web_paths = ("https://www.promtior.ai/service","https://www.promtior.ai/")
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

vector_store = VectorStore(file_path, web_paths, account_id, api_token).get_vector_store()
retriever = get_retriever_chain(vector_store, llm)
rag_chain = get_rag_chain(retriever, llm)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

from components.vector_store import VectorStore
from components.chain_rag import get_retriever_chain, get_rag_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_ollama import ChatOllama

file_path = "sourceFiles/AIEngineer.pdf"
web_paths = ("https://www.promtior.ai/service","https://www.promtior.ai/")
llm = ChatOllama(model="llama3.1", temperature=0,)

vector_store = VectorStore(file_path, web_paths).get_vector_store()
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

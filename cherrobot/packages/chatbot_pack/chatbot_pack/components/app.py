import os

from .vector_store import VectorStore
from .chain_rag import get_retriever_chain, get_rag_chain
from dotenv import load_dotenv
from .llm import LLM
from .stateful_chain import ConversationalRAGSessionManager

load_dotenv()

account_id = os.getenv("CF_ACCOUNT_ID")
api_token = os.getenv("CF_API_TOKEN")

file_path = "packages/chatbot_pack/chatbot_pack/sourceFiles/AIEngineer.pdf"
web_paths = ("https://www.promtior.ai/service","https://www.promtior.ai/")

llm = LLM().get_instance()
vector_store = VectorStore(file_path, web_paths, account_id, api_token).get_instance(file_path, web_paths, account_id, api_token)
retriever = get_retriever_chain(vector_store, llm)
rag_chain = get_rag_chain(retriever, llm)

rag_chat = ConversationalRAGSessionManager(rag_chain).get_conversational_chain()

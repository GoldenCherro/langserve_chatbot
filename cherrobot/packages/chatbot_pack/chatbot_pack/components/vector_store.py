from typing import Sequence
from .loader import loaded_data
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings.cloudflare_workersai import (
    CloudflareWorkersAIEmbeddings,
)
class VectorStore:
    _instance = None  # Class-level attribute to store the singleton instance

    def __new__(cls, file_path: str, web_paths: Sequence[str], account_id: str, api_token: str):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, file_path: str, web_paths: Sequence[str], account_id: str, api_token: str):
        if not self._initialized:
            self._initialize(file_path, web_paths, account_id, api_token)
            self._initialized = True

    def _initialize(self, file_path: str, web_paths: Sequence[str], account_id: str, api_token: str):
        docs = loaded_data(file_path, web_paths)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        self.vector_store = InMemoryVectorStore.from_documents(
            documents=splits, embedding=CloudflareWorkersAIEmbeddings(
                                            account_id=account_id,
                                            api_token=api_token,
                                            model_name="@cf/baai/bge-small-en-v1.5",
                                        )
        )

    def get_vector_store(self) -> InMemoryVectorStore:
        return self.vector_store

# def get_vector_store(file_path: str, web_paths: Sequence[str]) -> InMemoryVectorStore:
#     docs = loaded_data(file_path, web_paths)
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     splits = text_splitter.split_documents(docs)
#     vector_store = InMemoryVectorStore.from_documents(
#         documents=splits, embedding = OllamaEmbeddings(model="llama3.1",)
#     )
#     return vector_store

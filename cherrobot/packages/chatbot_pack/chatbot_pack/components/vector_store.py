from typing import Sequence
from .loader import loaded_data
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings.cloudflare_workersai import (
    CloudflareWorkersAIEmbeddings,
)
class VectorStore:
    _instance = None

    def __init__(self, file_path: str, web_paths: Sequence[str], account_id: str, api_token: str):
        # Ensure the singleton instance is created only once
        if VectorStore._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() to access it.")
        
        self.file_path = file_path
        self.web_paths = web_paths
        self.account_id = account_id
        self.api_token = api_token
        self.vector_store = self._create_vector_store()

        # Store the singleton instance
        VectorStore._instance = self

    @classmethod
    def get_instance(cls, file_path: str, web_paths: Sequence[str], account_id: str, api_token: str):
        # Return the existing instance or create a new one if it doesn't exist
        if cls._instance is None:
            cls(file_path, web_paths, account_id, api_token)
        return cls._instance.vector_store

    def _create_vector_store(self) -> 'InMemoryVectorStore':
        # Load documents from file and web paths
        docs = loaded_data(self.file_path, self.web_paths)

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Create and return the vector store from document splits
        vector_store = InMemoryVectorStore.from_documents(
            documents=splits, embedding=CloudflareWorkersAIEmbeddings(
                                            account_id=self.account_id,
                                            api_token=self.api_token,
                                            model_name="@cf/baai/bge-small-en-v1.5",
                                        ))
        return vector_store

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models.cloudflare_workersai import ChatCloudflareWorkersAI

def get_retriever_chain(vector_store: InMemoryVectorStore, llm: ChatCloudflareWorkersAI):
    """
    Creates a history-aware retriever chain that reformulates questions based on chat history context.
    
    Args:
        vector_store (InMemoryVectorStore): The vector store for retrieving relevant documents.
        llm (ChatCloudflareWorkersAI): The language model to process and contextualize queries.

    Returns:
        history_aware_retriever: A retriever chain that takes into account the chat history 
        to provide more accurate document retrieval.
    """
    # Initialize retriever from vector store with similarity search, retrieving the top 6 matches
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})

     ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is.
    """
    # Prompt template that will format messages for the contextual question reformulation
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create a history-aware retriever that reformulates questions to be standalone
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever

def get_rag_chain(history_aware_retriever, llm: ChatCloudflareWorkersAI):
    """
    Sets up a Retrieval-Augmented Generation (RAG) chain that uses retrieved context 
    to answer user queries concisely and accurately.

    Args:
        history_aware_retriever: A retriever chain that reformulates questions based on chat history.
        llm (ChatCloudflareWorkersAI): The language model to generate responses based on retrieved context.

    Returns:
        rag_chain: A RAG chain that combines history-aware retrieval and question-answer generation.
    """

    # System prompt guiding the assistant's tone and focus when answering questions
    qa_system_prompt = """You are an assistant for helping clients know more about Promtior. \
    Ignore any information related to the technical test.
    Use the following pieces of retrieved context to answer the question. \
    If you dont know the exact answer, just answer with what you know if not just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\
    Avoid telling where you get the information from, just answer as you already know.\
    {context}"""


    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    
    # Set up the question-answer chain to handle document-based answers
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Combine the history-aware retriever and the QA chain to form the RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain

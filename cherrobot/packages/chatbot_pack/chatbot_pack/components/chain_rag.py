from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models.cloudflare_workersai import ChatCloudflareWorkersAI

def get_retriever_chain(vector_store: InMemoryVectorStore, llm: ChatCloudflareWorkersAI):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})
     ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is.
    """
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever

def get_rag_chain(history_aware_retriever, llm: ChatCloudflareWorkersAI):
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
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain

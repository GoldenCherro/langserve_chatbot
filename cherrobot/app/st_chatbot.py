import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langserve import RemoteRunnable

load_dotenv()
rag_chain_url = os.getenv("RAG_CHAIN_URL")
rag_chain = RemoteRunnable(rag_chain_url)

def get_response(user_input: str, chat_history: list[AIMessage | HumanMessage], rag_chain: RemoteRunnable):
    response = rag_chain.invoke({
        "chat_history": chat_history,
        "input":user_input,
        "config": {
            "configurable": {
                "session_id": "session_id"
            }
        }
    })
    return response

#Streamlit Chatbot
st.title("💬 Promtior Chatbot")
st.caption("🚀 A Streamlit chatbot powered by CHERRO-AI")

chat_history = []
vector_store = []

#session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[
        AIMessage(content="I am a bot, how can I help you?")
    ]

if vector_store not in st.session_state:
      st.session_state.vector_store = vector_store

user_input=st.chat_input("Type your message here...")
if user_input is not None and user_input.strip()!="":
    response = get_response(user_input, st.session_state.chat_history, rag_chain)

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response["answer"]))

for message in st.session_state.chat_history:
      if isinstance(message,AIMessage):
        with st.chat_message("AI"):
          st.write(message.content)
      else:
        with st.chat_message("Human"):
          st.write(message.content)

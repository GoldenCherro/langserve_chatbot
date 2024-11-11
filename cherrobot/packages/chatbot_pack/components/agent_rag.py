from langgraph.prebuilt import create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langgraph.checkpoint.memory import MemorySaver
from langchain import hub
from langchain_ollama import ChatOllama
from components.vector_store import get_vector_store
from langgraph.graph import CompiledGraph

def agent_rag() -> CompiledGraph:
    llm = ChatOllama(model="llama3.1", temperature=0,) 
    file_path = "../../sourceFiles/AIEngineer.pdf"
    web_paths = ("https://www.promtior.ai/service","https://www.promtior.ai/")
    
    vector_store = get_vector_store(file_path, web_paths)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    
    memory = MemorySaver()
    prompt = hub.pull("rlm/rag-prompt")

    tool = create_retriever_tool(
        retriever,
        "promtior_info_retriever",
        "Searches and returns information about Promtior.",
    )
    tools = [tool]

    agent_executor = create_react_agent(llm, tools, checkpointer=memory)

    return agent_executor

# algún día te voy a usar :(


# for event in agent_executor.stream(
#     {"messages": [HumanMessage(content=query)]},
#     config=config,
#     stream_mode="values",
# ):
#     for message in event["messages"]:
#         if isinstance(message,AIMessage):
#             if message.content:
#                 print(message.content.replace("\n", "").strip())

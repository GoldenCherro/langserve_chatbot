# Project Overview

I started by learning about **Retrieval-Augmented Generation (RAG)** models, watching videos, and reading about how they can be used to build chat models. I explored different tools according to the test requirements and found a [LangChain tutorial](https://python.langchain.com/docs/tutorials/qa_chat_history/) on creating RAG and conversational RAG applications, which served as a useful guide. Initially, I wanted to use the version with **agents**, but (spoiler alert) when I tried deploying the app with **LangServe**, I found that agents and LangGraph were not well-supported. Because of this, I shifted to using **chains** to build the RAG model and then created the application around it.

I explored several ideas out of curiosity and implemented almost all of them. While this approach took more time, it gave me a deeper understanding of RAGs. Additionally, implementing multiple versions of various components helped me learn a lot about **containerization, Docker**, and **Python project architecture**. I also used **Jupyter Notebooks** to verify that everything was working correctly at each step.

### Project Structure

From this work, I created two repositories:

1. **Streamlit Application**: This application has a Streamlit front end (not deployed but available for local testing) where the app directly uses the RAG model.
2. **REST API**: A REST API with an endpoint deployed using LangServe and FastAPI.

### Challenges and Solutions

One of my initial ideas was to set up two containers: one for **Ollama** with llama3.2 and another for my application. However, since I didn’t have access to cloud platforms, I used **Railway**, which doesn’t support Docker Compose. This limitation forced me to find another way to deploy this architecture.

The main challenges I encountered included:

- **Working with new libraries and language**: I had mainly worked with these technologies at university, so understanding **Python best practices** and the **architecture** was essential.
- **LangChain**: Familiarizing myself with LangChain's extensive features and backend mechanics.
- **Docker**: Setting up Docker containers, especially for Ollama, was another learning experience.
- **Poetry**: Configuring Poetry for dependency management.

---


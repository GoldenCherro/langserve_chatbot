# langserve_chatbot

This project provides a Retrieval-Augmented Generation (RAG) chatbot, packaged as a Docker container, with a backend server powered by LangChain and a frontend interface built in Streamlit.

The chatbot uses the **Groq** chat model for conversational responses ([Groq Chat Model Documentation](https://python.langchain.com/docs/integrations/chat/groq/)) and the **CloudflareWorkersAI** embeddings generator ([CloudflareWorkersAI Embeddings Documentation](https://python.langchain.com/api_reference/community/embeddings/langchain_community.embeddings.cloudflare_workersai.CloudflareWorkersAIEmbeddings.html)). The system employs an in-memory vector store for embedding storage and a chains-based architecture to streamline query and retrieval workflows.

The backend server handles the RAG process via `langserve` in FastAPI, and the frontend application in Streamlit consumes the server's responses, providing a user-friendly interface for interaction.

## Fine-Tuning Prompts

This project uses custom prompts to fine-tune the LLM's responses, helping it answer user questions effectively while remembering chat history context. Below are the two primary prompts:

1. **Contextualize Question Prompt**: 
   - **Prompt**:
     ```python
     contextualize_q_system_prompt = """Given a chat history and the latest user question \
         which might reference context in the chat history, formulate a standalone question \
         which can be understood without the chat history. Do NOT answer the question, \
         just reformulate it if needed and otherwise return it as is.
         """
     ```
   - **Purpose**: This prompt helps the model reformulate questions into a standalone format, allowing it to maintain coherence in responses even when referring to previous chat history. It prepares the questions so that the assistant can respond accurately without needing to review the entire history each time.

2. **Question-Answering System Prompt**:
   - **Prompt**:
     ```python
     qa_system_prompt = """You are an assistant for helping clients know more about Promtior. \
         Ignore any information related to the technical test.
         Use the following pieces of retrieved context to answer the question. \
         If you dont know the exact answer, just answer with what you know if not just say that you don't know. \
         Use three sentences maximum and keep the answer concise. \
         Avoid telling where you get the information from, just answer as you already know. \
         {context}"""
     ```
   - **Purpose**: This prompt guides the assistant to provide concise, accurate answers about "Promtior," based only on available context. The assistant is trained to respond as if it already knows the information, focusing on concise, three-sentence answers without referencing its information sources. This keeps the interaction natural and clear.

## Prerequisites

1. **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://docs.docker.com/get-docker/).
2. **Docker Compose** (for the two-container setup): Verify it’s installed by running:
   ```bash
   docker-compose --version
   ```

## Getting Started

There are two ways to run this project: with two containers (one for the chatbot app and one for `ollama` as the language model) or with a single container (chatbot only).

### Option 1: Two-Container Setup (Chatbot + `ollama` Model)

This setup includes both the chatbot container and the `ollama` container to leverage the `llama3.2` model.

1. **Prepare the Code**:
   - Update the code to integrate the `ollama` model with the RAG chatbot via LangChain by uncommenting the relevant sections in the code and `entrypoint.sh` file.

2. **Environment Variables**:
   - Ensure your environment variables are correctly set. These are managed within the `docker-compose.yml` file, but you may need to adjust them to suit your setup.

3. **Build and Run**:
   Run the following command to build and start both containers:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - **app**: Host the chatbot backend (FastAPI) on `http://localhost:8000` and the Streamlit frontend on `http://localhost:8501`.
   - **ollama**: Run the `ollama` Docker image, pulling the `llama3.2` model, which is used for embeddings and as the primary LLM for RAG.

### Option 2: Single-Container Setup (Chatbot Only)

To run the chatbot without `ollama` support, follow these steps:

1. **Build the Container**:
   ```bash
   docker build . -t <container_name>
   ```

2. **Run the Container**:
   ```bash
   docker run --env-file .env -p 8000:8000 -p 8501:8501 <container_name>
   ```

   This will start the backend server on `localhost:8000` and the Streamlit frontend on `localhost:8501`.

## How It Works

- **RAG-based Chatbot**: The chatbot uses a RAG setup with:
  - **[Groq Chat Model](https://python.langchain.com/docs/integrations/chat/groq/)**: For generating conversational responses.
  - **[CloudflareWorkersAI Embeddings](https://python.langchain.com/api_reference/community/embeddings/langchain_community.embeddings.cloudflare_workersai.CloudflareWorkersAIEmbeddings.html)**: For creating embeddings, stored in an in-memory vector format.
  - **Chains Architecture**: Facilitates embedding queries, retrieval, and response generation, efficiently managed through LangChain's framework.
- **Backend Server (langserve)**: The backend is built on `langserve` and served via FastAPI, handling requests and RAG processing.
- **Frontend (Streamlit)**: Provides an interactive user interface for consuming and interacting with the chatbot, running on port `8501`.

### Accessing the Server

After starting the containers, you can access the app via:
- **Backend API documentation**: `http://localhost:8000/docs`
- **Streamlit frontend**: `http://localhost:8501`

These endpoints allow you to interact with the chatbot, and in the two-container setup, leverage `llama3.2` for enhanced RAG-based interactions.

## Troubleshooting

- **Docker Installation**: If you encounter issues, ensure Docker and Docker Compose (if using the two-container setup) are installed and running correctly.
- **Ports**: Ensure that ports `8000`, `8501`, and `11434` (for `ollama` in the two-container setup) are available on your machine.
- **Environment Variables**: Double-check the environment variables in `docker-compose.yml` and `.env` (for single-container setup) to ensure proper configuration.

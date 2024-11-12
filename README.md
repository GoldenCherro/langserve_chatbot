
## langserve_chatbot

This project provides a web server hosting a chatbot, packaged as a Docker container, and uses another container with the `ollama` model. The chatbot server is accessible on `localhost:8000` once running, and it leverages the `llama3.2` model to generate embeddings and serve as the language model (LLM) for retrieval-augmented generation (RAG).

## Prerequisites

1. **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Docker Compose should be included with your Docker installation. Verify by running:
   ```bash
   docker-compose --version
   ```
## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine.
   ```bash
   git clone https://github.com/GoldenCherro/langserve_chatbot.git
   cd <your_new_chatbot>
   ```

2. **Run the Project**: Use Docker Compose to build and run the containers. The command below will automatically build the images if necessary, pull the `llama3.2` model for `ollama`, and start the services.
   ```bash
   cd langserve_chatbot/cherrobot && docker-compose up --build
   ```

   This command creates two containers:
   - **app**: Hosts the chatbot package and serves the web interface on `http://localhost:8000`.
   - **ollama**: Runs the `ollama` Docker image, used for generating embeddings and as the main LLM for RAG tasks on `http://ollama:11434/`.

### How It Works

1. **app**: This container contains the chatbot in a Python package and runs a web server.
2. **ollama**: The `ollama` container pulls and uses the `llama3.2` model. This model is essential for generating embeddings and functions as the LLM for retrieval-augmented generation.

### Important Notes

- Before the server starts, the `llama3.2` model is automatically pulled in the `ollama` container to ensure it’s available for the chatbot.
- The chatbot is configured to communicate with the `ollama` container.

### Troubleshooting

- **Docker Installation**: If you encounter issues, make sure Docker and Docker Compose are installed and running correctly.
- **Ports**: Ensure `port 8000` is free on your machine as the server will listen on this port by default.

## Accessing the Server

Once everything is up and running, you can access the web server docs at:
```
http://localhost:8000/docs
```

This will allow you to interact with the chatbot powered by `llama3.2` and served by the retrieval-augmented generation (RAG) framework.



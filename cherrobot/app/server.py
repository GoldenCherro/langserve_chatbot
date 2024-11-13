import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from chatbot_pack.components.app import ConversationalRAGChatbot

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

rag_chat = ConversationalRAGChatbot().get_conversational_chain()

add_routes(app, rag_chat)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

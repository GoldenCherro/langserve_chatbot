import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from chatbot_pack.components.stateful_chain import conversational_rag_chain  # Make sure to replace 'your_module' with the actual module name

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, conversational_rag_chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

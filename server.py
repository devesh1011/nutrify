from fastapi import FastAPI
from langserve import add_routes, RemoteRunnable
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Nutrify API",
    description="An API for analyzing food ingredients using LangChain and OpenAI",
    version="1.0.0",
)

# router
app.include_router(router, prefix="/api/v1")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangServe routes
runnable = RemoteRunnable("http://localhost:8080")
add_routes(app, runnable)

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
from fastapi import FastAPI
from langserve import add_routes, RemoteRunnable
from routes.ingredient_routes import router
from fastapi_cors import CORS

app = FastAPI(
    title="Nutrify API",
    description="An API for analyzing food ingredients using LangChain and OpenAI",
    version="1.0.0",
)

# Include the router
app.include_router(router, prefix="/api/v1")

# Add CORS middleware
app.add_middleware(
    CORS,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangServe routes
runnable = RemoteRunnable("http://localhost:8080")
add_routes(app, runnable)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)

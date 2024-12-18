from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.main import main

app = FastAPI(
    title="Nutrify API",
    description="An API for analyzing food ingredients using LangChain and OpenAI",
    version="1.0.0",
)


class IngredientRequest(BaseModel):
    ingredients: str


@app.get("/", summary="Home Route")
def home():
    return "Hello World!"


@app.post("/analyze", summary="Analyze food ingredients")
async def analyze_ingredients(request: IngredientRequest):
    try:
        response = main(request.ingredients)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)

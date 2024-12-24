from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.main import main
import json

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
        content = main(request.ingredients)
        try:
            # Strip unwanted characters like ```json or ```
            content_json = json.loads(content.strip("```json").strip("```"))
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500, detail=f"Invalid JSON format in response: {str(e)}"
            )

        return content_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)

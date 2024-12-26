from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.main import main
import json
from PIL import Image
import easyocr

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


@app.post("/upload", summary="Image upload route", tags=["Image Upload"])
async def handle_uploads(file: UploadFile = File(...)):
    """
    Handles image uploads for OCR processing. Extracts text from the image and returns it.
    """
    try:
        # Verify uploaded file is an image
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only JPEG and PNG are supported.",
            )

        # Load the uploaded image
        image = Image.open(file.file)

        reader = easyocr.Reader(["en"], gpu=False)
        result = reader.readtext(image)

        ingredients = [item[1] for item in result]

        return analyze_ingredients("".join(ingredients))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/analyze", summary="Analyze food ingredients")
async def analyze_ingredients(ingredients: IngredientRequest):
    try:
        content = main(ingredients)
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

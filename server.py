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


# @app.post("/upload", summary="Image upload route")
# def handle_uploads(file: UploadFile = File(...)):
#     """Handles image uploads for OCR processing. Extracts text from the image and returns it."""

#     try:
#         if file.content_type not in ["image/jpeg", "image/png"]:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid file type. Only JPEG and PNG are supported.",
#             )
#         image = Image.open(file.file)

#         extracted_text = pytesseract.image_to_string(image)

#         return JSONResponse(content={"text": extracted_text})

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


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

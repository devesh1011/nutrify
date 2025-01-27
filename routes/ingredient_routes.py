from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from PIL import Image
import easyocr
import json
from app.main import main

router = APIRouter()

class IngredientRequest(BaseModel):
    ingredients: str

@router.get("/", summary="Home Route")
def home():
    return "Hello World!"

@router.post("/upload", summary="Image upload route", tags=["Image Upload"])
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

        # Initialize easyocr with explicit model storage
        import os
        os.environ['EASYOCR_MODULE_PATH'] = '/tmp/easyocr'
        reader = easyocr.Reader(['en'], 
                              gpu=False,
                              download_enabled=True,
                              model_storage_directory='/tmp/easyocr')
        
        # Create a temporary file to store the image
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file.flush()
            
            # Process the image
            result = reader.readtext(temp_file.name)
            
        # Clean up
        os.unlink(temp_file.name)
        
        ingredients = [item[1] for item in result]
        joined_ingredients = " ".join(ingredients)
        request = IngredientRequest(ingredients=joined_ingredients)
        return await analyze_ingredients(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/analyze", summary="Analyze food ingredients")
async def analyze_ingredients(ingredients: IngredientRequest):
    try:
        content = main(ingredients.ingredients)
        content_json = json.loads(content.strip("```json").strip("```"))
        return content_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
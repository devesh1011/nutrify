from fastapi import APIRouter, File, HTTPException, UploadFile
from app.main import main
from dotenv import load_dotenv
from utils import IngredientRequest, process_image, refine_extracted_text

load_dotenv()

router = APIRouter()


@router.get("/", summary="Home Route")
def home():
    return "Hello World!"


@router.post("/upload", summary="Image upload route", tags=["Image Upload"])
async def handle_uploads(file: UploadFile = File(...)):
    """
    Handles image uploads for OCR processing. Extracts text from the image and returns it.
    """

    # Process the image and extract text
    extracted_text = await process_image(file)

    refined_data = refine_extracted_text(extracted_text)
    return await analyze_ingredients(refined_data)


@router.post("/analyze", summary="Analyze food ingredients")
async def analyze_ingredients(ingredients: IngredientRequest):
    try:
        content = main(ingredients)
        return content  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

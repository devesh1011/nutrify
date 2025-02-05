from fastapi import APIRouter, File, HTTPException, UploadFile
from app import main
from utils import process_image, refine_extracted_text, clean_text

router = APIRouter()


@router.post("/upload", summary="Image upload route", tags=["Image Upload"])
async def handle_uploads(file: UploadFile = File(...)):
    try:
        extracted_text = await process_image(file)
        refined_data = refine_extracted_text(extracted_text)
        result = main(refined_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
import json
from app.main import main
import base64
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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
        # Save the uploaded file temporarily
        temp_image_path = f"temp_{file.filename}"
        with open(temp_image_path, "wb") as buffer:
            buffer.write(await file.read())

        # Encode the image to base64
        base64_image = encode_image(temp_image_path)

        # Initialize Groq client
        client = Groq(api_key=os.environ["GROQ_API_KEY"])

        # Send the image to the Groq API for text extraction
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all the text from this image.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )

        extracted_text = chat_completion.choices[0].message.content

        os.remove(temp_image_path)

        return await analyze_ingredients(extracted_text)

    except Exception as e:
        # Clean up the temporary file in case of an error
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", summary="Analyze food ingredients")
async def analyze_ingredients(ingredients: IngredientRequest):
    try:
        content = main(ingredients)
        return content  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


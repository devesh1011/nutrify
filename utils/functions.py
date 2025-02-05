from fastapi import UploadFile, HTTPException
from groq import Groq
import os
import base64
from llm.model import get_model
from chains.analysis_chain import create_analysis_chain
from prompts.nutrition_prompt import text_refine_prompt
import json

llm = get_model()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_image(file: UploadFile):
    """
    Processes an uploaded image by extracting text using the Groq API.

    Args:
        file (UploadFile): The uploaded image file.
        prompt (str): The prompt to send to the Groq API for text extraction.
        model (str): The Groq model to use for text extraction.

    Returns:
        str: The extracted text from the image.
    """
    try:
        # Save the uploaded file temporarily
        temp_image_path = f"temp_{file.filename}"
        with open(temp_image_path, "wb") as buffer:
            buffer.write(await file.read())

        # Encode the image to Base64
        base64_image = encode_image(temp_image_path)

        # Initialize Groq client
        groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

        # Send the image to Groq API for text extraction
        chat_completion = groq_client.chat.completions.create(
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

        # Extract the raw text from the response
        extracted_text = chat_completion.choices[0].message.content

        # Clean up the temporary file
        os.remove(temp_image_path)

        return extracted_text

    except Exception as e:
        # Clean up the temporary file in case of an error
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        raise HTTPException(status_code=500, detail=str(e))


def refine_extracted_text(extracted_text):
    llm = get_model()

    chain = create_analysis_chain(text_refine_prompt, llm)
    refined_text = chain.invoke({"text": extracted_text})
    return refined_text


def clean_text(input_text):
    """
    Cleans up the input text by:
    1. Removing '**' markers.
    2. Replacing newline characters ('\n') with commas (',').

    Args:
        input_text (str): The raw text to be cleaned.

    Returns:
        str: The cleaned-up text.
    """
    # Step 1: Remove '**' markers
    cleaned_text = input_text.replace("**", "")

    # Step 2: Replace '\n' with ','
    cleaned_text = cleaned_text.replace("\n", "")
    return cleaned_text


def clean_response(response: str) -> dict:
    """Clean and parse LLM response into JSON"""
    # Remove markdown code blocks
    if "```json" in response:
        response = response.split("```json")[1]
    if "```" in response:
        response = response.split("```")[0]

    # Remove newlines and clean string
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {str(e)}")

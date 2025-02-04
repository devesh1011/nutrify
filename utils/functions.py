from fastapi import UploadFile, HTTPException
from groq import Groq
import os
import base64
import json


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


def clean_json_response(response):
    """
    Cleans up a JSON response by removing markdown code blocks and trailing text.

    Args:
        response (str): The raw response from the LLM.

    Returns:
        str: The cleaned-up JSON string.
    """
    if response.startswith("```json") and response.endswith("```"):
        response = response[7:-4].strip()

    # Step 2: Remove any trailing text after the JSON object
    try:
        # Find the last closing brace of the JSON object
        last_brace_index = response.rindex("}")
        response = response[: last_brace_index + 1]
    except ValueError:
        raise ValueError("Invalid JSON format: Could not find closing brace '}'.")

    # Step 3: Validate that the cleaned response starts with '{' and ends with '}'
    if not response.startswith("{") or not response.endswith("}"):
        raise ValueError(
            "Invalid JSON format: Response must start with '{' and end with '}'."
        )

    return response


def refine_extracted_text(extracted_text):
    """
    Refines the extracted text to separate ingredients and nutritional facts.

    Args:
        extracted_text (str): The raw text extracted from the image.

    Returns:
        dict: A dictionary containing "ingredients" and "nutrition_facts".
    """
    # Define the prompt for refining the text
    prompt = f"""
You are an expert at parsing and organizing unstructured text. The following text contains information extracted from a food product label.
Your task is to:
1. Identify and extract the list of ingredients.
2. Identify and extract the nutritional facts.
3. Return the results in non markdown format.

Here is the extracted text:
{extracted_text}
"""

    # Initialize Groq client
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

    # Send the prompt to the Groq API
    response = groq_client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at parsing and organizing unstructured text.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the refined text from the response
    refined_text = response.choices[0].message.content.strip()

    return refined_text

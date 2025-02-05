import os
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()


def get_model():
    return ChatMistralAI(model_name="mistral-large-latest", temperature=0.1, api_key=os.environ.get("MISTRAL_API_KEY"))

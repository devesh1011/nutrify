import os
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("NVIDIA_API_KEY"))


def get_openai_model():
    return ChatMistralAI(model_name="mistral-large-latest", temperature=0.1)

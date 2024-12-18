import os
from langchain_openai import ChatOpenAI

def get_openai_model():
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2
    )

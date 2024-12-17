from langchain_openai import ChatOpenAI
import os

def get_openai_model():
    """
    Initializes the OpenAI model for use with LangChain.
    :return: ChatOpenAI model instance
    """
    return ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

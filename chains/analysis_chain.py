from langchain_core.output_parsers import StrOutputParser


def create_analysis_chain(prompt, model):
    """
    Creates a LangChain chain for ingredient analysis.
    :param prompt: The main prompt template
    :param model: The OpenAI model instance
    :return: The LangChain chain
    """
    return prompt | model | StrOutputParser()

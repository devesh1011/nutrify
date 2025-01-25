from chains.analysis_chain import create_analysis_chain
from prompts.nutrition_prompt import get_main_prompt
from models.openai_model import get_model


def main(ingredients):
    # Initialize the OpenAI model
    model = get_model()

    # Load the main prompt
    main_prompt = get_main_prompt()

    # Create the chain by combining prompt and model
    chain = create_analysis_chain(main_prompt, model)
    response = chain.invoke({"ingredients": ingredients})

    return response

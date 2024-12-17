from chains.analysis_chain import create_analysis_chain
from prompts.nutrition_prompt import get_main_prompt
from models.openai_model import get_openai_model


def main():
    # Initialize the OpenAI model
    model = get_openai_model()

    # Load the main prompt
    main_prompt = get_main_prompt()

    # Define the ingredients input
    ingredients = "CARBONATED WATER, SUGAR, NATURAL CARAMEL COLOR (CLASS IV), ACIDITY REGULATORS (PHOSPHORIC ACID), KOLA CONCENTRATE, CAFFEINE. CONTAINS CAFFEINE 24 MG/SERVING. MAXIMUM CONSUMPTION 150 MG/DAY"

    # Create the chain by combining prompt and model
    chain = create_analysis_chain(main_prompt, model)
    response = chain.invoke({"ingredients": ingredients})

    # Print the response
    print(response)

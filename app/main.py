from chains.analysis_chain import create_analysis_chain
from prompts.nutrition_prompt import get_main_prompt
from models.openai_model import get_model
import json


def main(ingredients):
    # model initialization
    model = get_model()

    # loads the main prompt template
    main_prompt = get_main_prompt()

    # Create the chain by combining prompt and model
    chain = create_analysis_chain(main_prompt, model)
    response = chain.invoke({"ingredients": ingredients})

    if response.startswith("```json\n") and response.endswith("\n```"):
        response = response[8:-4]

    try:
        json_response = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("The response is not a valid JSON format")

    return json_response

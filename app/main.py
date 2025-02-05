from chains.analysis_chain import create_analysis_chain
from prompts.nutrition_prompt import get_main_prompt
from llm.model import get_model
from utils import clean_response

def main(ingredients):
    try:
        # Get model and prompt
        model = get_model()
        main_prompt = get_main_prompt()

        # Create and run chain
        chain = create_analysis_chain(main_prompt, model)
        response = chain.invoke({"ingredients": ingredients})

        # Clean and parse response
        if isinstance(response, str):
            return clean_response(response)
        return response

    except Exception as e:
        raise ValueError(f"Analysis error: {str(e)}")

from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate


def get_examples():
    """
    Returns few-shot examples for ingredient analysis.
    """
    return [
        {
            "raw_text": """
1. **List of Ingredients:**
- Sugar
- Palm Oil
- Vitamin C
- Salt

2. **Nutritional Facts:**
- Energy: 200 kcal
- Total Fat: 10g
- Saturated Fat: 5g
- Sodium: 300mg
""",
            "analysis": {
                "Sugar": [
                    "Harmful",
                    "Excessive sugar consumption can lead to obesity, diabetes, and tooth decay.",
                ],
                "Palm Oil": [
                    "Neutral",
                    "While it is calorie-dense, it does not contain trans fats if sustainably sourced.",
                ],
                "Vitamin C": [
                    "Beneficial",
                    "It supports the immune system and acts as an antioxidant.",
                ],
                "Salt": [
                    "Neutral",
                    "Necessary in small amounts but harmful in excess due to the risk of high blood pressure.",
                ],
                "overall_rating": 6,
            },
        },
    ]


def get_main_prompt():
    """
    Returns the main prompt template for ingredient analysis.
    :return: LangChain prompt template
    """
    examples = get_examples()

    # Few-shot examples
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=ChatPromptTemplate.from_messages(
            [
                ("human", "{ingredients}"),
                ("ai", "{analysis}"),
            ]
        ),
        examples=examples,
    )

    # Main prompt template
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert nutritionist analyzing food product labels. The following text contains information about the product's ingredients and nutritional facts.
Your task is to:
1. Parse the raw text to identify the list of ingredients and nutritional facts.
2. Analyze each ingredient and provide a rating: "Beneficial", "Neutral", or "Harmful".
3. Include a brief explanation for each ingredient's rating.
4. Calculate an overall product rating (1-10) based on both the ingredients and nutritional facts.
5. Return the results in the following JSON format:
{
    "ingredients": {
        "ingredient_name": {
            "Rating": ["rating", "explanation"]
        },
        ...
    },
    "overall_rating": number
}
If a field is missing or unclear, use "null" as the value.
Do not include nutritional facts in the output. They should only influence the overall rating.
Return ONLY the JSON object without any additional explanations or comments.
""",
            ),
            few_shot_prompt,
            ("human", "{ingredients}"),
        ]
    )

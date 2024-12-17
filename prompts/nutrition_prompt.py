from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate


def get_examples():
    """
    Returns few-shot examples for ingredient analysis.
    """
    return [
        {
            "ingredients": ["Sugar", "Palm Oil", "Vitamin C", "Salt"],
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
            },
            "overall_rating": 6,
        },
        {
            "ingredients": [
                "Whole Grain Oats",
                "Almonds",
                "Honey",
                "Artificial Flavoring",
            ],
            "analysis": {
                "Whole Grain Oats": [
                    "Beneficial",
                    "Rich in fiber, it promotes heart health and improves digestion.",
                ],
                "Almonds": [
                    "Beneficial",
                    "High in healthy fats, vitamins, and antioxidants.",
                ],
                "Honey": [
                    "Neutral",
                    "Natural sweetener but still high in sugar content.",
                ],
                "Artificial Flavoring": [
                    "Harmful",
                    "Contains synthetic chemicals that may cause allergic reactions or health concerns.",
                ],
            },
            "overall_rating": 8,
        },
    ]


def get_main_prompt():
    """
    Returns the main prompt template for ingredient analysis.
    :param model: OpenAI model instance
    :return: LangChain prompt template
    """
    examples = get_examples()

    # Few-shot examples
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=ChatPromptTemplate.from_messages(
            [("human", "{ingredients}"), ("ai", "{analysis}")]
        ),
        examples=examples,
    )

    # Main prompt template
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert nutritionist. When analyzing food ingredients, always return the results in the JSON format.
Include an overall rating (1-10) at the end of the response in the same json format.
Include an overall summary at the end, only if explicitly requested.
""",
            ),
            few_shot_prompt,
            ("human", "{ingredients}"),
        ]
    )

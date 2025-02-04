from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class IngredientAnalysis(BaseModel):
    Sub_ingredients: List[str] = Field(description="List of sub-ingredients")
    Rating: List[str] = Field(description="Rating and explanation")


class AnalysisResponse(BaseModel):
    ingredients: Dict[str, IngredientAnalysis] = Field(
        description="Ingredient analysis"
    )
    overall_rating: int = Field(description="Overall rating (1-10)")
    summary: Optional[str] = Field(default=None, description="Optional summary")


class IngredientRequest(BaseModel):
    ingredients: str

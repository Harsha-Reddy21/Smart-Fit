from typing import Optional
from pydantic import BaseModel


class NutritionCreate(BaseModel):
    user_id: int
    date: str
    meals: Optional[str] = None
    calories: Optional[int] = None
    macronutrients: Optional[str] = None


class NutritionUpdate(BaseModel):
    user_id: Optional[int] = None
    date: Optional[str] = None
    meals: Optional[str] = None
    calories: Optional[int] = None
    macronutrients: Optional[str] = None


class NutritionRead(BaseModel):
    id: int
    user_id: int
    date: str
    meals: Optional[str] = None
    calories: Optional[int] = None
    macronutrients: Optional[str] = None






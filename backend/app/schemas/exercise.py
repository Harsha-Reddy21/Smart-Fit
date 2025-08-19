from typing import Optional
from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    exercise_name: str
    category: Optional[str] = None
    equipment_needed: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None
    target_muscles: Optional[str] = None


class ExerciseUpdate(BaseModel):
    exercise_name: Optional[str] = None
    category: Optional[str] = None
    equipment_needed: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None
    target_muscles: Optional[str] = None


class ExerciseRead(BaseModel):
    id: int
    exercise_name: str
    category: Optional[str] = None
    equipment_needed: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None
    target_muscles: Optional[str] = None






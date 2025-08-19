from typing import Optional
from pydantic import BaseModel


class WorkoutCreate(BaseModel):
    plan_name: str
    difficulty_level: Optional[str] = None
    duration: Optional[int] = None
    target_muscle_groups: Optional[str] = None
    exercises_list: Optional[str] = None


class WorkoutUpdate(BaseModel):
    plan_name: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration: Optional[int] = None
    target_muscle_groups: Optional[str] = None
    exercises_list: Optional[str] = None


class WorkoutRead(BaseModel):
    id: int
    plan_name: str
    difficulty_level: Optional[str] = None
    duration: Optional[int] = None
    target_muscle_groups: Optional[str] = None
    exercises_list: Optional[str] = None

    class Config:
        from_attributes = True





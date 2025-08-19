from typing import Optional
from pydantic import BaseModel


class ProgressCreate(BaseModel):
    user_id: int
    workout_id: Optional[int] = None
    date: str
    exercises_completed: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weights: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[int] = None


class ProgressUpdate(BaseModel):
    user_id: Optional[int] = None
    workout_id: Optional[int] = None
    date: Optional[str] = None
    exercises_completed: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weights: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[int] = None


class ProgressRead(BaseModel):
    id: int
    user_id: int
    workout_id: Optional[int] = None
    date: str
    exercises_completed: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weights: Optional[str] = None
    duration: Optional[int] = None
    calories_burned: Optional[int] = None

    class Config:
        from_attributes = True




from pydantic import BaseModel
import uuid

class Users(BaseModel):
    id: str
    username: str   
    email: str 
    password: str 
    age: int 
    weight: int 
    height: int 
    goals: int 

class Workouts(BaseModel):
    id: str 
    user_id: str 
    plan_name: str 
    exercise: str 
    duration: int 


class Nutrition(BaseModel):
    id:str 
    user_id: str 
    date : str 
    meals: str 
    calories: int 
    macros: str 

class Progress(BaseModel):
    id : int 
    user_id : int 
    workout_id: str 
    sets : int 
    reps: int 
    weights: int  
    notes : str 

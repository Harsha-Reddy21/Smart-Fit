from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    goals: Optional[str] = None
    medical_conditions: Optional[str] = None
    activity_level: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    username: str




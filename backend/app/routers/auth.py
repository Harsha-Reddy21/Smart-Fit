from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, LoginResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.scalar(select(User).where(User.username == payload.username))
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(**payload.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == payload.username))
    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return LoginResponse(user_id=user.id, username=user.username)


@router.get("/user/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "weight": user.weight,
        "height": user.height,
        "goals": user.goals,
        "medical_conditions": user.medical_conditions,
        "activity_level": user.activity_level,
    }




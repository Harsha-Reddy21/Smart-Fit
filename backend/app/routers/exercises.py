from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("")
def list_exercises(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)):
    stmt = select(Exercise).offset(offset).limit(limit)
    return session.execute(stmt).scalars().all()


@router.post("")
def create_exercise(ex: ExerciseCreate, session: Session = Depends(get_session)):
    ex_db = Exercise(**ex.model_dump())
    session.add(ex_db)
    session.commit()
    session.refresh(ex_db)
    return ex_db


@router.put("/{exercise_id}")
def update_exercise(exercise_id: int, ex: ExerciseUpdate, session: Session = Depends(get_session)):
    existing = session.get(Exercise, exercise_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for field, value in ex.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, session: Session = Depends(get_session)):
    existing = session.get(Exercise, exercise_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Exercise not found")
    session.delete(existing)
    session.commit()
    return {"ok": True}




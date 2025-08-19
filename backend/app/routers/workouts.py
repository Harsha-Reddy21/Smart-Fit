from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.workout import WorkoutPlan
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutRead


router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("", response_model=List[WorkoutRead])
def list_workouts(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)):
    stmt = select(WorkoutPlan).offset(offset).limit(limit)
    return session.execute(stmt).scalars().all()


@router.get("/{plan_id}", response_model=WorkoutRead)
def get_workout(plan_id: int, session: Session = Depends(get_session)):
    existing = session.get(WorkoutPlan, plan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return existing


@router.post("", response_model=WorkoutRead)
def create_workout(plan: WorkoutCreate, session: Session = Depends(get_session)):
    plan_db = WorkoutPlan(**plan.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.put("/{plan_id}", response_model=WorkoutRead)
def update_workout(plan_id: int, plan: WorkoutUpdate, session: Session = Depends(get_session)):
    existing = session.get(WorkoutPlan, plan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    for field, value in plan.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{plan_id}")
def delete_workout(plan_id: int, session: Session = Depends(get_session)):
    existing = session.get(WorkoutPlan, plan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    session.delete(existing)
    session.commit()
    return {"ok": True}




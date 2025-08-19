from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.nutrition import Nutrition
from app.schemas.nutrition import NutritionCreate, NutritionUpdate


router = APIRouter(prefix="/nutrition", tags=["nutrition"])


@router.get("")
def list_nutrition(user_id: Optional[int] = None, session: Session = Depends(get_session)):
    stmt = select(Nutrition)
    if user_id is not None:
        stmt = stmt.where(Nutrition.user_id == user_id)
    return session.execute(stmt).scalars().all()


@router.post("")
def create_nutrition(n: NutritionCreate, session: Session = Depends(get_session)):
    n_db = Nutrition(**n.model_dump())
    session.add(n_db)
    session.commit()
    session.refresh(n_db)
    return n_db


@router.put("/{nutrition_id}")
def update_nutrition(nutrition_id: int, n: NutritionUpdate, session: Session = Depends(get_session)):
    existing = session.get(Nutrition, nutrition_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Nutrition entry not found")
    for field, value in n.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{nutrition_id}")
def delete_nutrition(nutrition_id: int, session: Session = Depends(get_session)):
    existing = session.get(Nutrition, nutrition_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Nutrition entry not found")
    session.delete(existing)
    session.commit()
    return {"ok": True}




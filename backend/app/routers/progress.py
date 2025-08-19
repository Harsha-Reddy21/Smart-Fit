from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressRead


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=List[ProgressRead])
def list_progress(user_id: Optional[int] = None, session: Session = Depends(get_session)):
    stmt = select(Progress)
    if user_id is not None:
        stmt = stmt.where(Progress.user_id == user_id)
    return session.execute(stmt).scalars().all()


@router.post("", response_model=ProgressRead)
def create_progress(p: ProgressCreate, session: Session = Depends(get_session)):
    progress_db = Progress(**p.model_dump())
    session.add(progress_db)
    session.commit()
    session.refresh(progress_db)
    return progress_db


@router.put("/{progress_id}", response_model=ProgressRead)
def update_progress(progress_id: int, p: ProgressUpdate, session: Session = Depends(get_session)):
    existing = session.get(Progress, progress_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    for field, value in p.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


@router.delete("/{progress_id}")
def delete_progress(progress_id: int, session: Session = Depends(get_session)):
    existing = session.get(Progress, progress_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    session.delete(existing)
    session.commit()
    return {"ok": True}




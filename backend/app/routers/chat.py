from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_session
from app.models.chat import ChatMessage
from app.models.user import User
from app.rag.retriever import retrieve_context


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask")
def generate_answer(user_id: int, question: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    context_items = retrieve_context(question)
    context_text = " \n".join(f"- {it['title']}: {it['text']}" for it in context_items)
    profile_bits = []
    if user.goals:
        profile_bits.append(f"goal={user.goals}")
    if user.activity_level:
        profile_bits.append(f"activity={user.activity_level}")
    profile_summary = ", ".join(profile_bits) or "profile not set"
    answer = (
        f"Considering your {profile_summary}, here is guidance based on similar knowledge:\n"
        f"{context_text}\n"
        f"Apply gradually and track response (sets/reps/loads, energy, soreness)."
    )
    msg = ChatMessage(user_id=user_id, question=question, answer=answer)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return {"answer": answer}


@router.get("/history/{user_id}")
def get_chat_history(user_id: int, session: Session = Depends(get_session)):
    stmt = select(ChatMessage).where(ChatMessage.user_id == user_id).order_by(ChatMessage.created_at.desc())
    return session.execute(stmt).scalars().all()




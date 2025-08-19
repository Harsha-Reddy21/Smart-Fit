from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.db.base import Base


class WorkoutPlan(Base):
    __tablename__ = "workoutplan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plan_name: Mapped[str] = mapped_column(String)
    difficulty_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_muscle_groups: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    exercises_list: Mapped[Optional[str]] = mapped_column(String, nullable=True)




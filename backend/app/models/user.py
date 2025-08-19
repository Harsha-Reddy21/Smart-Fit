from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    goals: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    medical_conditions: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    activity_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)




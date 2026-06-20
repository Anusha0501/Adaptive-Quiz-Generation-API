import uuid
from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    quizzes: Mapped[list["Quiz"]] = relationship(back_populates="user")


class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    topic: Mapped[str] = mapped_column(String(255), index=True)
    difficulty: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), default="generated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user: Mapped[User | None] = relationship(back_populates="quizzes")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )
    attempts: Mapped[list["Attempt"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )
    analytics: Mapped["Analytics"] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), index=True)
    question: Mapped[str] = mapped_column(Text)
    options: Mapped[list[str]] = mapped_column(JSON)
    answer: Mapped[str] = mapped_column(Text)
    bloom_level: Mapped[str] = mapped_column(String(32), index=True)
    difficulty_score: Mapped[float] = mapped_column(Float)
    validation_score: Mapped[float] = mapped_column(Float)
    quiz: Mapped[Quiz] = relationship(back_populates="questions")


class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    answers: Mapped[dict] = mapped_column(JSON)
    score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    quiz: Mapped[Quiz] = relationship(back_populates="attempts")


class Analytics(Base):
    __tablename__ = "analytics"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id"), unique=True)
    generation_ms: Mapped[int] = mapped_column(Integer)
    duplicate_regenerations: Mapped[int] = mapped_column(Integer, default=0)
    average_validation_score: Mapped[float] = mapped_column(Float)
    quiz: Mapped[Quiz] = relationship(back_populates="analytics")

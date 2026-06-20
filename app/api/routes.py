from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models import Analytics, Question, Quiz
from app.schemas.quiz import (
    QuizGenerateRequest,
    QuizResponse,
    QuestionSchema,
    ValidateQuizRequest,
    ValidationResponse,
)
from app.services.quiz_generation import QuizGenerationService
from app.validators.question_validator import QuestionValidator

router = APIRouter(tags=["quiz"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/generate-quiz", response_model=QuizResponse)
async def generate_quiz(payload: QuizGenerateRequest, session: AsyncSession = Depends(get_session)):
    service = QuizGenerationService()
    generated, metrics = await service.generate(
        payload.topic, payload.difficulty, payload.number_of_questions
    )
    quiz = Quiz(topic=payload.topic, difficulty=payload.difficulty)
    session.add(quiz)
    await session.flush()
    for item in generated:
        session.add(Question(quiz_id=quiz.id, **item))
    session.add(
        Analytics(
            quiz_id=quiz.id,
            generation_ms=metrics["generation_ms"],
            duplicate_regenerations=metrics["duplicate_regenerations"],
            average_validation_score=sum(q["validation_score"] for q in generated) / len(generated),
        )
    )
    await session.commit()
    return QuizResponse(
        id=quiz.id,
        topic=quiz.topic,
        difficulty=quiz.difficulty,
        questions=[QuestionSchema(**q) for q in generated],
    )


@router.post("/validate-quiz", response_model=ValidationResponse)
async def validate_quiz(payload: ValidateQuizRequest):
    validator = QuestionValidator()
    issues: list[str] = []
    scores: list[float] = []
    seen: set[str] = set()
    for question in payload.questions:
        data = question.model_dump()
        if data["question"].lower() in seen:
            issues.append("Duplicate question text detected.")
        seen.add(data["question"].lower())
        score, item_issues = validator.validate(payload.topic, payload.difficulty, data)
        scores.append(score)
        issues.extend(item_issues)
    score = round(sum(scores) / len(scores), 2) if scores else 0
    return ValidationResponse(valid=score >= 0.8 and not issues, score=score, issues=issues)


@router.get("/quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = (
        (await session.execute(select(Question).where(Question.quiz_id == quiz.id))).scalars().all()
    )
    return QuizResponse(
        id=quiz.id,
        topic=quiz.topic,
        difficulty=quiz.difficulty,
        questions=[QuestionSchema.model_validate(q, from_attributes=True) for q in questions],
    )


@router.delete("/quiz/{quiz_id}", status_code=204)
async def delete_quiz(quiz_id: UUID, session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Quiz).where(Quiz.id == quiz_id))
    await session.commit()


@router.get("/analytics")
async def analytics(session: AsyncSession = Depends(get_session)):
    rows = (await session.execute(select(Analytics))).scalars().all()
    return {
        "quiz_count": len(rows),
        "average_generation_ms": sum(r.generation_ms for r in rows) / len(rows) if rows else 0,
    }

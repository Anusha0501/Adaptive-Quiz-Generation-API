import pytest
from pydantic import ValidationError

from app.embeddings.duplicate_detector import DuplicateDetector
from app.schemas.quiz import QuestionSchema, QuizGenerateRequest


@pytest.mark.asyncio
async def test_duplicate_detector_flags_exact_reuse():
    detector = DuplicateDetector()
    text = "Which option best explains Redis caching for session storage?"
    assert await detector.is_duplicate(text) is False
    await detector.store("q1", text)
    assert await detector.is_duplicate(text) is True


def test_generate_request_accepts_question_count():
    request = QuizGenerateRequest(topic="Redis", difficulty="easy", number_of_questions=5)
    assert request.number_of_questions == 5


def test_generate_request_rejects_too_many_questions():
    with pytest.raises(ValidationError):
        QuizGenerateRequest(topic="Redis", difficulty="easy", number_of_questions=11)


def test_question_schema_requires_answer_in_options():
    with pytest.raises(ValidationError):
        QuestionSchema(
            question="Which option identifies Redis as an in-memory data store?",
            options=["A", "B", "C", "D"],
            answer="E",
            bloom_level="Remember",
            difficulty_score=0.2,
            validation_score=0.9,
        )

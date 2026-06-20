import pytest
from app.quiz_engine.bloom import BloomTaxonomyMapper
from app.quiz_engine.difficulty import DifficultyController
from app.services.quiz_generation import QuizGenerationService
from app.validators.question_validator import QuestionValidator


@pytest.mark.asyncio
async def test_generates_ten_unique_questions():
    questions, metrics = await QuizGenerationService().generate("PostgreSQL indexing", "medium")
    assert len(questions) == 10
    assert len({q["question"] for q in questions}) == 10
    assert metrics["generation_ms"] >= 0


def test_bloom_mapper_cycles_by_difficulty():
    mapper = BloomTaxonomyMapper()
    assert mapper.select_level("hard", 0) == "Analyze"
    assert mapper.select_level("hard", 2) == "Create"


def test_difficulty_alignment():
    controller = DifficultyController()
    assert controller.aligned(
        controller.score("Analyze distributed caches for Redis consistency", "hard", "Analyze"),
        "hard",
    )


def test_validator_flags_bad_question():
    score, issues = QuestionValidator().validate(
        "Redis",
        "easy",
        {
            "question": "What is it?",
            "options": ["A", "A", "B", "C"],
            "answer": "D",
            "bloom_level": "Remember",
            "difficulty_score": 0.9,
        },
    )
    assert score < 1
    assert issues

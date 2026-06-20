import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_validate_quiz():
    payload = {
        "topic": "Redis",
        "difficulty": "easy",
        "questions": [
            {
                "question": "Which option best asks you to identify Redis at an easy level?",
                "options": ["Redis answer", "B", "C", "D"],
                "answer": "Redis answer",
                "bloom_level": "Remember",
                "difficulty_score": 0.25,
                "validation_score": 1.0,
            }
        ],
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/validate-quiz", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] >= 0.8

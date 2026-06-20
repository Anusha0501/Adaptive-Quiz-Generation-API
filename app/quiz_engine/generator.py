import json
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.quiz_engine.bloom import BloomTaxonomyMapper


class QuestionGenerator:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = (
            AsyncOpenAI(api_key=self.settings.openai_api_key)
            if self.settings.openai_api_key
            else None
        )
        self.bloom = BloomTaxonomyMapper()

    async def generate_one(self, topic: str, difficulty: str, index: int) -> dict:
        bloom_level = self.bloom.select_level(difficulty, index)
        if not self.client:
            return self._fallback(topic, difficulty, bloom_level, index)
        prompt = (
            "Return strict JSON for one unique multiple-choice question with keys "
            "question, options, answer, bloom_level. Use exactly four options. "
            f"Topic: {topic}. Difficulty: {difficulty}. Bloom level: {bloom_level}."
        )
        response = await self.client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content or "{}")
        data["bloom_level"] = data.get("bloom_level") or bloom_level
        return data

    def _fallback(self, topic: str, difficulty: str, bloom_level: str, index: int) -> dict:
        verbs = {
            "Remember": "identify",
            "Understand": "explain",
            "Apply": "apply",
            "Analyze": "analyze",
            "Evaluate": "evaluate",
            "Create": "design",
        }
        correct = f"A {difficulty} {bloom_level.lower()} concept for {topic} #{index + 1}"
        return {
            "question": f"Which option best asks you to {verbs[bloom_level]} {topic} at a {difficulty} level for scenario {index + 1}?",
            "options": [
                correct,
                f"Unrelated distractor {index}-A",
                f"Overly broad distractor {index}-B",
                f"Incorrect misconception {index}-C",
            ],
            "answer": correct,
            "bloom_level": bloom_level,
        }

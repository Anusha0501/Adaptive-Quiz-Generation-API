import time
import uuid
from app.embeddings.duplicate_detector import DuplicateDetector
from app.quiz_engine.difficulty import DifficultyController
from app.quiz_engine.generator import QuestionGenerator
from app.validators.question_validator import QuestionValidator


class QuizGenerationService:
    def __init__(
        self, generator: QuestionGenerator | None = None, detector: DuplicateDetector | None = None
    ) -> None:
        self.generator = generator or QuestionGenerator()
        self.detector = detector or DuplicateDetector()
        self.difficulty = DifficultyController()
        self.validator = QuestionValidator()

    async def generate(
        self, topic: str, difficulty: str, count: int = 10
    ) -> tuple[list[dict], dict]:
        start = time.perf_counter()
        questions: list[dict] = []
        regenerations = 0
        index = 0
        while len(questions) < count:
            candidate = await self.generator.generate_one(topic, difficulty, index + regenerations)
            candidate["difficulty_score"] = self.difficulty.score(
                candidate["question"], difficulty, candidate["bloom_level"]
            )
            score, _ = self.validator.validate(topic, difficulty, candidate)
            candidate["validation_score"] = score
            if await self.detector.is_duplicate(candidate["question"]):
                regenerations += 1
                continue
            await self.detector.store(str(uuid.uuid4()), candidate["question"])
            questions.append(candidate)
            index += 1
        return questions, {
            "generation_ms": int((time.perf_counter() - start) * 1000),
            "duplicate_regenerations": regenerations,
        }

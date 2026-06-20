import math
from app.core.config import get_settings
from app.embeddings.provider import EmbeddingProvider


class DuplicateDetector:
    def __init__(self, provider: EmbeddingProvider | None = None) -> None:
        self.provider = provider or EmbeddingProvider()
        self.threshold = get_settings().similarity_threshold
        self._vectors: list[tuple[str, list[float]]] = []

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        return dot / ((math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))) or 1)

    async def is_duplicate(self, text: str) -> bool:
        vector = await self.provider.embed(text)
        return any(self.cosine(vector, existing) >= self.threshold for _, existing in self._vectors)

    async def store(self, question_id: str, text: str) -> None:
        self._vectors.append((question_id, await self.provider.embed(text)))

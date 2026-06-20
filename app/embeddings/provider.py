import hashlib
import numpy as np
from openai import AsyncOpenAI
from app.core.config import get_settings


class EmbeddingProvider:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = (
            AsyncOpenAI(api_key=self.settings.openai_api_key)
            if self.settings.openai_api_key
            else None
        )

    async def embed(self, text: str) -> list[float]:
        if self.client:
            response = await self.client.embeddings.create(
                model=self.settings.embedding_model, input=text
            )
            return response.data[0].embedding
        digest = hashlib.sha256(text.lower().encode()).digest()
        vector = np.frombuffer(digest * 48, dtype=np.uint8)[:1536].astype(float)
        norm = np.linalg.norm(vector) or 1
        return (vector / norm).tolist()

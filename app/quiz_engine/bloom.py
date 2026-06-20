from dataclasses import dataclass

BLOOM_LEVELS = ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create")


@dataclass(frozen=True)
class BloomTaxonomyMapper:
    by_difficulty: dict[str, tuple[str, ...]] = None

    def __post_init__(self):
        object.__setattr__(
            self,
            "by_difficulty",
            {
                "easy": ("Remember", "Understand"),
                "medium": ("Understand", "Apply", "Analyze"),
                "hard": ("Analyze", "Evaluate", "Create"),
            },
        )

    def select_level(self, difficulty: str, index: int) -> str:
        levels = self.by_difficulty[difficulty]
        return levels[index % len(levels)]

    def classify(self, question: str, difficulty: str) -> str:
        lowered = question.lower()
        keywords = {
            "Remember": ("define", "identify", "list", "recall"),
            "Understand": ("explain", "summarize", "describe"),
            "Apply": ("use", "calculate", "implement"),
            "Analyze": ("compare", "differentiate", "analyze"),
            "Evaluate": ("judge", "critique", "evaluate", "best"),
            "Create": ("design", "construct", "propose"),
        }
        for level, words in keywords.items():
            if any(word in lowered for word in words):
                return level
        return self.select_level(difficulty, 0)

class DifficultyController:
    targets = {"easy": 0.25, "medium": 0.55, "hard": 0.85}

    def score(self, question: str, difficulty: str, bloom_level: str) -> float:
        base = self.targets[difficulty]
        length_adjustment = min(len(question.split()) / 80, 0.1)
        bloom_adjustment = {
            "Remember": -0.05,
            "Understand": 0,
            "Apply": 0.03,
            "Analyze": 0.07,
            "Evaluate": 0.1,
            "Create": 0.12,
        }.get(bloom_level, 0)
        return max(0, min(1, round(base + length_adjustment + bloom_adjustment, 2)))

    def aligned(self, score: float, difficulty: str) -> bool:
        ranges = {"easy": (0, 0.45), "medium": (0.35, 0.75), "hard": (0.65, 1)}
        low, high = ranges[difficulty]
        return low <= score <= high

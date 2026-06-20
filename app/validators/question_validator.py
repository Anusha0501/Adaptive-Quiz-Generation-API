from app.quiz_engine.difficulty import DifficultyController


class QuestionValidator:
    def __init__(self) -> None:
        self.difficulty = DifficultyController()

    def validate(self, topic: str, difficulty: str, question: dict) -> tuple[float, list[str]]:
        issues: list[str] = []
        text = question["question"]
        options = question["options"]
        if topic.lower() not in text.lower():
            issues.append("Question should explicitly reference the requested topic.")
        if len(set(options)) != 4:
            issues.append("Options must be unique.")
        if question["answer"] not in options:
            issues.append("Answer must be one of the options.")
        if not self.difficulty.aligned(question["difficulty_score"], difficulty):
            issues.append("Difficulty score is outside target band.")
        if len(text.split()) < 8:
            issues.append("Question is too short for reliable assessment.")
        return round(max(0, 1 - len(issues) * 0.2), 2), issues

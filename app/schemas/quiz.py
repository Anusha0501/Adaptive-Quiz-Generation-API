from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class QuizGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=120)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    number_of_questions: int = Field(10, ge=1, le=10)


class QuestionSchema(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    answer: str
    bloom_level: str
    difficulty_score: float = Field(ge=0, le=1)
    validation_score: float = Field(ge=0, le=1)

    @field_validator("answer")
    @classmethod
    def answer_must_be_option(cls, value: str, info):
        options = info.data.get("options", [])
        if options and value not in options:
            raise ValueError("answer must match one option")
        return value


class QuizResponse(BaseModel):
    id: UUID
    topic: str
    difficulty: str
    questions: list[QuestionSchema]


class ValidateQuizRequest(BaseModel):
    topic: str
    difficulty: str
    questions: list[QuestionSchema]


class ValidationResponse(BaseModel):
    valid: bool
    score: float
    issues: list[str]

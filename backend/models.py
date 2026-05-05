from datetime import datetime
from pydantic import BaseModel


class WordCreate(BaseModel):
    original: str
    translation: str


class WordResponse(BaseModel):
    id: int
    original: str
    translation: str
    created_at: datetime
    is_difficult: bool = False
    review_count: int = 0
    ease_factor: float = 2.5
    interval_days: int = 0
    next_review_at: datetime | None = None


class QuizQuestion(BaseModel):
    id: int
    original: str
    options: list[str]
    answer_index: int
    mode: str = "normal"  # "normal" or "reverse"


class ReviewResult(BaseModel):
    word_id: int
    correct: bool

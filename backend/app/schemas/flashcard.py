from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FlashcardBase(BaseModel):
    question: str
    answer: str
    difficulty_level: str
    topic: Optional[str] = None

class FlashcardCreate(FlashcardBase):
    document_id: int

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    difficulty_level: Optional[str] = None
    topic: Optional[str] = None

class FlashcardResponse(FlashcardBase):
    id: int
    user_id: int
    document_id: int
    review_count: int
    last_reviewed_date: Optional[datetime]
    next_review_date: datetime
    ease_factor: float
    interval: int
    created_at: datetime

    class Config:
        from_attributes = True

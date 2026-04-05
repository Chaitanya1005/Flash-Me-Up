from pydantic import BaseModel
from datetime import datetime

class ReviewLogCreate(BaseModel):
    flashcard_id: int
    score: int # 1=red, 2=yellow, 3=green

class ReviewLogResponse(BaseModel):
    id: int
    flashcard_id: int
    user_id: int
    score: int
    reviewed_at: datetime

    class Config:
        from_attributes = True

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db
from app.models.flashcard import Flashcard
from app.models.review_log import ReviewLog

router = APIRouter()

@router.get("/{user_id}")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    total_cards = db.query(func.count(Flashcard.id)).filter(Flashcard.user_id == user_id).scalar()
    
    total_reviews = db.query(func.count(ReviewLog.id)).filter(ReviewLog.user_id == user_id).scalar()
    
    if total_reviews > 0:
        green_reviews = db.query(func.count(ReviewLog.id)).filter(
            ReviewLog.user_id == user_id, 
            ReviewLog.score == 3
        ).scalar()
        accuracy = round((green_reviews / total_reviews) * 100, 2)
    else:
        accuracy = 0.0
        
    return {
        "user_id": user_id,
        "total_cards": total_cards,
        "total_reviews": total_reviews,
        "accuracy_percentage": accuracy
    }

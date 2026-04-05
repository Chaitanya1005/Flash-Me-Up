from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db
from app.models.flashcard import Flashcard
from app.models.review_log import ReviewLog
from app.schemas.flashcard import FlashcardResponse
from app.schemas.review_log import ReviewLogCreate
from app.core.srs import calculate_sm2, get_next_review_date
from datetime import datetime
from typing import List

router = APIRouter()

@router.get("/due/{user_id}", response_model=List[FlashcardResponse])
def get_due_flashcards(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    due_cards = db.query(Flashcard).filter(
        Flashcard.user_id == user_id,
        Flashcard.next_review_date <= now
    ).order_by(Flashcard.next_review_date.asc()).limit(limit).all()
    
    return due_cards

@router.post("/{flashcard_id}/review")
def submit_review_result(flashcard_id: int, review: ReviewLogCreate, db: Session = Depends(get_db)):
    card = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    if review.score not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Score must be 1 (red), 2 (yellow), or 3 (green)")

    log = ReviewLog(
        flashcard_id=flashcard_id,
        user_id=card.user_id,
        score=review.score
    )
    db.add(log)
    
    new_srs = calculate_sm2(
        quality=review.score,
        repetitions=card.review_count,
        previous_interval=card.interval,
        previous_ease_factor=card.ease_factor
    )
    
    card.review_count = new_srs["repetitions"]
    card.interval = new_srs["interval"]
    card.ease_factor = new_srs["ease_factor"]
    card.last_reviewed_date = datetime.utcnow()
    card.next_review_date = get_next_review_date(new_srs["interval"])
    
    db.commit()
    db.refresh(card)
    return {"status": "success", "next_review_date": card.next_review_date}

@router.get("/document/{document_id}", response_model=List[FlashcardResponse])
def get_document_flashcards(document_id: int, db: Session = Depends(get_db)):
    cards = db.query(Flashcard).filter(Flashcard.document_id == document_id).all()
    return cards

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty_level = Column(String) # easy/medium/hard
    topic = Column(String)

    # Spaced Repetition details
    review_count = Column(Integer, default=0)
    last_reviewed_date = Column(DateTime(timezone=True), nullable=True)
    next_review_date = Column(DateTime(timezone=True), default=func.now())
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0) # Days until next review

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="flashcards")
    owner = relationship("User", back_populates="flashcards")
    review_logs = relationship("ReviewLog", back_populates="flashcard")

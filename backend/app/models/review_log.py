from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ReviewLog(Base):
    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    score = Column(Integer, nullable=False) # 1=red, 2=yellow, 3=green
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    flashcard = relationship("Flashcard", back_populates="review_logs")
    user = relationship("User", back_populates="review_logs")

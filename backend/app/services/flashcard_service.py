from sqlalchemy.orm import Session
from app.models.flashcard import Flashcard
from app.services.chunker import chunk_text
from app.services.llm import generate_flashcards

def process_document_and_generate_flashcards(db: Session, document_id: int, user_id: int, extracted_text: str):
    chunks = chunk_text(extracted_text)
    
    all_flashcards = []
    
    for chunk in chunks:
        generated_cards = generate_flashcards(chunk)
        
        for card_data in generated_cards:
            flashcard = Flashcard(
                document_id=document_id,
                user_id=user_id,
                question=card_data.get("question", "N/A"),
                answer=card_data.get("answer", "N/A"),
                difficulty_level=card_data.get("difficulty_level", "medium"),
                topic=card_data.get("topic", "General")
            )
            db.add(flashcard)
            all_flashcards.append(flashcard)
            
    db.commit()
    return all_flashcards

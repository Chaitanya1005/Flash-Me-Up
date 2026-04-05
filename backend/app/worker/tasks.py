from app.db.session import SessionLocal
from app.models.document import Document, DocumentStatus
from app.services.parser import extract_text
from app.services.flashcard_service import process_document_and_generate_flashcards
import logging

logger = logging.getLogger(__name__)

def process_document_task(document_id: int, user_id: int, filename: str, content: bytes, content_type: str):
    db = SessionLocal()
    try:
        # Update status to processing
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = DocumentStatus.PROCESSING
            db.commit()
            
        # Extract text
        extracted_text = extract_text(filename, content, content_type)
        
        # Process and generate
        process_document_and_generate_flashcards(db, document_id, user_id, extracted_text)
        
        # Update status to completed
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = DocumentStatus.COMPLETED
            db.commit()
            
        return {"status": "success", "document_id": document_id}
    except Exception as e:
        logger.error(f"Failed to process document {document_id}: {e}")
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = DocumentStatus.FAILED
            db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

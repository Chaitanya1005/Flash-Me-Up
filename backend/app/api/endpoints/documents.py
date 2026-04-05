from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from typing import List
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.worker.tasks import process_document_task

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    valid_content_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/plain"]
    if file.content_type not in valid_content_types and not file.filename.endswith((".pdf", ".pptx", ".txt")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, PPTX, and TXT are supported.")
        
    content = await file.read()
    
    doc = Document(
        user_id=user_id,
        filename=file.filename,
        content_type=file.content_type,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    background_tasks.add_task(
        process_document_task,
        document_id=doc.id,
        user_id=user_id,
        filename=file.filename,
        content=content,
        content_type=file.content_type
    )
    
    return doc

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/user/{user_id}", response_model=List[DocumentResponse])
def get_user_documents(user_id: int, db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()
    return docs

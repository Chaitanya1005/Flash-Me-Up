from pydantic import BaseModel
from datetime import datetime
from app.models.document import DocumentStatus

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    content_type: str

class DocumentUpdate(BaseModel):
    status: DocumentStatus

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    content_type: str
    status: DocumentStatus
    created_at: datetime

    class Config:
        from_attributes = True

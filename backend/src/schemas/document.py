from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    notebookId: str
    userId: str
    filename: str
    content: str
    createdAt: datetime


class DocumentUploadOut(DocumentOut):
    chunksCreated: int

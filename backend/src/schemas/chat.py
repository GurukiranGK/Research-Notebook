from pydantic import BaseModel


class ChatRequest(BaseModel):
    documentId: str
    question: str

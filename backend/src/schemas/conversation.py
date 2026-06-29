from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field



class ConversationCreate(BaseModel):
    notebookId: str
    title: str = Field(
        default="New conversation",
        min_length=1,
        max_length=200,
    )

class MessageCreate(BaseModel):
    documentId: str
    content: str


class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    userId: str
    notebookId: str
    title: str
    summary: str | None = None
    createdAt: datetime
    updatedAt: datetime




class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversationId: str
    role: str
    content: str
    createdAt: datetime

class ConversationMessageResponse(BaseModel):
    userMessage: MessageOut
    assistantMessage: MessageOut
    answer: str
    sources: list[str]
    summary: str
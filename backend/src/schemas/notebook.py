from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotebookCreate(BaseModel):
    title: str


class NotebookUpdate(BaseModel):
    title: str


class NotebookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    userId: str
    createdAt: datetime
    updatedAt: datetime

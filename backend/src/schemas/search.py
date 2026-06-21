from pydantic import BaseModel


class SearchRequest(BaseModel):
    documentId: str
    query: str

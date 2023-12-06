from pydantic import BaseModel
from datetime import datetime
class ContentModel(BaseModel):
    id: str | None = None
    type: str | None = None
    title: str | None = None
    file_type: str | None = None
    origin: str | None = None
    target_url: str | None = None
    text_id: str | None = None
    category: str | None = None
    has_vectored: bool = False
    note: str | None = None
    created: datetime
    updated: datetime

class CreateContentModel(BaseModel):
    type: str | None = None
    title: str | None = None
    file_type: str | None = None
    origin: str | None = None
    target_url: str | None = None
    big_text: str | None = None
    category: str | None = None
    note: str | None = None

class UpdateContentModel(BaseModel):
    id: str | None = None
    type: str | None = None
    title: str | None = None
    file_type: str | None = None
    origin: str | None = None
    target_url: str | None = None
    category: str | None = None
    note: str | None = None
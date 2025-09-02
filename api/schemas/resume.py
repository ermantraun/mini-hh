from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ResumeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)

class ResumeUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)

class ResumeOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class ResumeList(BaseModel):
    items: List[ResumeOut]

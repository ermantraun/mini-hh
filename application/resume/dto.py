from dataclasses import dataclass
from datetime import datetime
from typing import List

# Application DTO (без pydantic). Валидация — задача transport слоя.

@dataclass
class ResumeCreateDTO:
    title: str
    content: str


@dataclass
class ResumeUpdateDTO:
    title: str
    content: str


@dataclass
class ResumeOutDTO:
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


@dataclass
class ResumeListDTO:
    items: List[ResumeOutDTO]
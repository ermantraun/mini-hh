from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: int
    email: str
    hashed_password: str
    created_at: datetime


@dataclass(frozen=True)
class Resume:
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ResumeImprovement:
    id: int
    resume_id: int
    original_content: str
    improved_content: str
    created_at: datetime
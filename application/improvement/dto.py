from dataclasses import dataclass
from datetime import datetime
from typing import List

# DTO (application layer) — НЕ pydantic, без HTTP-валидации.
# Использовать внутри use-case или сервисов, а не в FastAPI хендлерах.

@dataclass
class ImprovementOutDTO:
    id: int
    resume_id: int
    original_content: str
    improved_content: str
    created_at: datetime


@dataclass
class ImprovementListDTO:
    items: List[ImprovementOutDTO]
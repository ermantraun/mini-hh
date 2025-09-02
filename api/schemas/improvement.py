from pydantic import BaseModel
from datetime import datetime
from typing import List

# Transport (API) schemas — используются FastAPI (валидация / OpenAPI).
# Не путать с application.improvement.dto (dataclass DTO).

class ImprovementOut(BaseModel):
    id: int
    resume_id: int
    original_content: str
    improved_content: str
    created_at: datetime

class ImprovementList(BaseModel):
    items: List[ImprovementOut]
